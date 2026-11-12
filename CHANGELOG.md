# Changelog

All notable changes to this project are recorded here.

## Unreleased

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
