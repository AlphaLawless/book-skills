Skills are organized into bucket folders under `book/`:

- `poupa-time/` — meta-tools (scaffolding, bootstrap, time-savers)
- `scientist/` — research and explainer skills

Each skill lives at `book/<bucket>/<skill-name>/SKILL.md` and is made globally available via a symlink at `~/.claude/skills/<skill-name>` pointing to the absolute skill folder. When folders move or rename, refresh the symlink.

Each bucket has a `README.md` listing its skills with one-line descriptions. When adding or removing a skill, update the bucket `README.md`.

Other top-level folders are not skills:

- `books/` — PDFs and reading material
- `study/` — external repos cloned for reference (read-only, never edit)
