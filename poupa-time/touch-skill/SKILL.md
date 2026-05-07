---
name: touch-skill
description: Scaffold a new agent skill with proper structure (YAML frontmatter, progressive disclosure, bundled resources) and a global symlink. Use when the user wants to create, write, build, scaffold, or "touch" a new skill — triggers on "create skill", "new skill", "build skill", "scaffold skill", "touch skill".
---

# touch-skill

Scaffold new skills following Anthropic's [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), with a deterministic boilerplate script and progressive-disclosure structure.

## Quick start

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/scaffold.sh" <skill-name>
```

Creates `<book>/<skill-name>/SKILL.md` (placeholder) and symlinks `~/.claude/skills/<skill-name>` to the absolute path. Then fill the description and instructions per the rules below.

If `${CLAUDE_SKILL_DIR}` isn't set, use the absolute path: `bash /home/alpha/Projects/me/skills/poupa-time/touch-skill/scripts/scaffold.sh <name>`.

## Workflow

Copy this checklist and tick items as you go:

```
- [ ] 1. Capture intent (4 questions)
- [ ] 2. Run scaffold.sh <name>
- [ ] 3. Fill description with trigger keywords ("Use when ...")
- [ ] 4. Write Quick start + Workflow sections (<150 lines total)
- [ ] 5. Add references/ for content >300 lines or domain variants
- [ ] 6. Add scripts/ for deterministic operations
- [ ] 7. Run review checklist (below)
- [ ] 8. Manual test: invoke /<name> with natural phrasing — does it trigger?
```

### Step 1 — Capture intent

Before scaffolding, get crisp answers to:

1. **What** should this skill enable Claude to do? (one sentence)
2. **When** should it trigger? Concrete user phrases or contexts (3+).
3. **Output** format expected? (file edits, plan, summary, command, etc.)
4. **Verifiable?** Should we add a validation script? Skills with objective outputs (transforms, extraction, codegen, fixed workflows) benefit; subjective ones (writing style, taste) usually don't.

If you can't answer (1) in one sentence and list 3 triggers for (2), **stop** and ask the user. The skill isn't ready.

### Step 2 — Scaffold

```bash
bash scripts/scaffold.sh <name>                  # place in current book folder
bash scripts/scaffold.sh <name> --book <dir>     # custom book
bash scripts/scaffold.sh <name> --no-symlink     # skip global symlink
```

Name validation: lowercase letters/digits/hyphens, ≤64 chars, no `anthropic` or `claude` substring (reserved by Anthropic).

## Anatomy of a skill

```
<book>/<skill-name>/
├── SKILL.md           required — main instructions, <500 lines
├── README.md          optional — one-line index entry for the book
├── references/        optional — markdown loaded on-demand (>300 lines, domain variants)
│   ├── aws.md
│   └── gcp.md
├── scripts/           optional — deterministic operations, run via bash (0 tokens)
│   └── validate.sh
└── assets/            optional — templates, fonts, files used in output
```

## Frontmatter rules

```yaml
---
name: skill-name           # lowercase + hyphens, ≤64 chars, no "anthropic"/"claude"
description: ...           # ≤1024 chars; first sentence what, second "Use when ..."
---
```

The `description` is the **only** thing Claude sees when picking a skill from dozens. Be *pushy* with triggers — Claude tends to under-trigger.

**Good** — concrete capability + concrete triggers:

> Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDFs or when user mentions PDFs, forms, or extraction.

**Bad** — vague, no triggers:

> Helps with documents.

## Progressive disclosure (3 levels)

| Level | Content | When loaded | Token cost |
|-------|---------|-------------|------------|
| 1 | `name` + `description` | Always (system prompt) | ~50/skill |
| 2 | SKILL.md body | When skill triggers | full body, persistent |
| 3 | `references/`, `scripts/` | Only when SKILL.md says to read/run | 0 until accessed |

SKILL.md content **stays in context for the rest of the session** once loaded — every line is recurring cost. When you cross ~150 lines, split: move detailed examples to `EXAMPLES.md`, large reference to `references/<domain>.md`. Point to them with usage hints: *"For AWS-specific config, see `references/aws.md`."*

## When to add a script vs more markdown

Add a `scripts/foo.sh` (or `.py`) when:

- The operation is deterministic (validation, formatting, scaffolding)
- Claude would regenerate the same code every run
- Errors need explicit, verbose handling (e.g., "Field X not found. Available: ...")

Scripts execute via bash — their source stays on disk (0 tokens), only the output enters context.

Keep it as markdown when the task needs judgement, branching prose, or per-context adaptation.

## Explain the why, not just the rule

LLMs generalise from reasoning. Prefer:

> Use constructor injection. Field injection breaks testability — we can't mock the field without Spring context.

Over:

> ALWAYS use constructor injection. NEVER use field injection.

ALL-CAPS rules are a yellow flag. Reframe with the underlying reason — Claude then handles edge cases the skill never spelled out.

## Review checklist

Before shipping:

- [ ] `name` is lowercase + hyphens, ≤64 chars, no `anthropic`/`claude`
- [ ] `description` ≤1024 chars, includes "Use when ..." with 2-3 real trigger phrases
- [ ] SKILL.md body ≤500 lines (target ≤150 for terse skills)
- [ ] No time-sensitive info (dates, "current version of X")
- [ ] Consistent terminology — same word for same concept throughout
- [ ] At least one concrete example
- [ ] References one level deep (`references/foo.md`, not `references/sub/foo.md`)
- [ ] Scripts have verbose error messages
- [ ] Symlink at `~/.claude/skills/<name>` resolves correctly (`ls -L`)
- [ ] Manual trigger test passed (invoked from a natural user phrase)

## Common pitfalls

- **Description too vague** ("helps with X") — Claude can't disambiguate from sibling skills.
- **Skill never triggers** — Claude under-triggers by default. Add more keywords; rephrase the description more aggressively.
- **Skill triggers too often** — make the description more specific, or set `disable-model-invocation: true` for manual-only invocation.
- **Bloated SKILL.md** — body stays in context all session. Split into `references/` aggressively.
- **Reserved-word names** — names containing `anthropic` or `claude` are silently rejected.

## References

- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — Anthropic
- [Agent Skills overview (3-level model)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — Anthropic
- [Claude Code skills docs](https://code.claude.com/docs/en/skills)
- [skill-creator (reference impl)](https://github.com/anthropics/skills/tree/main/skills/skill-creator) — Anthropic
- [matt-pocock/skills](https://github.com/mattpocock/skills) — terse-style inspiration
