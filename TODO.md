# TODO

Pending decisions and improvements for the skills repo. Append new items here; when done, delete or move to a "Done" section.

---

## touch-claude — handle `AGENT.md` / `AGENTS.md` aliases

**Status:** open
**Skill:** `book/poupa-time/touch-claude`
**Date logged:** 2026-05-08

### Context

When `touch-claude` bootstraps into a project, the vendored `doctor.sh` reports:

```
bad  AGENT.md missing
warn AGENTS.md missing
warn Codex hooks missing
```

We intentionally vendor only `CLAUDE.md` because Claude Code is the only target, but `doctor.sh` still expects the upstream 3-file pattern (`AGENT.md` source-of-truth, `CLAUDE.md` for Claude Code, `AGENTS.md` for Codex/Cursor/Windsurf).

### Options

- **A) Symlinks (recommended).** Add `ensure_aliases()` to `bootstrap.py` that creates `AGENT.md` and `AGENTS.md` as relative symlinks to `CLAUDE.md` after the template copy. ~10 lines. Single source of truth, doctor satisfied, future-proof if a non-Claude agent is ever added.

- **B) Edit vendored `doctor.sh`.** Remove the `AGENT.md`/`AGENTS.md`/Codex-hooks checks from the script. Works because we own the vendored copy. Diverges from upstream — we already accepted "no upstream sync".

- **C) Status quo.** Accept doctor's `bad`/`warn` as informational noise.

### Recommendation

**A**, optionally combined with **B** (silence the Codex-hooks `warn` too, since we don't use Codex either). Keeps the noise floor of `doctor.sh` honest — it should only complain about things we actually care about.

### Acceptance criteria

- `touch-claude` run on a fresh project produces a `doctor.sh` output with **no `bad` lines** and no unrelated `warn` lines.
- Existing `CLAUDE.md` in the target is still preserved (not overwritten).
- Symlinks (if option A) are relative, not absolute, so the project remains portable.
