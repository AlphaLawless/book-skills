---
name: touch-skill
description: Create new agent skills following Anthropic best practices — YAML frontmatter, progressive disclosure, bundled resources, global symlink. Pure-instruction skill, no scaffold script — Claude reads template + runs mkdir/ln directly. Use when the user wants to create, write, build, scaffold, or "touch" a new skill — triggers on "create skill", "new skill", "build skill", "scaffold skill", "touch skill".
---

# touch-skill

Create new skills following Anthropic's [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices). No scaffold script — instructions only. Develop in `/home/alpha/Projects/me/skills/<book>/<skill-name>/`, then symlink to `~/.claude/skills/<skill-name>` for global access.

**Why no script?** A scaffolder that writes a placeholder `SKILL.md` triggers the harness "must Read before Write" check, forcing extra round trips. Three deterministic shell commands (`mkdir`, `ln`, regex check) belong inline.

## Workflow

```
- [ ] 1. Capture intent (4 questions)
- [ ] 2. Validate the chosen name
- [ ] 3. mkdir + symlink
- [ ] 4. Write SKILL.md from template (Write tool, no Read needed — new file)
- [ ] 5. Add references/, scripts/, assets/ as needed (progressive disclosure)
- [ ] 6. Run review checklist
- [ ] 7. Manual test: invoke /<name> with natural phrasing
```

### Step 1 — Capture intent

Get crisp answers before creating anything:

1. **What** should this skill enable Claude to do? (one sentence)
2. **When** should it trigger? Concrete user phrases (3+).
3. **Output** format? (file edits, plan, summary, command)
4. **Verifiable?** Add a validation script for objective outputs (transforms, codegen). Skip for subjective ones (writing style, taste).

If you can't write (1) in one sentence and list 3 triggers for (2), **stop**. Ask the user.

### Step 2 — Validate the name

The name must satisfy all of:

- Lowercase letters, digits, hyphens only: matches `^[a-z0-9-]+$`
- Length ≤ 64 characters
- Does **not** contain `anthropic` or `claude` (Anthropic-reserved tokens — silently rejected)

If invalid, refuse and ask the user for another. Don't try to "fix" their name silently.

### Step 3 — Create folder + symlink

Run from the user's `me/skills` repo:

```bash
NAME="<skill-name>"
BOOK="/home/alpha/Projects/me/skills/poupa-time"   # or another book folder
mkdir -p "$BOOK/$NAME"
mkdir -p "$HOME/.claude/skills"
ln -s "$BOOK/$NAME" "$HOME/.claude/skills/$NAME"
```

If `~/.claude/skills/$NAME` already exists, skip the `ln -s` and warn the user — don't clobber.

### Step 4 — Write SKILL.md from this template

Use the Write tool **directly** — the file is new, no Read needed. Replace placeholders, then refine.

````markdown
---
name: <skill-name>
description: <one sentence — what it does>. Use when <2-3 trigger phrases users would actually say>.
---

# <Skill Name>

## Quick start

[Minimal working example or one-line invocation]

## Workflow

1. [Step]
2. [Step]
3. [Step]

## When to use

- <concrete trigger 1>
- <concrete trigger 2>

## Notes

[Why/reasoning. Avoid ALL-CAPS rules — explain the reason instead.]
````

### Step 5 — Bundled resources (optional)

Add subfolders only when warranted:

- `references/` — markdown loaded on-demand (>300 lines, domain variants)
- `scripts/` — deterministic operations, run via bash (0 tokens until output)
- `assets/` — templates, fonts, files used in output

## Skill anatomy (full)

```
<book>/<skill-name>/
├── SKILL.md           required — ≤500 lines (target ≤150)
├── README.md          optional — one-line index entry for the book
├── references/        optional — load on-demand
├── scripts/           optional — bash/python utilities
└── assets/            optional — templates, fonts
```

## Frontmatter rules

```yaml
---
name: skill-name           # lowercase + hyphens, ≤64 chars, no "anthropic"/"claude"
description: ...           # ≤1024 chars; first sentence what, second "Use when ..."
---
```

The `description` is the **only** thing Claude sees when picking a skill from many. Be *pushy* with triggers — Claude tends to under-trigger.

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

SKILL.md body **stays in context for the rest of the session** once loaded — every line is recurring cost. When you cross ~150 lines, split: detailed examples → `EXAMPLES.md`, large reference → `references/<domain>.md`.

## When to add a script

Add a `scripts/foo.sh` (or `.py`) when:

- The operation is deterministic (validation, formatting)
- Claude would regenerate the same code every run
- Errors need explicit, verbose handling

Scripts execute via bash — source stays on disk (0 tokens), only output enters context.

Stay in markdown when the task needs judgement, branching prose, or per-context adaptation.

## Explain the why, not just the rule

LLMs generalise from reasoning. Prefer:

> Use constructor injection. Field injection breaks testability — we can't mock the field without Spring context.

Over:

> ALWAYS use constructor injection. NEVER use field injection.

ALL-CAPS rules are a yellow flag. Reframe with the underlying reason — Claude then handles edge cases the skill never spelled out.

## Review checklist

- [ ] `name` ≤64 chars, lowercase+hyphens, no `anthropic`/`claude`
- [ ] `description` ≤1024 chars, includes "Use when ..." with 2-3 trigger phrases
- [ ] SKILL.md body ≤500 lines (target ≤150)
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] At least one concrete example
- [ ] References one level deep
- [ ] Symlink resolves: `ls -L ~/.claude/skills/<name>`
- [ ] Manual test: invoke with natural phrasing — does it trigger?

## Common pitfalls

- **Description too vague** — Claude can't disambiguate.
- **Skill never triggers** — add more keywords; rephrase aggressively.
- **Skill triggers too often** — make description more specific or set `disable-model-invocation: true`.
- **Bloated SKILL.md** — body persists in context; split into `references/`.
- **Reserved words** — `anthropic`/`claude` in name silently rejected.

## References

- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — Anthropic
- [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — Anthropic
- [Claude Code skills docs](https://code.claude.com/docs/en/skills)
- [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) — Anthropic reference impl
- [matt-pocock/skills](https://github.com/mattpocock/skills) — pure-instruction style inspiration
