---
name: touch-claude
description: Bootstrap a vendored agent-md template (CLAUDE.md, .claude/hooks/, memory/, .agent-md/bin/) into a project. Self-contained — no network at runtime, no third-party install scripts, all files audited and copied locally. Lean for Claude Code only, 6 hooks (verify gate, progress enforcement, edit-time lint, TDD nudge, UI sensory reminder, playwright capture). Pre-seeds memory/gotchas.md with personal CLAUDE.md v3 directives. Use when the user wants to init/setup CLAUDE.md, scaffold project agent rules, bootstrap a new project's Claude config — triggers on "init claude", "init claude.md", "setup claude", "novo projeto", "bootstrap claude", "agent-md", "touch claude".
---

# touch-claude

Drop the audited agent-md template into a project. Everything is **vendored** in `assets/template/` — runtime is pure file copy, no network, no third-party install scripts. The template is yours now: edit it as your taste evolves.

## Provenance

Vendored from `iamfakeguru/agent-md` at commit `ae8117e9` (2026-04-27). 9 shell scripts audited before vendoring — see [`assets/PROVENANCE.md`](assets/PROVENANCE.md) for the audit record. Hand-maintained from here, no upstream sync.

## Quick start

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-/home/alpha/.claude/skills/touch-claude}"
python3 "$SKILL_DIR/scripts/bootstrap.py" /path/to/project
```

Defaults: skip files that already exist; append v3 seed to `memory/gotchas.md`. Re-run with `--force` to overwrite (each replaced file backed up to `<name>.bak`).

## What gets copied (17 files)

```
<target>/
├── CLAUDE.md                         the directives (15 sections)
├── .claude/
│   ├── settings.json                 wires the 6 hooks
│   └── hooks/
│       ├── _lib.sh                   shared helpers
│       ├── post-edit-verify.sh       PostToolUse → lint after Write/Edit
│       ├── tdd-check.sh              PostToolUse → warn on export-without-test
│       ├── stop-verify.sh            Stop → typecheck + lint + test gate
│       ├── state-enforcement.sh      Stop → block if progress.md not updated
│       └── sensory-reminder.sh       Stop → ask for screenshot on UI change
├── .agent-md/
│   ├── README.md
│   └── bin/
│       ├── doctor.sh                 self-diagnostic
│       ├── discover_helpers.sh       list helper scripts
│       └── playwright-capture.sh     DOM screenshot for visual validation
└── memory/
    ├── agents.md                     active tooling, MCPs, tech stack
    ├── plan.md                       macro design
    ├── progress.md                   current task, completed, backlog, blocked
    ├── verify.md                     definition of done
    └── gotchas.md                    corrected mistakes (seeded with v3 directives)
```

**Excluded:** `block-destructive.sh` (RTK already covers destructive bash), `truncation-check.sh` (niche), `.codex/`, `.cursor/`, `.windsurf/`, `.agents/skills/`, `.githooks/pre-commit`, `AGENT.md`, `AGENTS.md` (Claude Code only).

## The 3 enforcement pillars

| Pillar | Hook | Effect |
|---|---|---|
| **Verify gate** | `stop-verify.sh` | Reads `agent-md.toml`, runs typecheck + lint + test on Stop. Blocks "Done" until they pass. |
| **Progress enforcement** | `state-enforcement.sh` | Blocks Stop if source files changed but `memory/progress.md` did not. |
| **Edit-time lint** | `post-edit-verify.sh` | Runs lint on the edited file right after Write/Edit, surfaces errors fast. |

Plus 3 nudges: `tdd-check.sh` (warn on export-without-test), `sensory-reminder.sh` (UI screenshot prompt), `playwright-capture.sh` (the actual screenshot helper).

## Workflow

```
- [ ] 1. Confirm target dir (default: cwd)
- [ ] 2. Sanity check — exists, is a dir
- [ ] 3. Run bootstrap.py — copies template + seeds gotchas
- [ ] 4. Write agent-md.toml directly with stack-specific verify commands (templates in Step 2)
- [ ] 5. Inspect: cat <target>/CLAUDE.md ; bash <target>/.agent-md/bin/doctor.sh
- [ ] 6. Commit with the user's approval
```

### Step 1 — Run

```bash
python3 scripts/bootstrap.py <target>          # default: skip existing
python3 scripts/bootstrap.py <target> --force  # overwrite (backups go to *.bak)
python3 scripts/bootstrap.py <target> --dry-run
python3 scripts/bootstrap.py <target> --no-seed
```

### Step 2 — Write `agent-md.toml`

Auto-detection is intentionally not bundled — early-adopter stacks (biome, oxc, tsgo) get mis-classified by heuristics. Write the toml fresh per project, picking from the templates below. Use the `Write` tool directly; `agent-md.toml` is a new file, no Read needed.

**Node + biome (early-adopter):**

```toml
[verify]
typecheck = "npx --no-install tsc --noEmit"
lint      = "biome check ."
test      = "pnpm test"
lint_file = "biome check {file}"
```

**Python + ruff + uv:**

```toml
[verify]
typecheck = "uv run mypy ."
lint      = "uv run ruff check ."
test      = "uv run pytest"
lint_file = "uv run ruff check {file}"
```

**UI work — enable visual evidence:**

```toml
[visual]
required          = true
artifacts_dir     = ".agent/visual"
freshness_seconds = 3600
```

### Step 3 — Verify install

```bash
bash <target>/.agent-md/bin/doctor.sh
```

Reports any missing pieces (no `agent-md.toml`, missing hooks, etc.). `discover_helpers.sh` lists the helper scripts.

## Common pitfalls

- **Existing `.claude/settings.json` in target** — bootstrap skips by default. Merge entries manually, or pass `--force` to back up + replace.
- **Existing `CLAUDE.md`** — same default-skip. Diff against the template manually before forcing.
- **Hooks not executable** — `shutil.copy2` preserves mode bits. If somehow not, run `chmod +x .claude/hooks/*.sh .agent-md/bin/*.sh`.
- **`agent-md.toml` not created** — bootstrap doesn't generate one. Write it from the templates in Step 2. Until it exists, `stop-verify.sh` falls back to heuristic detection (works, but less explicit).
- **Network blocked** — irrelevant. Bootstrap is pure local file copy.

## References

- [`assets/template/`](assets/template/) — the 17 vendored files (your code now)
- [`assets/PROVENANCE.md`](assets/PROVENANCE.md) — audit summary + origin record
- [`assets/gotchas-seed.md`](assets/gotchas-seed.md) — v3 directives appended to `memory/gotchas.md`
- [agent-md upstream](https://github.com/iamfakeguru/agent-md) — origin (read-only reference)
