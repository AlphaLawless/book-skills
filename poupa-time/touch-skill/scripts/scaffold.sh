#!/usr/bin/env bash
# scaffold.sh — scaffold a new skill folder with SKILL.md boilerplate + global symlink.
#
# Usage: scaffold.sh <skill-name> [--book <dir>] [--no-symlink]
#
# Default book is the parent of this skill folder (e.g. poupa-time/).
# Refuses to overwrite existing SKILL.md. Validates name per Anthropic rules.

set -euo pipefail

usage() {
  cat >&2 <<EOF
Usage: $(basename "$0") <skill-name> [--book <dir>] [--no-symlink]

  <skill-name>     lowercase letters, digits, hyphens; max 64 chars
  --book <dir>     book/plugin folder to place the skill in (default: parent of touch-skill)
  --no-symlink     skip ~/.claude/skills/<name> symlink

Creates: <book>/<skill-name>/SKILL.md (boilerplate)
Symlinks: ~/.claude/skills/<skill-name> -> absolute skill path
EOF
  exit 1
}

[[ $# -lt 1 ]] && usage
NAME="$1"; shift

# Anthropic name rules: lowercase letters/digits/hyphens only; max 64; no "anthropic"/"claude".
if [[ ! "$NAME" =~ ^[a-z0-9-]+$ ]]; then
  echo "ERROR: name must be lowercase letters, digits, hyphens only — got: '$NAME'" >&2
  exit 2
fi
if (( ${#NAME} > 64 )); then
  echo "ERROR: name exceeds 64 chars (${#NAME})" >&2
  exit 2
fi
if [[ "$NAME" == *anthropic* || "$NAME" == *claude* ]]; then
  echo "ERROR: name cannot contain 'anthropic' or 'claude' (reserved)" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOUCH_SKILL_DIR="$(dirname "$SCRIPT_DIR")"
BOOK_DIR="$(dirname "$TOUCH_SKILL_DIR")"
DO_SYMLINK=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --book)        BOOK_DIR="$(cd "$2" && pwd)"; shift 2 ;;
    --no-symlink)  DO_SYMLINK=0; shift ;;
    -h|--help)     usage ;;
    *)             echo "Unknown arg: $1" >&2; usage ;;
  esac
done

TARGET="$BOOK_DIR/$NAME"

if [[ -e "$TARGET/SKILL.md" ]]; then
  echo "ERROR: $TARGET/SKILL.md already exists — refusing to overwrite" >&2
  exit 3
fi

mkdir -p "$TARGET"

# Title: skill-name -> Skill Name
TITLE="$(echo "$NAME" | awk -F- '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1' OFS=' ')"

cat > "$TARGET/SKILL.md" <<EOF
---
name: $NAME
description: TODO one sentence — what it does. Use when TODO 2-3 trigger phrases users would actually say.
---

# $TITLE

## Quick start

[Minimal working example or one-line invocation]

## Workflow

1. [Step]
2. [Step]
3. [Step]

## When to use

- TODO concrete trigger 1
- TODO concrete trigger 2

## Notes

[Any why/reasoning. Avoid ALL-CAPS rules — explain the reason instead.]
EOF

echo "Created: $TARGET/SKILL.md"

if (( DO_SYMLINK )); then
  LINK="$HOME/.claude/skills/$NAME"
  if [[ -L "$LINK" || -e "$LINK" ]]; then
    echo "WARN: $LINK already exists — skipping symlink"
  else
    mkdir -p "$HOME/.claude/skills"
    ln -s "$TARGET" "$LINK"
    echo "Linked: $LINK -> $TARGET"
  fi
fi

cat <<EOF

Next:
  1. Edit $TARGET/SKILL.md — fill description with real triggers
  2. Add references/ for >300-line content; scripts/ for deterministic ops
  3. Validate: head -3 "$TARGET/SKILL.md"
EOF
