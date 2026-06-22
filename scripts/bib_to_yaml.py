#!/usr/bin/env python3
"""Convert data/pubs.bib -> data/publications.yaml for the Hugo site.
One source of truth shared with the CV. Run in CI after the NCBI update."""
import re, sys, yaml, bibtexparser

IN_BIB = "data/pubs.bib"
OUT_YAML = "data/publications.yaml"


def split_authors(field):
    out = []
    for a in field.split(" and "):
        a = a.strip()
        if "," in a:
            last, first = [p.strip() for p in a.split(",", 1)]
            out.append(f"{first} {last}".strip())
        else:
            out.append(a)
    return out


def main():
    with open(IN_BIB, encoding="utf-8") as f:
        db = bibtexparser.load(f)
    entries = []
    for e in db.entries:
        pmid = e.get("pmid", "").strip()
        entries.append({
            "key": e.get("ID"),
            "pmid": pmid,
            "title": re.sub(r"[{}]", "", e.get("title", "")).strip().rstrip("."),
            "authors": split_authors(e.get("author", "")),
            "journal": re.sub(r"[{}]", "", e.get("journal", "")).strip(),
            "year": int(e["year"]) if e.get("year", "").isdigit() else None,
            "volume": e.get("volume", ""),
            "number": e.get("number", ""),
            "pages": e.get("pages", ""),
            "doi": e.get("doi", "").strip(),
            "pubmed": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
            "abstract": re.sub(r"\s+", " ", e.get("abstract", "")).strip(),
        })
    entries.sort(key=lambda x: (x["year"] or 0), reverse=True)
    with open(OUT_YAML, "w", encoding="utf-8") as f:
        yaml.safe_dump({"publications": entries}, f, allow_unicode=True, sort_keys=False)
    print(f"Wrote {len(entries)} publications to {OUT_YAML}")


def _selftest():
    assert split_authors("Zhang, Weizhou and Borcherding, Nicholas") == \
        ["Weizhou Zhang", "Nicholas Borcherding"], "split_authors basic"
    # already "First Last" with no comma passes through unchanged
    assert split_authors("admin") == ["admin"], "split_authors no-comma"
    # extra whitespace around the separator and parts
    assert split_authors("Doe ,  Jane ") == ["Jane Doe"], "split_authors whitespace"
    print("bib_to_yaml self-tests passed")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
        sys.exit(0)
    sys.exit(main())
