# Agent instructions

This repository publishes one Agent Skill, `codebase-improvement`, installed with `npx skills add dvdthecoder/codebase-improvement`. Read [README.md](README.md) for what it does and [CONTEXT.md](CONTEXT.md) for the terms to use.

## Layout

- `skills/codebase-improvement/` is the shipped skill. Everything in it is copied into users' repositories.
- `docs/adr/` records design decisions. Read them before changing the run record or the Steer score.
- `tests/` and `examples/` support development and are not shipped.

## Commands

Run all of these before committing. They need only Python 3.10+.

```bash
S=skills/codebase-improvement/scripts
python -B $S/check_doc_tokens.py --directory .
python -B $S/check_documentation.py --directory skills/codebase-improvement
python -B $S/validate_links.py --directory .
python -m py_compile $S/*.py
python -B tests/test_render_report.py
python -B tests/test_score_steer.py
python -B $S/score_steer.py --repo .
```

CI (`.github/workflows/validate-skill.yml`) runs the same checks.

## Conventions

- Scripts use the standard library only, and never run code from a scored or target repository.
- Every Markdown file stays under 5,000 tokens; aim for 4,200. Keep `SKILL.md` short and move detail into `references/`.
- Use the terms in `CONTEXT.md` (Skill, Agent, Baseline commit, Improvement commit, Steer score, Steer level). Add new terms there when they are settled.
- Record hard-to-reverse design choices as a new ADR in `docs/adr/`.
- Add each user-visible change under `## Unreleased` in `CHANGELOG.md`.

## Do not change without approval

- `.agents/`, `.claude/` and `skills-lock.json` hold development-only skills. They are git-ignored and must never be published.
- The commit trailer names (`Codebase-Improvement`, `Steer-Score`, `Steer-Score-Before`) and check IDs in `score_steer.py`: users' history and reports depend on them.
- Releases: tag `vX.Y.Z` on `main` and create a GitHub Release from the CHANGELOG entry, only when asked.
