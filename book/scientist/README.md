# scientist

Research and explainer skills — for when you want sourced facts, multi-source synthesis, and explanations in plain language. Inspired by Richard Feynman's pedagogy: *if you can't explain it simply, you don't understand it*.

## Skills

- **[feynman-search](./feynman-search/SKILL.md)** — Token-efficient web research using only python3 stdlib (`urllib`, `html.parser`, `json`, `re`). Translates the user's query to English first (more sources), pulls from Wikipedia, DuckDuckGo, arXiv, and Crossref, then synthesises findings in Feynman's 4-step style: TL;DR, lay analogy with one aha moment, technical depth, sources + open gaps. For dense academic content, asks whether to translate source quotes or keep originals. Output lands at `<cwd>/.feynman-searchs/`, auto-gitignored if cwd is a git repo.
