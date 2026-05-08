#!/usr/bin/env python3
"""arXiv API query -> JSON list of abstracts.

Usage: arxiv.py <query> [--max 5]
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
UA = "feynman-search/0.1"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--max", type=int, default=5)
    args = p.parse_args()

    url = (
        "http://export.arxiv.org/api/query"
        f"?search_query=all:{urllib.parse.quote(args.query)}"
        f"&max_results={args.max}"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=10) as r:
            xml = r.read()
    except Exception as e:
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
        return 1

    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        print(json.dumps({"error": f"xml: {e}"}))
        return 1

    papers = []
    for entry in root.findall("a:entry", NS):
        title = (entry.findtext("a:title", "", NS) or "").strip().replace("\n", " ")
        summary = (entry.findtext("a:summary", "", NS) or "").strip().replace("\n", " ")
        link = entry.findtext("a:id", "", NS) or ""
        authors = [a.findtext("a:name", "", NS) or "" for a in entry.findall("a:author", NS)]
        papers.append(
            {"title": title, "authors": authors, "summary": summary[:600], "url": link}
        )
    print(json.dumps({"papers": papers}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
