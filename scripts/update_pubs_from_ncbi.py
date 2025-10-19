#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch all PMIDs from a public MyNCBI bibliography (paginated),
then retrieve PubMed records via E-utilities and write BibTeX.
Preprints (bioRxiv/medRxiv/arXiv) are excluded.
"""

import os
import re
import time
import sys
import html
import logging
from typing import List, Set, Dict

import requests
from Bio import Entrez
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

# ------------------ Config ------------------

MYNCBI_PUBLIC_URL = "https://www.ncbi.nlm.nih.gov/myncbi/1FKxdfRDEdusri/bibliography/public/"
OUT_BIB = "data/pubs.bib"

# polite scraping
HEADERS = {
    "User-Agent": "ncborcherding-pubs-updater/1.0 (+https://www.borch.dev)"
}

# NCBI E-utilities
Entrez.email = os.getenv("ENTREZ_EMAIL", "actions@github.com")
API_KEY = os.getenv("NCBI_API_KEY", "").strip()
if API_KEY:
    Entrez.api_key = API_KEY

REQUEST_DELAY = float(os.getenv("NCBI_DELAY", "0.34"))  # <= 3 req/sec
RETRY_MAX = 3
TIMEOUT = 20

# preprint patterns (journals or source strings)
PREPRINT_RX = re.compile(r"\b(biorxiv|medrxiv|arxiv)\b", re.I)

# PMID regex targets: anchor hrefs like /pubmed/12345678, data-attributes, etc.
PMID_RX = re.compile(r"/pubmed/(\d{5,9})|data-pid=[\"'](\d{5,9})[\"']", re.I)

# --------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stdout,
)


def http_get(url: str, params: Dict = None) -> requests.Response:
    for attempt in range(1, RETRY_MAX + 1):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            return r
        except Exception as e:
            if attempt == RETRY_MAX:
                raise
            time.sleep(1.0 * attempt)
    # unreachable
    return None  # type: ignore


def collect_pmids_from_myncbi(base_url: str) -> List[str]:
    """
    Paginate ?page=1..N and collect all PMIDs present in the public bibliography.
    Stops when a page yields no *new* PMIDs.
    """
    pmids: List[str] = []
    seen: Set[str] = set()

    page = 1
    logging.info("Fetching PMIDs from public MyNCBI bibliography…")
    while True:
        params = {"page": page}
        r = http_get(base_url, params=params)
        html_text = r.text

        # Find PMIDs on the page
        found: Set[str] = set()
        for m in PMID_RX.finditer(html_text):
            pid = m.group(1) or m.group(2)
            if pid:
                found.add(pid)

        new_on_page = [p for p in found if p not in seen]

        logging.info(f"Page {page}: found {len(found)} PMIDs, new {len(new_on_page)}")

        if not new_on_page:
            # If no new PMIDs and we've already gathered some, break.
            # This handles last page (and also the edge case where the first page has none).
            break

        pmids.extend(new_on_page)
        seen.update(new_on_page)

        page += 1
        time.sleep(0.5)  # be polite to NCBI web

    logging.info(f"Found {len(pmids)} total PMIDs")
    return pmids


def fetch_pubmed_xml(pmids: List[str]) -> List[dict]:
    """
    Fetch PubMed records via efetch in batches.
    """
    if not pmids:
        return []

    BATCH = 200
    records = []
    logging.info("Fetching PubMed XML via E-utilities…")

    for i in range(0, len(pmids), BATCH):
        chunk = pmids[i:i + BATCH]
        # Respect rate limits
        time.sleep(REQUEST_DELAY)
        for attempt in range(1, RETRY_MAX + 1):
            try:
                with Entrez.efetch(db="pubmed", id=",".join(chunk), retmode="xml") as handle:
                    data = Entrez.read(handle)
                # 'PubmedArticle' list
                recs = data.get("PubmedArticle", [])
                logging.info(f"Fetched {len(recs)} records (batch {i//BATCH + 1})")
                records.extend(recs)
                break
            except Exception as e:
                if attempt == RETRY_MAX:
                    logging.error(f"Failed efetch for batch starting at {i}: {e}")
                time.sleep(1.0 * attempt)

    return records


def is_preprint(pub: dict) -> bool:
    """
    Return True if the record appears to be a preprint (bioRxiv/medRxiv/arXiv).
    Check Journal/Source fields, ELocationID, and CommentsCorrections if present.
    """
    try:
        art = pub["MedlineCitation"]["Article"]
        journal = (art.get("Journal", {}).get("Title") or "").lower()
        if PREPRINT_RX.search(journal):
            return True

        # Some preprints carry 'PubmedData' -> 'ArticleIdList' with DOI domain hints.
        pubdata = pub.get("PubmedData", {})
        for aid in pubdata.get("ArticleIdList", []):
            if isinstance(aid, dict):
                val = (aid.get("_") or "").lower()
                if PREPRINT_RX.search(val):
                    return True

        # Also scan 'ArticleTitle' just in case:
        title = (art.get("ArticleTitle") or "")
        if isinstance(title, bytes):
            title = title.decode("utf-8", "ignore")
        if PREPRINT_RX.search(title):
            return True

    except Exception:
        pass
    return False


def pub_to_bib_entry(pub: dict) -> Dict:
    """
    Convert a PubMed XML record to a BibTeX dict that bibtexparser can write.
    """
    med = pub.get("MedlineCitation", {})
    art = med.get("Article", {})
    jnl = art.get("Journal", {})

    # PMID
    pmid = med.get("PMID", "")
    if isinstance(pmid, dict):
        pmid = pmid.get("_", "")

    # Title
    title = art.get("ArticleTitle", "")
    if isinstance(title, bytes):
        title = title.decode("utf-8", "ignore")
    # Unescape HTML entities and enforce utf-8 safe
    title = html.unescape(title)
    title = title.encode("utf-8", "ignore").decode()

    # Authors
    authors_list = []
    for a in art.get("AuthorList", []):
        if "LastName" in a and "ForeName" in a:
            authors_list.append(f"{a['LastName']}, {a['ForeName']}")
        elif "CollectiveName" in a:
            authors_list.append(a["CollectiveName"])
    authors = " and ".join(authors_list)

    # Journal & year
    journal_title = jnl.get("Title", "")
    year = ""
    try:
        year = jnl.get("JournalIssue", {}).get("PubDate", {}).get("Year", "")
        if not year:
            # Sometimes it's like "2020 Jan"
            med_date = jnl.get("JournalIssue", {}).get("PubDate", {}).get("MedlineDate", "")
            if med_date:
                year = re.findall(r"\d{4}", med_date)[0]
    except Exception:
        pass

    # Volume/issue/pages
    volume = jnl.get("JournalIssue", {}).get("Volume", "")
    number = jnl.get("JournalIssue", {}).get("Issue", "")
    pages = art.get("Pagination", {}).get("MedlinePgn", "")

    # DOI if available
    doi = ""
    for aid in pub.get("PubmedData", {}).get("ArticleIdList", []):
        if isinstance(aid, dict) and aid.get("IdType", "").lower() == "doi":
            doi = aid.get("_", "")

    # BibTeX entry key
    key = f"PMID{pmid}" if pmid else f"ref{hash(title) & 0xffffffff}"

    entry = {
        "ENTRYTYPE": "article",
        "ID": key,
        "title": title,
        "author": authors,
        "journal": journal_title,
        "year": str(year) if year else "",
        "volume": volume or "",
        "number": number or "",
        "pages": pages or "",
        "pmid": pmid or "",
    }
    if doi:
        entry["doi"] = doi

    return entry


def write_bib(entries: List[Dict], out_path: str):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    db = BibDatabase()
    db.entries = entries

    writer = BibTexWriter()
    writer.indent = "  "
    writer.comma_first = False
    writer.order_entries_by = ("year", "author", "title")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(writer.write(db))


def main():
    pmids = collect_pmids_from_myncbi(MYNCBI_PUBLIC_URL)
    if not pmids:
        logging.info("No PMIDs found; nothing to do.")
        return

    # Fetch PubMed XML
    pubs = fetch_pubmed_xml(pmids)

    # Filter out preprints
    filtered = [p for p in pubs if not is_preprint(p)]
    logging.info(f"Keeping {len(filtered)} after excluding preprints")

    # Convert to BibTeX entries
    entries = [pub_to_bib_entry(p) for p in filtered]

    # Sort newest first
    def year_int(e):
        try:
            return int(e.get("year", "0") or "0")
        except Exception:
            return 0

    entries.sort(key=year_int, reverse=True)

    # Write bib
    write_bib(entries, OUT_BIB)
    logging.info(f"Wrote {OUT_BIB}")


if __name__ == "__main__":
    main()
