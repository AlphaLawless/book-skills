#!/usr/bin/env python3
"""Wikipedia REST summary fetcher.

Usage: wiki.py <title-or-query> [--lang en|pt]
Output: JSON with {title, extract, url, lang} or {error}.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request

UA = "feynman-search/0.1 (+https://github.com/AlphaLawless/skills)"


def http_get(url: str, timeout: float = 8.0) -> bytes:
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def opensearch(query: str, lang: str) -> str | None:
    url = (
        f"https://{lang}.wikipedia.org/w/api.php?action=opensearch"
        f"&format=json&limit=1&search={urllib.parse.quote(query)}"
    )
    data = json.loads(http_get(url))
    if isinstance(data, list) and len(data) >= 2 and data[1]:
        return data[1][0].replace(" ", "_")
    return None


def summary(title: str, lang: str) -> dict:
    url = (
        f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/"
        f"{urllib.parse.quote(title)}"
    )
    data = json.loads(http_get(url))
    return {
        "title": data.get("title", title),
        "extract": data.get("extract", ""),
        "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
        "lang": lang,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--lang", default="en")
    args = p.parse_args()

    try:
        # Direct title first; fall back to opensearch.
        try:
            result = summary(args.query.replace(" ", "_"), args.lang)
            if not result["extract"]:
                raise ValueError("empty extract")
        except Exception:
            title = opensearch(args.query, args.lang)
            if not title:
                print(json.dumps({"error": "no match"}))
                return 1
            result = summary(title, args.lang)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
