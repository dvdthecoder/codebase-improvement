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

**Steer**:
How well a repository's own documentation directs an agent working in it: what the system is, how it is built and tested, which terms to use and which rules to follow. For an agent, the codebase and its documentation are the context it works from.
_Avoid_: context quality, AI-readiness

**Steer score**:
A repeatable measure of a repository's Steer, tracked across runs and compared across repositories in a Batch run. Built in two tiers: software-development documentation first, then agent-specific steer.
_Avoid_: doc score, quality score

**Steer level**:
The rung a repository has reached on the Steer ladder: L0 Undescribed, L1 Described, L2 Engineered, L3 Steerable, L4 Self-maintaining. A level is reached only when every check of that level and all lower levels passes.
_Avoid_: grade, tier (tiers group levels; levels are the rungs)

**Batch run**:
Scoring many repositories in one invocation to see how many meet the Steer bar.

## Relationships

- One **Skill** is **Published** once and **Installed** into many **Agents**
- The published repo contains exactly one **Skill**: `codebase-improvement`
- A run produces exactly one **Baseline commit**, followed by zero or more **Improvement commits**
- A **Run report** is derived from those commits; it is never the source of truth
- Codex and OpenCode share the project-level skill directory; Claude Code has its own

## Flagged ambiguities

- "backend" was used to mean **Agent**. Resolved: use **Agent**.
- "npm install" was used to mean **Install** via `npx`. Resolved: no npm registry package.
