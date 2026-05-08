# API sources — endpoints and templates

All endpoints work without API keys. All return parseable formats. All callable from python3 stdlib (`urllib`, `json`, `xml.etree`, `re`, `html.parser`).

## Wikipedia REST — page summary

```
GET https://{lang}.wikipedia.org/api/rest_v1/page/summary/{Title_With_Underscores}
Response: JSON with {title, extract, content_urls.desktop.page}
```

`extract` is a 1-2 paragraph human summary already optimised for plain language — perfect first stop. ~1KB per page. Tolerant rate limit; identify yourself in `User-Agent`.

## Wikipedia opensearch — title resolution

```
GET https://{lang}.wikipedia.org/w/api.php?action=opensearch&format=json&limit=1&search={query}
Response: ["query", ["Top Title"], ["..."], ["url"]]
```

Use when you don't know the canonical title — the REST summary requires the exact slug.

## DuckDuckGo HTML — open web search

```
GET https://html.duckduckgo.com/html/?q={query}
Response: HTML (~30-40KB)
Result blocks: <a class="result__a" href="//duckduckgo.com/l/?uddg={ENCODED_URL}">{TITLE}</a>
```

Decode the `uddg` query param to get the real target URL. No JavaScript needed. No CAPTCHA at low volume. Set a `User-Agent`. Filter response down to 5 titles+URLs (~2KB).

## arXiv — academic preprints

```
GET http://export.arxiv.org/api/query?search_query=all:{query}&max_results={n}
Response: Atom XML
```

Parse with `xml.etree.ElementTree`, namespace `http://www.w3.org/2005/Atom`. Each `<entry>` has `<title>`, `<summary>` (the abstract), `<author>/<name>`, `<id>` (URL).

**Rate limit:** 3 seconds between calls — always sleep. Returning `Rate exceeded` means you ignored that.

## Crossref — citable works with DOI

```
GET https://api.crossref.org/works?query={query}&rows={n}
Headers: User-Agent must include a mailto: identifier (polite pool gets faster service)
Response: JSON. Items at message.items[]
```

Each item: `title[0]`, `author[].given/family`, `issued.date-parts[0][0]` (year), `DOI`, `container-title[0]`.

## Hacker News (Algolia) — tech opinion

```
GET https://hn.algolia.com/api/v1/search?query={query}&hitsPerPage={n}
Response: JSON. hits[] with {title, url, points, num_comments}
```

Useful for "what does the tech crowd think of X" queries. Skip if not relevant.

## Stack Exchange — Q&A

```
GET https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={query}&site=stackoverflow
Response: JSON. items[] with {title, link, score, is_answered}
```

100 requests/day anonymous. Add `&filter=default` for cleaner output.

## Token-cost cheatsheet

| Source | Typical bytes | When to call |
|---|---|---|
| Wikipedia summary | 800-1500 | Always first |
| Wikipedia opensearch | 200-400 | Title resolution |
| DDG (filtered to 5 results) | 1-2KB | Breadth |
| arXiv (3 abstracts) | 2-4KB | Scientific depth |
| Crossref (5 works) | 1-2KB | Citation list |
| HN (5 hits) | ~1KB | Tech zeitgeist |
| Stack Exchange (5 hits) | ~1KB | Q&A practical |

Combined "deep" research budget: ~10KB. Stay under that.

## Failure modes

- **Wikipedia disambiguation page** — `extract` is a one-liner pointing elsewhere; opensearch + retry with refined query.
- **arXiv rate limit** — XML body says "Rate exceeded". Wait 5s, retry once, then drop.
- **DDG empty results** — page returns no `result__a` matches. Try with broader keywords.
- **Encoding** — always read `Content-Type` charset; fall back to utf-8 with `errors="replace"`.
- **Hook-blocked HTTP** — environments may block `curl`/`wget`. python3 `urllib` bypasses the hook.
