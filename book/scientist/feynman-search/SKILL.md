---
name: feynman-search
description: Token-efficient web research using only python3 stdlib (urllib, html.parser, json, re). Translates the user's query to English first (more sources available), then pulls from Wikipedia, DuckDuckGo HTML, arXiv, and Crossref, and synthesises findings in Feynman's 4-step style — TL;DR, lay analogy, technical depth, sources + open gaps. For dense/academic content, asks the user whether to translate source quotes or keep them in original language. Output lands at `<cwd>/.feynman-searchs/research-<slug>.md`, auto-gitignored if cwd is a git repo. Use when the user wants to research, search, look up, or explain a topic — triggers on "pesquisar", "search", "research", "explica como Feynman", "ELI5", "explique pra leigo", "find papers on", "look up", "investigate".
---

# feynman-search

Research engine that fetches from trusted sources via python3 stdlib (zero deps) and presents findings in Richard Feynman's pedagogy: *if you can't explain it simply, you don't understand it*.

**Default behaviour:** translate the query to English (more content available), search EN across Wikipedia / DDG / arXiv / Crossref, synthesise the answer in the user's original language, write the note to `<cwd>/.feynman-searchs/research-<slug>.md`. If `<cwd>` is a git repo, `.feynman-searchs/` is appended to `.gitignore` automatically.

## Quick start

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-/home/alpha/.claude/skills/feynman-search}"
python3 "$SKILL_DIR/scripts/search.py" "dynamic programming" --backends wiki,ddg,arxiv,crossref
```

The note lands at `<cwd>/.feynman-searchs/research-dynamic-programming.md`. Pass `--out <path>` to override.

## Workflow

```
- [ ] 1. Parse user query — detect intent + language + depth (lay vs academic)
- [ ] 2. Translate query to English (the actual search keyword) before invoking backends
- [ ] 3. Decide backends — Wikipedia always; arXiv/Crossref if scientific; DDG for breadth
- [ ] 4. Fetch via search.py with the EN keyword (writes ranked snippets, ~2-5KB)
- [ ] 5. For academic content (arxiv or crossref present), ASK user: keep source quotes in original language or translate?
- [ ] 6. Synthesise in user's original language using the gathered sources
- [ ] 7. Note lands at <cwd>/.feynman-searchs/; return inline TL;DR (3 lines) + path
```

### Step 1 — Parse

Detect:

- **Language:** PT-BR markers like "como", "pesquisar", "explique" → user wants output in PT.
- **Depth:** "papers on X", "recent research", author names → academic. "what is X", "explain X" → lay.
- **Comparison:** "X vs Y" → multi-source synthesis.

### Step 2 — Translate query to English

The **single most load-bearing step**. Most authoritative content (Wikipedia titles, arXiv keywords, Crossref title-search, top web pages) is in English. A verbose query like `"como funciona programação dinâmica"` sent verbatim:

- `wiki.py opensearch` returns nothing — it's not a Wikipedia title
- `arxiv.py` times out or returns noise — keyword soup
- only `fetch.py ddg` survives because DDG tolerates natural language

Strip the question prefix and translate the topic to its canonical English term:

| User query (PT) | Translated (EN) for backends |
|---|---|
| "como funciona programação dinâmica" | `dynamic programming` |
| "o que é entropia em sistemas distribuídos" | `entropy distributed systems` |
| "explique emaranhamento quântico" | `quantum entanglement` |
| "papers de Donald Knuth" | `Donald Knuth literate programming` |
| "what is the Feynman technique" | `Feynman technique` (already EN, just strip prefix) |

If the topic is rare or has no obvious English equivalent, ask the user before translating.

### Step 3 — Backend strategy

| Query type | Backends | Why |
|---|---|---|
| Lay/general | wiki + ddg | Wikipedia for facts; DDG for diversity |
| Scientific | wiki + arxiv + crossref | Abstracts + citable DOIs |
| Author/work | wiki + crossref | Wikipedia bio + citable papers |
| Quick fact | wiki only | Fastest, cleanest |

See `references/api-sources.md` for endpoints, rate limits, URL templates.

### Step 4 — Fetch

```bash
python3 scripts/search.py "<en-translated-query>" \
  --backends wiki,ddg,arxiv,crossref \
  --max-results 5 \
  --lang auto
```

`--lang` controls Wikipedia language (auto-detects PT when PT markers were in the user's *original* query, even though search uses EN). Each backend script (`wiki.py`, `arxiv.py`, `crossref.py`, `fetch.py`) is callable standalone.

### Step 5 — Source language prompt (academic only)

If `arxiv.papers` or `crossref.works` came back non-empty, sources are dense English academic text. **Ask the user**:

> *"As fontes acadêmicas (arXiv/Crossref) vieram em inglês. Prefere que eu traduza as citações pra português na síntese, ou mantenho na língua original?"*

Default if user doesn't reply or said "tanto faz": keep original-language quotes, write the Feynman synthesis in user's language. Preserves source fidelity while staying readable.

Skip this step for non-academic queries (only `wiki` + `ddg`) — Wikipedia PT branch already serves PT content directly.

### Step 6 — Synthesise (Feynman 4-step)

Apply the technique from `references/feynman-method.md`:

1. **TL;DR (3 lines)** — what it is, in plain words
2. **Layered explanation** — analogy a 12-year-old would get; reveal *one* aha moment
3. **Technical depth (optional)** — the precise definition; what makes it non-trivial
4. **Sources + open questions** — list with reliability tags; gaps in the explanation

Write the synthesis in the user's **original** language. Read `references/feynman-method.md` for worked translations and `references/teachers-canon.md` for pedagogy notes from Lewin, Sagan, Knuth, Hofstadter, Tao, and Bret Victor.

### Step 7 — Write note + return inline

The scaffold note is at `<cwd>/.feynman-searchs/research-<slug>.md`. Read it, overwrite with the full synthesis. Inline reply: 3-line TL;DR + file path.

If `<cwd>` is a git repo, `.feynman-searchs/` is auto-added to `.gitignore` on first run (idempotent — won't duplicate the line).

## When to invoke

User says any of: "pesquisar X", "search X", "research X", "explique X como Feynman", "ELI5 X", "find papers on X", "investigate X", "what's the science behind X". Or when a topic explanation needs sources, not just model knowledge.

## Token budget

| Step | Cost |
|---|---|
| Wikipedia summary | ~1KB |
| DDG top-5 titles+URLs | ~2KB |
| arXiv 3 abstracts | ~3KB |
| Crossref 5 papers | ~2KB |
| Synthesised note | written to file (0 inline) |
| Inline TL;DR | ~300B |

Worst case: ~10KB into context for deep research; ~1KB for a quick fact.

## Constraints

- **Stdlib only.** `curl`/`wget` are blocked by hooks in some environments. Always use `urllib`, never shell out for HTTP.
- **No API keys required** — all sources work anonymously.
- **Rate limits:** arXiv asks 3s between requests; Wikipedia REST tolerant. Don't loop without backoff.
- **Slug normalises Unicode.** Accents are stripped (NFKD) before slug → "programação" becomes "programacao".

## References

- [`references/feynman-method.md`](references/feynman-method.md) — the 4-step technique with worked translations
- [`references/teachers-canon.md`](references/teachers-canon.md) — Lewin, Sagan, Knuth, Hofstadter, Tao, Victor — pedagogical core
- [`references/api-sources.md`](references/api-sources.md) — endpoint table, URL templates, rate limits
- [`assets/note-template.md`](assets/note-template.md) — output structure
