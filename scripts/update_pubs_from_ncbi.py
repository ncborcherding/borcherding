#!/usr/bin/env python3
"""
Pull PMIDs from a PUBLIC MyNCBI bibliography page, fetch PubMed metadata via
NCBI E-utilities, and write data/pubs.bib for Quarto, EXCLUDING preprints
(e.g., bioRxiv/medRxiv) automatically.

Requires: biopython, bibtexparser, requests
  pip install biopython bibtexparser requests
"""
import os, re, time, html, requests
from urllib.parse import urljoin
from typing import List, Dict
from Bio import Entrez
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

MYNCBI_PUBLIC_URL = "https://www.ncbi.nlm.nih.gov/myncbi/1FKxdfRDEdusri/bibliography/public/"  # <-- your public page
EMAIL_FOR_NCBI    = "borcherding.n@wustl.edu"  # NCBI asks for a contact email
NCBI_API_KEY      = os.getenv("NCBI_API_KEY", "")  # optional but recommended

# Journals/venues to exclude (case-insensitive)
EXCLUDED_VENUES_RE = re.compile(r"(?:^|\b)(bioRxiv|medRxiv)(?:\b|$)", re.IGNORECASE)

# ---- Helpers ----------------------------------------------------------------
def get_pmids_from_page(url: str) -> (List[str], str | None):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    text = r.text
    pmids = re.findall(r"PubMed PMID:\s*(\d+)", text)
    next_url = None
    m = re.search(r'href="([^"]+)"[^>]*>\s*Next page\s*<', text)
    if m:
        href = html.unescape(m.group(1))
        next_url = urljoin(url, href)
    return pmids, next_url

def crawl_all_pmids(start_url: str) -> List[str]:
    all_pmids, seen_pages = [], set()
    url = start_url
    while url and url not in seen_pages:
        seen_pages.add(url)
        pmids, next_url = get_pmids_from_page(url)
        all_pmids.extend(pmids)
        url = next_url
    # de-dup while preserving order
    deduped, seen = [], set()
    for p in all_pmids:
        if p not in seen:
            seen.add(p); deduped.append(p)
    return deduped

def chunked(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

def pubmed_xml_for_pmids(pmids: List[str]):
    Entrez.email = EMAIL_FOR_NCBI
    if NCBI_API_KEY:
        Entrez.api_key = NCBI_API_KEY
    out = []
    for batch in chunked(pmids, 200):
        handle = Entrez.efetch(db="pubmed", id=",".join(batch), retmode="xml")
        data = Entrez.read(handle)
        handle.close()
        out.extend(data.get("PubmedArticle", []))
        time.sleep(0.34)  # be gentle with NCBI
    return out

def is_preprint(article) -> bool:
    """Return True if the PubMed record is a preprint we should exclude."""
    # Journal/venue title check
    art = article.get("MedlineCitation", {}).get("Article", {})
    journal = art.get("Journal", {}) or {}
    journal_title = (journal.get("Title") or
                     journal.get("ISOAbbreviation") or "")
    if EXCLUDED_VENUES_RE.search(journal_title or ""):
        return True

    # Publication type check (e.g., 'Preprint')
    pub_types = art.get("PublicationTypeList", [])
    for pt in pub_types:
        if str(pt).strip().lower() == "preprint":
            return True

    # Safety: sometimes title strings include 'bioRxiv'/'medRxiv'
    title = str(art.get("ArticleTitle", "")).strip()
    if EXCLUDED_VENUES_RE.search(title):
        return True

    return False

def to_bib_entry(article) -> Dict:
    """Convert a PubmedArticle to a BibTeX entry."""
    art = article["MedlineCitation"]["Article"]
    journal = art.get("Journal", {})
    jinfo = journal.get("JournalIssue", {})
    artids = article.get("PubmedData", {}).get("ArticleIdList", [])
    pmid = article["MedlineCitation"]["PMID"]

    title = str(art.get("ArticleTitle", "")).rstrip(".")
    pubdate = jinfo.get("PubDate", {}) or {}
    year = pubdate.get("Year") or (pubdate.get("MedlineDate", "")[:4] if pubdate.get("MedlineDate") else "")
    authors = []
    for a in art.get("AuthorList", []):
        last = a.get("LastName") or ""
        fore = a.get("ForeName") or a.get("Initials") or ""
        if last or fore:
            authors.append(f"{fore} {last}".strip())
    authors_str = " and ".join(authors)
    journal_title = journal.get("Title") or journal.get("ISOAbbreviation") or ""
    volume = jinfo.get("Volume", "")
    issue  = jinfo.get("Issue", "")
    pages  = art.get("Pagination", {}).get("MedlinePgn", "")
    doi    = ""
    url    = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    for aid in artids:
        if aid.attributes.get("IdType") == "doi":
            doi = str(aid); break

    entry = {
        "ENTRYTYPE": "article",
        "ID": re.sub(r"[^A-Za-z0-9]+", "", (title[:40] + str(year))) or f"pmid{pmid}",
        "title": title,
        "author": authors_str,
        "year": str(year),
        "journal": journal_title,
        "volume": volume,
        "number": issue,
        "pages": pages,
        "url": url,
        "pmid": str(pmid),
    }
    if doi:
        entry["doi"] = doi
    return entry

def write_bib(entries: List[Dict], path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    db = BibDatabase(); db.entries = entries
    writer = BibTexWriter(); writer.order_entries_by = ("year", )
    with open(path, "w", encoding="utf-8") as f:
        f.write(writer.write(db))

def main():
    print("Fetching PMIDs from public MyNCBI bibliography…")
    pmids = crawl_all_pmids(MYNCBI_PUBLIC_URL)
    print(f"Found {len(pmids)} PMIDs")
    if not pmids:
        return

    print("Fetching PubMed XML via E-utilities…")
    articles = pubmed_xml_for_pmids(pmids)
    print(f"Fetched {len(articles)} records")

    # FILTER OUT PREPRINTS
    filtered = [a for a in articles if not is_preprint(a)]
    print(f"Keeping {len(filtered)} after excluding preprints")

    # Convert to BibTeX and sort newest first
    bib_entries = [to_bib_entry(a) for a in filtered]
    bib_entries = sorted(bib_entries, key=lambda e: (e.get("year",""), e.get("title","")), reverse=True)
    write_bib(bib_entries, "data/pubs.bib")
    print("Wrote data/pubs.bib")

if __name__ == "__main__":
    main()
