# poupa-time

Time-saver skills — meta-tools that scaffold new skills, configs, and project setup. Anything that lets you start the real work faster.

## Skills

- **[touch-skill](./touch-skill/SKILL.md)** — Create new agent skills following Anthropic best practices. Pure-instruction style (no scaffold script): the SKILL.md teaches Claude to validate the name, create folder + symlink, and write `SKILL.md` from a template. Used to author every other skill in this repo.

- **[touch-claude](./touch-claude/SKILL.md)** — Bootstrap a vendored `agent-md` template into a project. Self-contained — no network at runtime, no `install.sh`, all 17 files audited and copied locally. Lean for Claude Code only: 6 hooks (verify gate, progress enforcement, edit-time lint, TDD nudge, UI sensory reminder, playwright capture) + 5 `memory/` files seeded with personal CLAUDE.md v3 directives.
