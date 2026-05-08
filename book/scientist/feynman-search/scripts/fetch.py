#!/usr/bin/env python3
"""Fetch + clean text. Two modes: ddg (search), url (single page).

Usage:
  fetch.py ddg "<query>" [--max 5]      # DuckDuckGo HTML scrape
  fetch.py url "<url>" [--chars 2000]   # Cleaned plain text
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; feynman-search/0.1)"


def http_get(url: str, timeout: float = 10.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        ctype = r.headers.get("Content-Type", "")
        m = re.search(r"charset=([\w-]+)", ctype)
        enc = m.group(1) if m else "utf-8"
        return raw.decode(enc, errors="replace")


class TextOnly(HTMLParser):
    """Strips tags + drops noisy regions (script/style/nav/footer/aside/form)."""

    SKIP = {"script", "style", "noscript", "head", "nav", "footer", "aside", "form"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.skip_depth == 0 and data.strip():
            self.parts.append(data.strip())


def clean_text(html_doc: str, char_limit: int) -> str:
    p = TextOnly()
    p.feed(html_doc)
    text = re.sub(r"\s+", " ", " ".join(p.parts))
    return text[:char_limit]


def ddg_search(query: str, max_n: int) -> dict:
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    page = http_get(url)
    # DDG result block: <a class="result__a" href="//duckduckgo.com/l/?uddg=...">title</a>
    pairs = re.findall(
        r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        page,
        re.DOTALL,
    )
    results = []
    for href, raw_title in pairs[:max_n]:
        m = re.search(r"uddg=([^&]+)", href)
        target = urllib.parse.unquote(m.group(1)) if m else href
        title = re.sub(r"<[^>]+>", "", raw_title)
        title = html.unescape(title).strip()
        results.append({"title": title, "url": target})
    return {"results": results, "count": len(results)}


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)

    s_ddg = sub.add_parser("ddg")
    s_ddg.add_argument("query")
    s_ddg.add_argument("--max", type=int, default=5)

    s_url = sub.add_parser("url")
    s_url.add_argument("url")
    s_url.add_argument("--chars", type=int, default=2000)

    args = p.parse_args()

    try:
        if args.mode == "ddg":
            print(json.dumps(ddg_search(args.query, args.max), ensure_ascii=False))
        elif args.mode == "url":
            text = clean_text(http_get(args.url), args.chars)
            print(json.dumps(
                {"url": args.url, "text": text, "chars": len(text)},
                ensure_ascii=False,
            ))
        return 0
    except Exception as e:
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
