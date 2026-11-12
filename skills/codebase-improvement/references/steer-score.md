# Steer Score

## Purpose

Measure how well a repository's own documentation steers an agent. For an agent, the codebase and its documentation are the context it works from. The score is produced by `scripts/score_steer.py`: read-only, standard library only, and it never runs code from the scored repository. The same repository state always gives the same score, so scores can be compared across runs and across repositories.

## Levels

Levels form a ladder. A repository reaches a level only when every check of that level and every lower level passes.

| Level | Name | Meaning |
|---|---|---|
| L0 | Undescribed | No usable README |
| L1 | Described | A human can tell what it is and how to run it |
| L2 | Engineered | Architecture, glossary, test command and links are in place |
| L3 | Steerable | An agent can act without guessing: instructions, real references, coverage, context-sized docs |
| L4 | Self-maintaining | Decisions are recorded, docs keep up with code, and CI checks them |

Points: each of the 13 checks is worth an equal share of 100. Points show progress inside a level; the level answers "is this repository at the bar?"

## Checks

| ID | Check | Passes when |
|---|---|---|
| 1.1 | README | Root README has at least 150 words |
| 1.2 | How to run | README contains a fenced code block |
| 2.1 | Architecture | `architecture.md`, an `architecture/` folder, or an Architecture/Components section |
| 2.2 | Glossary | `docs/glossary.md`, `GLOSSARY.md` or `CONTEXT.md` defines at least 5 terms |
| 2.3 | How to test | Docs name a test command (`pytest`, `npm test`, `go test`, ...) |
| 2.4 | Links | No broken local links in docs |
| 3.1 | Agent instructions | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md` or `.cursor/rules/` |
| 3.2 | References are real | At least 90% of backticked code paths in docs exist in the repository |
| 3.3 | Coverage | At least 80% of source modules are named in docs |
| 3.4 | Fits in context | Every doc is under 5,000 tokens (changelogs and licences excluded) |
| 4.1 | Decisions | `docs/adr/` or `docs/decisions/` holds at least one record |
| 4.2 | Fresh | Docs last changed no more than 90 days before the last code change |
| 4.3 | Enforced | A CI workflow runs a documentation or link check |

Thresholds are named constants at the top of `score_steer.py`.

## Using the score

- **Score-only mode:** run the script, then explain each failed check and the smallest honest fix.
- **Improvement runs:** score at the start (Phase 0) and after the baseline (Phase 1). Phase 1 aims for L3. Failed L4 checks become Phase 3 findings because they change process or CI.
- **History:** recorded as `Steer-Score` trailers on run commits (see `references/run-record.md`). `git log` shows the trend.
- **Batch runs:** `score_steer.py --batch <dir>...` prints one row per repository and the count per level. It writes nothing.

## Limits

The score measures structure, not truth. A complete but wrong document can pass. Check 3.2 is a cheap accuracy proxy only: it confirms that referenced paths exist, not that claims about them are correct. Accuracy comes from the evidence-based baseline in Phase 1.
