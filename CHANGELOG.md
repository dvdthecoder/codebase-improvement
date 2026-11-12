# Changelog

All notable changes to this project are recorded here.

## Unreleased

- Baseline documentation now includes a domain glossary (`docs/glossary.md`, or the repository's existing glossary or `CONTEXT.md`), with a new template `assets/documentation-template/glossary.md`.

## 0.2.0

- Run record: the skill works on a `codebase-improvement/<date>` branch and records one Baseline commit (documentation only) and one Improvement commit per approved change, each with a `Codebase-Improvement` trailer and a structured message. See `docs/adr/0001-phase-commits-as-run-record.md`.
- `scripts/render_report.py` generates a self-contained HTML run report in `.git/codebase-improvement/report.html` from those commits.
- New reference `references/run-record.md`.

## 0.1.0

- Initial modular Agent Skill package.
- Documentation-first baseline and architecture improvement workflow.
- Reference guides for architecture, refactoring, technical writing and quality gates.
- Standard-library documentation, token-budget and Markdown-link validators.
- GitHub Actions validation workflow.
- Installation via `npx skills add dvdthecoder/codebase-improvement` for Claude Code, Codex and OpenCode.
- `CONTEXT.md` glossary.
- Skill leaves no execution by-products (e.g. `__pycache__/`) in target repositories.
- New baseline docs default to `docs/`; stale claims are corrected in place.
- Validators ignore hidden directories (installed skills) and no longer skip a whole repo when an ancestor directory is named `build`, `dist`, etc. `validate_links.py --ignore-hidden` is replaced by `--include-hidden`.
- `stale-docs` fixture no longer reveals the expected answer.

## Release policy

This project uses semantic versioning once it reaches `1.0.0`:

- MAJOR: incompatible workflow, metadata or package changes.
- MINOR: backward-compatible capabilities or reference additions.
- PATCH: fixes and clarifications.
