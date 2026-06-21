#!/usr/bin/env python3
"""One-time seeder: build data/pub_meta.yaml from the legacy Wowchemy
publication folders (content/publication/*/index.md).

The bib (data/pubs.bib) is the canonical publication list but carries minimal
metadata. The legacy folders hold hand-curated overlay data (featured flag,
tags, links, abstracts) that we must not lose. This script resolves each legacy
folder to a PMID and emits ONLY the overlay fields the bib lacks, keyed by PMID
(string).

NOT part of CI. After this seeding run, data/pub_meta.yaml is hand-maintained.
"""
import os
import re
import sys
import glob
import yaml
import bibtexparser
import frontmatter

PUB_DIR = "content/publication"
IN_BIB = "data/pubs.bib"
OUT_YAML = "data/pub_meta.yaml"

PUBMED_RE = re.compile(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", re.IGNORECASE)


def normalize_title(t):
    """Lowercase, strip all non-alphanumeric, collapse whitespace away."""
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def normalize_doi(d):
    return (d or "").strip().lower()


def load_bib_index(path):
    """Return (by_doi, by_title, title_of_pmid) maps.

    by_doi:        normalized doi   -> pmid string
    by_title:      normalized title -> pmid string
    title_of_pmid: pmid string      -> normalized title (for URL verification)
    """
    with open(path, encoding="utf-8") as f:
        db = bibtexparser.load(f)
    by_doi, by_title, title_of_pmid = {}, {}, {}
    for e in db.entries:
        pmid = e.get("pmid", "").strip()
        if not pmid:
            continue
        doi = normalize_doi(e.get("doi", ""))
        if doi:
            by_doi.setdefault(doi, pmid)
        title = normalize_title(re.sub(r"[{}]", "", e.get("title", "")))
        if title:
            by_title.setdefault(title, pmid)
            title_of_pmid[pmid] = title
    return by_doi, by_title, title_of_pmid


def extract_pmid_from_urls(post):
    """Look for a pubmed id in links[].url and url_pdf."""
    candidates = []
    links = post.get("links") or []
    if isinstance(links, list):
        for link in links:
            if isinstance(link, dict) and link.get("url"):
                candidates.append(str(link["url"]))
    elif isinstance(links, dict) and links.get("url"):
        candidates.append(str(links["url"]))
    if post.get("url_pdf"):
        candidates.append(str(post["url_pdf"]))
    for url in candidates:
        m = PUBMED_RE.search(url)
        if m:
            return m.group(1)
    return None


# Confidence tiers for a resolved PMID. Higher wins on collision.
CONF_DOI = 4         # folder DOI matches a bib DOI (exact identifier)
CONF_URL_TITLE = 3   # url PMID's bib title matches the folder title (2 signals)
CONF_URL = 2         # url PMID exists in bib, no contradiction
CONF_TITLE = 1       # folder title matches a bib title, no usable url


def candidate_pmids(post, by_doi, by_title, title_of_pmid):
    """Return a list of (pmid, method, confidence) candidates for one folder,
    ordered by confidence descending. Empty if nothing resolves.

    The legacy folders contain copy-paste errors in BOTH directions:
      * a wrong links[].url pointing at another paper's PMID
        (e.g. maharjan2022natural carried the SARS-CoV-2 PMID), and
      * a wrong pasted title belonging to a different paper
        (e.g. baer2023fibrosis carried liu2023context's title).
    Returning ranked candidates lets the caller resolve collisions by
    confidence, so a high-confidence claim displaces a low-confidence one and
    the loser falls back to its next-best signal.
    """
    url_pmid = extract_pmid_from_urls(post)
    doi = normalize_doi(post.get("doi", ""))
    doi_pmid = by_doi.get(doi) if doi else None
    title = normalize_title(post.get("title", ""))
    title_pmid = by_title.get(title) if title else None

    cands = []
    seen = set()

    def add(pmid, method, conf):
        if pmid and (pmid, method) not in seen:
            seen.add((pmid, method))
            cands.append((pmid, method, conf))

    if doi_pmid:
        add(doi_pmid, "doi", CONF_DOI)
    if url_pmid:
        if title and title_of_pmid.get(url_pmid) == title:
            add(url_pmid, "url+title", CONF_URL_TITLE)
        else:
            add(url_pmid, "url", CONF_URL)
    if title_pmid:
        add(title_pmid, "title", CONF_TITLE)

    cands.sort(key=lambda c: c[2], reverse=True)
    return cands


def no_match_reason(post, by_doi):
    doi = normalize_doi(post.get("doi", ""))
    reason = "no pubmed url; "
    reason += f"doi '{doi}' not in bib; " if doi else "no doi; "
    reason += "title not in bib"
    return reason


def gather_links(post):
    """Collect curated links into an ordered dict of kind -> url.

    Pulls the url_* fields plus any named links[] entries whose name is not the
    generic 'Pubmed' (that one is already covered by the bib's pubmed field).
    """
    links = {}
    field_map = {
        "url_code": "code",
        "url_pdf": "pdf",
        "url_project": "project",
        "url_poster": "poster",
        "url_slides": "slides",
        "url_dataset": "dataset",
    }
    for field, kind in field_map.items():
        val = post.get(field)
        if val and str(val).strip() and str(val).strip() != "#":
            links[kind] = str(val).strip()
    named = post.get("links") or []
    if isinstance(named, list):
        for link in named:
            if not isinstance(link, dict):
                continue
            name = str(link.get("name", "")).strip()
            url = str(link.get("url", "")).strip()
            if not name or not url:
                continue
            if name.lower() == "pubmed":
                continue  # already in bib
            key = name.lower()
            links.setdefault(key, url)
    return links


def first_sentence(text):
    if not text:
        return None
    text = text.strip()
    m = re.search(r"(.+?[.!?])(\s|$)", text)
    return m.group(1).strip() if m else text


def build_overlay(post):
    """Overlay = only fields the bib lacks."""
    overlay = {}
    overlay["featured"] = bool(post.get("featured", False))
    tags = post.get("tags")
    if tags:
        overlay["tags"] = list(tags)
    links = gather_links(post)
    if links:
        overlay["links"] = links
    abstract = post.get("abstract")
    if abstract and str(abstract).strip():
        abstract = str(abstract).strip()
        overlay["highlight"] = first_sentence(abstract)
        overlay["abstract"] = abstract
    return overlay


def assign_pmids(folders, by_doi, by_title, title_of_pmid):
    """Greedy, confidence-first assignment of folders to PMIDs.

    folders: list of (folder_name, post). Returns (assigned, unmatched, notes):
      assigned:  dict pmid -> (folder, method)
      unmatched: list of (folder, title, reason)
      notes:     human-readable lines about overrides / displacements

    Each folder carries a ranked candidate list. We assign the globally
    highest-confidence unclaimed candidate first, so a DOI- or two-signal
    match takes a PMID ahead of a bare URL or title match. A folder whose
    every candidate is already claimed by a stronger folder falls through to
    unmatched (reported, never silently dropped).
    """
    # Build (confidence, folder, pmid, method) claims, strongest first.
    claims = []
    cand_map = {}
    for folder, post in folders:
        cands = candidate_pmids(post, by_doi, by_title, title_of_pmid)
        cand_map[folder] = cands
        for pmid, method, conf in cands:
            claims.append((conf, folder, pmid, method))
    # Strongest confidence first; tie-break deterministically by folder name.
    claims.sort(key=lambda c: (-c[0], c[1]))

    assigned = {}        # pmid -> (folder, method)
    folder_pmid = {}     # folder -> pmid
    notes = []
    for conf, folder, pmid, method in claims:
        if folder in folder_pmid:
            continue
        if pmid in assigned:
            continue
        assigned[pmid] = (folder, method)
        folder_pmid[folder] = pmid

    # Emit override / displacement notes.
    for folder, pmid in folder_pmid.items():
        cands = cand_map[folder]
        url_cand = next((c for c in cands if c[1] in ("url", "url+title")), None)
        if url_cand and url_cand[0] != pmid:
            method = assigned[pmid][1]
            notes.append(
                f"{folder}: used {method} -> {pmid} "
                f"(folder's pubmed url pointed at stale {url_cand[0]})")

    unmatched = []
    for folder, post in folders:
        if folder in folder_pmid:
            continue
        title = post.get("title", "")
        cands = cand_map[folder]
        if cands:
            taken = ", ".join(f"{p} (via {m}) claimed by {assigned[p][0]}"
                              for p, m, _ in cands if p in assigned)
            reason = f"all candidate PMIDs already claimed: {taken}"
        else:
            reason = no_match_reason(post, by_doi)
        unmatched.append((folder, title, reason))

    return assigned, unmatched, notes


def main():
    by_doi, by_title, title_of_pmid = load_bib_index(IN_BIB)
    md_files = sorted(glob.glob(os.path.join(PUB_DIR, "*", "index.md")))

    folders = []
    for path in md_files:
        folder = os.path.basename(os.path.dirname(path))
        folders.append((folder, frontmatter.load(path)))

    assigned, unmatched, notes = assign_pmids(
        folders, by_doi, by_title, title_of_pmid)

    post_by_folder = {f: p for f, p in folders}
    result = {pmid: build_overlay(post_by_folder[folder])
              for pmid, (folder, _method) in assigned.items()}

    # Deterministic order by integer PMID.
    ordered = {pmid: result[pmid] for pmid in sorted(result, key=lambda x: int(x))}

    with open(OUT_YAML, "w", encoding="utf-8") as f:
        yaml.safe_dump(ordered, f, allow_unicode=True, sort_keys=False)

    if notes:
        print("RECONCILED (stale legacy metadata corrected against the bib):")
        for line in sorted(notes):
            print(f"  - {line}")

    if unmatched:
        print("UNMATCHED (could not resolve to a PMID):")
        for folder, title, reason in unmatched:
            print(f"  - {folder}: {title!r} [{reason}]")
    else:
        print("UNMATCHED: none")

    print(f"Seeded {len(ordered)} entries, {len(unmatched)} unmatched")


def _selftest():
    assert PUBMED_RE.search(
        "https://pubmed.ncbi.nlm.nih.gov/37638293/"
    ).group(1) == "37638293", "pmid regex trailing slash"
    assert PUBMED_RE.search(
        "http://www.pubmed.ncbi.nlm.nih.gov/12345"
    ).group(1) == "12345", "pmid regex no slash"
    assert PUBMED_RE.search("https://example.com/foo") is None, "pmid regex no match"
    assert normalize_title("A NIK-IKK module: p27/Kip1.") == "anikikkmodulep27kip1"
    assert normalize_doi(" 10.1/AbC ") == "10.1/abc"
    assert first_sentence("First sentence. Second one.") == "First sentence."

    # --- candidate_pmids: confidence tiers ---
    by_doi = {"10.1/correct": "111"}
    by_title = {normalize_title("Right Paper"): "111",
                normalize_title("Other Paper"): "222"}
    title_of_pmid = {"111": normalize_title("Right Paper"),
                     "222": normalize_title("Other Paper"),
                     "999": normalize_title("Wrong Paper")}

    def post(**kw):
        return kw

    def url(pmid):
        return [{"url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"}]

    # DOI is highest confidence and leads the list.
    c = candidate_pmids(post(title="Right Paper", doi="10.1/correct",
                             links=url("111")), by_doi, by_title, title_of_pmid)
    assert c[0] == ("111", "doi", CONF_DOI), c

    # url whose bib title matches folder title -> url+title tier.
    c = candidate_pmids(post(title="Right Paper", links=url("111")),
                        by_doi, by_title, title_of_pmid)
    assert c[0] == ("111", "url+title", CONF_URL_TITLE), c

    # url whose bib title does NOT match folder title -> plain url tier,
    # and a distinct title match also offered as a lower candidate.
    c = candidate_pmids(post(title="Other Paper", links=url("999")),
                        by_doi, by_title, title_of_pmid)
    assert ("999", "url", CONF_URL) in c and ("222", "title", CONF_TITLE) in c, c
    assert c[0][0] == "999", c  # url outranks title

    # Nothing resolves -> empty candidate list.
    c = candidate_pmids(post(title="Unknown", doi="10.9/missing"),
                        by_doi, by_title, title_of_pmid)
    assert c == [], c

    # --- assign_pmids: collision resolution ---
    # maharjan-style: wrong url (222) collides with a real owner; the loser
    # falls back to its bib title match (own correct PMID 333).
    by_title2 = dict(by_title)
    by_title2[normalize_title("Estrogens Paper")] = "333"
    title_of_pmid2 = dict(title_of_pmid)
    title_of_pmid2["333"] = normalize_title("Estrogens Paper")
    folders = [
        ("owner", post(title="Other Paper", links=url("222"))),   # url+title -> 222
        ("maharjan", post(title="Estrogens Paper", links=url("222"))),  # wrong url
    ]
    assigned, unmatched, notes = assign_pmids(
        folders, by_doi, by_title2, title_of_pmid2)
    assert assigned["222"][0] == "owner", assigned
    assert assigned["333"][0] == "maharjan", assigned
    assert unmatched == [], unmatched

    # baer-style: correct url (222) but WRONG pasted title that matches 111's
    # owner. The owner of 111 keeps it; baer keeps its url 222.
    folders = [
        ("rightowner", post(title="Right Paper", links=url("111"))),  # url+title 111
        ("baer", post(title="Right Paper", links=url("222"))),         # url 222, bad title
    ]
    assigned, unmatched, notes = assign_pmids(
        folders, by_doi, by_title, title_of_pmid)
    assert assigned["111"][0] == "rightowner", assigned
    assert assigned["222"][0] == "baer", assigned
    assert unmatched == [], unmatched

    print("seed_pub_meta self-tests passed")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
        sys.exit(0)
    sys.exit(main())
