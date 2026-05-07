# Vendored agent-md template — provenance

## Source

- **Repo:** https://github.com/iamfakeguru/agent-md
- **Commit:** `ae8117e903fe07266c97560cbe286285e0562b82`
- **Date:** 2026-04-27 (commit) / 2026-05-07 (vendored)

## What was vendored (17 files)

```
assets/template/
├── CLAUDE.md
├── .claude/
│   ├── settings.json                  ← modified (see below)
│   └── hooks/
│       ├── _lib.sh
│       ├── post-edit-verify.sh
│       ├── sensory-reminder.sh
│       ├── state-enforcement.sh
│       ├── stop-verify.sh
│       └── tdd-check.sh
├── .agent-md/
│   ├── README.md
│   └── bin/
│       ├── discover_helpers.sh
│       ├── doctor.sh
│       └── playwright-capture.sh
└── memory/
    ├── agents.md
    ├── gotchas.md
    ├── plan.md
    ├── progress.md
    └── verify.md
```

## Audit summary

9 shell scripts read in full before vendoring. Risky-pattern scan checked for: `curl|wget|/dev/tcp` (network), `sudo`, `eval`, `rm -rf $var`, writes to `/etc/`/`/usr/`/`~/.ssh`, `chmod 777|+s`, `nc`/`netcat`.

| File | Size | Risky patterns | Verdict |
|---|---|---|---|
| `.claude/hooks/_lib.sh` | 4.5KB | none | ✓ |
| `.claude/hooks/post-edit-verify.sh` | 2.6KB | none | ✓ |
| `.claude/hooks/sensory-reminder.sh` | 3.2KB | none | ✓ |
| `.claude/hooks/state-enforcement.sh` | 2.0KB | none | ✓ |
| `.claude/hooks/stop-verify.sh` | 3.7KB | `eval "$cmd"` for user-defined verify commands | ✓ accepted |
| `.claude/hooks/tdd-check.sh` | 2.8KB | none | ✓ |
| `.agent-md/bin/discover_helpers.sh` | 1.2KB | none | ✓ |
| `.agent-md/bin/doctor.sh` | 1.6KB | none | ✓ |
| `.agent-md/bin/playwright-capture.sh` | 1.6KB | none (requires `npx playwright` at runtime) | ✓ |

The single `eval` in `stop-verify.sh` runs the typecheck/lint/test commands the user wrote in their `agent-md.toml`. Risk is bounded — the user is the only author of those strings. Never trust an `agent-md.toml` you didn't write.

## Modifications applied at vendor time

`assets/template/.claude/settings.json` — removed:

- `PreToolUse → Bash → block-destructive.sh` entry (whole `PreToolUse` block dropped, that was its only entry)
- `PostToolUse → Grep|Bash → truncation-check.sh` entry (whole matcher block dropped, that was its only entry)

The settings now wires 6 hooks instead of upstream's 8.

## Hand-maintained from here

No upstream sync planned. The template under `assets/template/` is author-maintained — edited in place as the workflow evolves. The provenance above is a one-time origin record, not an active link to the upstream repo.
