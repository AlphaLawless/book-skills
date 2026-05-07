#!/usr/bin/env python3
"""Bootstrap the vendored agent-md template into a project. Pure local copy.

Copies assets/template/ into the target project, preserving file modes
(executable hooks stay executable). Idempotent: skips files that already
exist unless --force. Appends the personal v3 gotchas seed to
memory/gotchas.md after copy.

Usage:
  bootstrap.py [target]              # default: cwd
  bootstrap.py --dry-run .
  bootstrap.py --force .             # back up existing files to *.bak
  bootstrap.py --no-seed .           # skip gotchas seed
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
TEMPLATE = SKILL_ROOT / "assets" / "template"
SEED = SKILL_ROOT / "assets" / "gotchas-seed.md"
SEED_MARKER = "Personal seed (from CLAUDE.md v3)"


def files(root: Path):
    for p in root.rglob("*"):
        if p.is_file():
            yield p, p.relative_to(root)


def append_seed(target: Path, seed_path: Path) -> str:
    gotchas = target / "memory" / "gotchas.md"
    if not gotchas.exists():
        return "skip (memory/gotchas.md missing)"
    if not seed_path.exists():
        return "skip (seed file missing in skill)"
    existing = gotchas.read_text()
    if SEED_MARKER in existing:
        return "skip (already seeded)"
    sep = "" if existing.endswith("\n") else "\n"
    gotchas.write_text(existing + sep + "\n---\n\n" + seed_path.read_text())
    return "appended"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("target", nargs="?", default=".",
                   help="Project root (default: cwd)")
    p.add_argument("--force", action="store_true",
                   help="Overwrite existing files (backup to *.bak)")
    p.add_argument("--no-seed", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    target = Path(args.target).resolve()
    if not target.exists() or not target.is_dir():
        print(f"ERROR: target is not a directory: {target}", file=sys.stderr)
        return 2
    if not TEMPLATE.exists():
        print(f"ERROR: template missing at {TEMPLATE}", file=sys.stderr)
        return 3

    print(f"Target:   {target}")
    print(f"Template: {TEMPLATE}")
    if args.dry_run:
        print("(dry-run — no changes)")

    written, skipped, replaced = [], [], []
    for src, rel in files(TEMPLATE):
        dst = target / rel
        if dst.exists():
            if not args.force:
                skipped.append(str(rel))
                if args.dry_run:
                    print(f"  skip    {rel}")
                continue
            if not args.dry_run:
                bak = dst.with_suffix(dst.suffix + ".bak")
                dst.rename(bak)
            replaced.append(str(rel))
            if args.dry_run:
                print(f"  replace {rel} (backup .bak)")

        if not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)  # preserves mode bits
        written.append(str(rel))
        if args.dry_run:
            print(f"  write   {rel}")

    if args.no_seed or args.dry_run:
        seed_status = "skipped" + (" (--no-seed)" if args.no_seed else " (dry-run)")
    else:
        seed_status = append_seed(target, SEED)

    print(f"\nResult:")
    print(f"  wrote:    {len(written)}")
    print(f"  replaced: {len(replaced)}")
    print(f"  skipped:  {len(skipped)}"
          f"{' (use --force to overwrite)' if skipped and not args.force else ''}")
    print(f"  seed:     {seed_status}")
    print(f"\nNext:")
    print(f"  Write {target}/agent-md.toml — see SKILL.md Step 2 for stack templates")
    print(f"  bash {target}/.agent-md/bin/doctor.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
