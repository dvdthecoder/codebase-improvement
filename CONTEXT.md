# Codebase Improvement

A portable Agent Skill, distributed from GitHub, that improves an existing repository through a documentation-first loop.

## Language

**Skill**:
The installable unit: a folder containing `SKILL.md` plus its references, scripts and assets.
_Avoid_: plugin, package

**Agent**:
A coding tool that loads and runs a Skill (Claude Code, Codex, OpenCode).
_Avoid_: backend, harness, platform

**Publish**:
Make the Skill installable by others from a GitHub repository. Nothing goes to the npm registry.
_Avoid_: release to npm

**Install**:
Copy a published Skill into an Agent's skill directory, at project or global level, using `npx skills add`.

**Dev Skill**:
A third-party Skill installed in this repo only to help develop it (e.g. `grill-with-docs`). Never Published.
_Avoid_: bundled skill

**Baseline commit**:
The commit that records the current-state documentation of the target repository, before any improvement. Contains documentation only.
_Avoid_: docs commit, initial commit

**Improvement commit**:
A commit that records one approved improvement: the code change, its tests and the documentation updates that describe it.
_Avoid_: refactor commit, fix commit

**Run report**:
A self-contained HTML page generated from a run's Baseline and Improvement commits, showing documentation and improvements separately.
_Avoid_: dashboard, summary

## Relationships

- One **Skill** is **Published** once and **Installed** into many **Agents**
- The published repo contains exactly one **Skill**: `codebase-improvement`
- A run produces exactly one **Baseline commit**, followed by zero or more **Improvement commits**
- A **Run report** is derived from those commits; it is never the source of truth
- Codex and OpenCode share the project-level skill directory; Claude Code has its own

## Flagged ambiguities

- "backend" was used to mean **Agent**. Resolved: use **Agent**.
- "npm install" was used to mean **Install** via `npx`. Resolved: no npm registry package.
