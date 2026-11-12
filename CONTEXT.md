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

## Relationships

- One **Skill** is **Published** once and **Installed** into many **Agents**
- The published repo contains exactly one **Skill**: `codebase-improvement`
- Codex and OpenCode share the project-level skill directory; Claude Code has its own

## Flagged ambiguities

- "backend" was used to mean **Agent**. Resolved: use **Agent**.
- "npm install" was used to mean **Install** via `npx`. Resolved: no npm registry package.
