#!/usr/bin/env python3
"""One-time seeder: build data/legacy_redirects.yaml from git history.

Commit d78f6ba ("promote Blowfish to default and retire Wowchemy") deleted the
whole Wowchemy content tree. Every URL it served now 404s. This script walks the
parent commit (93462c9) and reconstructs the old URL space, then resolves each
old publication folder to the PMID that keys data/publications.yaml.

Resolution order for a publication slug:
  1. data/pub_meta.yaml still embeds the old slug in its `pdf` links, and is
     itself keyed by PMID. That gives the pair directly.
  2. Fall back to the `doi` in the old front matter, matched against
     data/publications.yaml (repairing a known leading-zero typo).

NOT part of CI. Run once, review the YAML, then hand-maintain it.
Regenerate static/_redirects with scripts/gen_redirects.py.
"""
import re
import subprocess
import sys
import unicodedata

import yaml

MIGRATION = "d78f6ba"           # the commit that deleted the old tree
PRE_MIGRATION = MIGRATION + "^"  # 93462c9, where the old tree still lives
OUT = "data/legacy_redirects.yaml"


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.stdout


def old_dirs(section):
    """Directory names under content/<section>/ at the pre-migration commit."""
    out = git("ls-tree", "-d", "--name-only", PRE_MIGRATION, f"content/{section}/")
    return [d.split("/")[-1] for d in out.split("\n") if d.strip()]


def old_file(path):
    return git("show", f"{PRE_MIGRATION}:{path}")


def slugify(s):
    """Hugo's default urlize, close enough for these inputs."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    return re.sub(r"[\s_]+", "-", s)


def front_matter(raw, key):
    m = re.search(rf'^{key}:\s*["\']?([^"\'\n]+)', raw, re.M)
    return m.group(1).strip() if m else ""


def tags_of(raw):
    m = re.search(r"^tags:\n((?:- .*\n)+)", raw, re.M)
    return [t.strip() for t in re.findall(r"^- (.+)$", m.group(1), re.M)] if m else []


def main():
    pubs = yaml.safe_load(open("data/publications.yaml"))["publications"]
    meta = yaml.safe_load(open("data/pub_meta.yaml"))
    by_pmid = {str(p["pmid"]): p for p in pubs if p.get("pmid")}
    by_doi = {p["doi"].strip().lower(): p for p in pubs if p.get("doi")}

    # --- 1. slug -> pmid, via the old slug still embedded in pub_meta pdf links
    slug2pmid = {}
    for pmid, m in meta.items():
        for url in ((m or {}).get("links") or {}).values():
            if isinstance(url, str):
                hit = re.search(r"content/publication/([^/]+)/", url)
                if hit:
                    slug2pmid[hit.group(1)] = str(pmid)

    publication, unmapped, case_variants = {}, [], {}
    for d in sorted(old_dirs("publication"), key=str.lower):
        slug = d.lower()
        if slug != d:
            case_variants[slug] = d

        pmid = slug2pmid.get(d)
        if pmid and pmid in by_pmid:
            publication[slug] = pmid
            continue

        # --- 2. fall back to the DOI in the old front matter
        doi = front_matter(old_file(f"content/publication/{d}/index.md"), "doi").lower()
        if doi.startswith("0."):      # known typo: kim2024single lost its leading 1
            doi = "1" + doi
        if doi in by_doi:
            publication[slug] = str(by_doi[doi]["pmid"])
        else:
            unmapped.append(slug)

    # --- 3. legacy tags, and which kind of content carried each one
    tag_src = {}
    for section in ("publication", "post", "project", "event"):
        for d in old_dirs(section):
            for t in tags_of(old_file(f"content/{section}/{d}/index.md")):
                tag_src.setdefault(slugify(t), {"query": slugify(t), "on": set()})
                tag_src[slugify(t)]["on"].add(section)

    # How many papers actually carry each curated tag. pub_meta.yaml preserves
    # the legacy tag vocabulary, and entry.html surfaces it as data-tags, so the
    # filter can see it. A tag nothing carries gets a plain fallback instead of
    # dropping the visitor on an empty filtered list.
    tag_counts = {}
    for pmid, m in meta.items():
        if str(pmid) not in by_pmid:
            continue
        for t in (m or {}).get("tags") or []:
            tag_counts[slugify(t)] = tag_counts.get(slugify(t), 0) + 1

    live_tags = set()
    for f in subprocess.run(
        ["sh", "-c", "ls content/posts/*/index.md"], capture_output=True, text=True
    ).stdout.split():
        m = re.search(r'^tags:\s*\[(.+)\]', open(f).read(), re.M)
        if m:
            live_tags |= {slugify(t.strip().strip('"\'')) for t in m.group(1).split(",")}

    tag = {}
    for slug, info in sorted(tag_src.items()):
        if len(slug) < 3:                       # "r" would match every entry
            tag[slug] = "/publications/"
        elif slug in live_tags and "publication" not in info["on"]:
            tag[slug] = f"/tags/{slug}/"
        elif "publication" in info["on"]:
            tag[slug] = ("?q=" + info["query"]) if tag_counts.get(slug) else "/publications/"
        elif info["on"] == {"project"}:
            tag[slug] = "/#software"
        else:
            tag[slug] = "/publications/"

    # --- 4. posts whose slug changed in the move from /post/ to /posts/
    renames = {"binary-genes": "binary-genetics"}
    post = {}
    for d in old_dirs("post"):
        slug = d.lower()
        new = renames.get(slug, slug)
        if new != slug:
            post[slug] = f"/posts/{new}/"

    with open(OUT, "w") as f:
        f.write(f"""\
# Legacy URL map from the Wowchemy -> Blowfish migration (commit {MIGRATION}).
#
# Seeded by scripts/seed_legacy_redirects.py from the pre-migration tree, then
# hand-maintained. Consumed by scripts/gen_redirects.py, which writes
# static/_redirects. Netlify serves that file; Hugo just copies static/ across.
#
# Re-run gen_redirects.py after editing this file.

# Old /publication/<slug>/ -> /publications/#pmid-<pmid>
publication:
""")
        for slug, pmid in sorted(publication.items()):
            f.write(f"  {slug}: '{pmid}'\n")

        f.write("""
# No PMID in data/publications.yaml (thesis, book chapter, non-indexed journal).
# These fall back to /publications/ with no anchor.
publication_unmapped:
""")
        for slug in sorted(unmapped):
            f.write(f"  - {slug}\n")

        f.write("""
# Old directories that were mixed-case. Hugo lowercased them, so the lowercase
# form above is the real URL, but Netlify matches case-sensitively and some
# inbound links may carry the original. Both get a rule.
publication_case_variants:
""")
        for slug, orig in sorted(case_variants.items()):
            f.write(f"  {slug}: {orig}\n")

        f.write("""
# Old /tag/<slug>/. A "?q=..." value means /publications/ with the filter
# prefilled; anything else is a literal path.
tag:
""")
        for slug, dest in sorted(tag.items()):
            f.write(f"  {slug}: '{dest}'\n")

        f.write("""
# Posts whose slug changed. The rest are covered by the /post/* splat.
post:
""")
        for slug, dest in sorted(post.items()):
            f.write(f"  {slug}: {dest}\n")

    print(f"wrote {OUT}")
    print(f"  publication:        {len(publication)} mapped to a PMID")
    print(f"  publication_unmapped: {len(unmapped)} -> {unmapped}")
    print(f"  case variants:      {len(case_variants)}")
    print(f"  tag:                {len(tag)}")
    print(f"  post renames:       {len(post)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
