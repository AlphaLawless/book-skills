#!/usr/bin/env python3
"""Crossref REST API query -> JSON of citable papers.

Usage: crossref.py <query> [--max 5]
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request

# Crossref's "polite pool" recommends a mailto identifier in User-Agent.
UA = "feynman-search/0.1 (mailto:alpha.dlawless@gmail.com)"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--max", type=int, default=5)
    args = p.parse_args()

    url = (
        "https://api.crossref.org/works"
        f"?query={urllib.parse.quote(args.query)}&rows={args.max}"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
    except Exception as e:
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
        return 1

    works = []
    for item in data.get("message", {}).get("items", []):
        title = (item.get("title") or [""])[0]
        authors = [
            f"{a.get('given','')} {a.get('family','')}".strip()
            for a in item.get("author", [])
        ][:3]
        date_parts = item.get("issued", {}).get("date-parts", [[None]])
        year = (date_parts[0] or [None])[0] if date_parts else None
        works.append(
            {
                "title": title,
                "authors": authors,
                "year": year,
                "doi": item.get("DOI", ""),
                "container": (item.get("container-title") or [""])[0],
            }
        )
    print(json.dumps({"works": works}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
