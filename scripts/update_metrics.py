#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refresh data/metrics.yaml for the homepage "at a glance" band.

Pulls citation count + h-index from the public Google Scholar profile and the
star count for scRepertoire from the GitHub API. Google Scholar has no official
API and blocks aggressively, so this is best-effort: on any failure we KEEP the
previously committed value rather than overwrite it with zeros.

Publication count is NOT stored here - the site computes it live from
data/publications.yaml so it can never drift.
"""

import os
import re
import sys
import datetime
import logging

import requests
import yaml

SCHOLAR_USER = os.getenv("SCHOLAR_USER", "_n4TRuIAAAAJ")
GITHUB_REPO = os.getenv("METRICS_GH_REPO", "BorchLab/scRepertoire")
OUT = "data/metrics.yaml"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")

logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)


def load_existing() -> dict:
    try:
        with open(OUT, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def fetch_scholar():
    """Return (citations:int, h_index:int, i10:int) or None on failure."""
    url = f"https://scholar.google.com/citations?user={SCHOLAR_USER}&hl=en"
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=20)
        if r.status_code != 200 or "gsc_rsb_std" not in r.text:
            logging.warning(f"Scholar returned {r.status_code} or no stats table")
            return None
        cells = re.findall(r'gsc_rsb_std">([\d,]+)<', r.text)
        if len(cells) < 3:
            logging.warning("Scholar stats table incomplete")
            return None
        nums = [int(c.replace(",", "")) for c in cells]
        # Order: citations(all,since), h-index(all,since), i10(all,since)
        return nums[0], nums[2], (nums[4] if len(nums) > 4 else 0)
    except Exception as e:
        logging.warning(f"Scholar fetch failed: {e}")
        return None


def fetch_github_stars(repo: str):
    """Return star count int, or None on failure."""
    try:
        headers = {"Accept": "application/vnd.github+json", "User-Agent": UA}
        token = os.getenv("GITHUB_TOKEN", "").strip()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        r = requests.get(f"https://api.github.com/repos/{repo}", headers=headers, timeout=20)
        if r.status_code != 200:
            logging.warning(f"GitHub returned {r.status_code} for {repo}")
            return None
        return int(r.json().get("stargazers_count"))
    except Exception as e:
        logging.warning(f"GitHub fetch failed: {e}")
        return None


def main():
    data = load_existing()

    scholar = fetch_scholar()
    if scholar:
        citations, h_index, i10 = scholar
        data["citations"] = citations
        data["citations_display"] = f"{citations:,}"
        data["h_index"] = h_index
        data["i10_index"] = i10
        logging.info(f"Scholar: {citations} citations, h-index {h_index}")
    else:
        logging.info("Keeping previous Scholar values")

    stars = fetch_github_stars(GITHUB_REPO)
    if stars is not None:
        data["screpertoire_stars"] = stars
        logging.info(f"scRepertoire stars: {stars}")
    else:
        logging.info("Keeping previous star count")

    data["updated"] = datetime.date.today().isoformat()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=True)
    logging.info(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
