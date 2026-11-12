# Steer score: a read-only script with gated levels

For an agent, a repository's own documentation is the context it works from, so we measure how well it steers an agent. The Steer score is computed by `scripts/score_steer.py`, a standard-library script that only reads files and git history. It reports points (13 equal-weight checks out of 100) and a gated level (L0 to L4): a level counts only when that level and every lower level pass in full. History lives in `Steer-Score` trailers on run commits. Batch runs print a table and write nothing.

## Considered options

- **Agent-judged score**: rejected as the main score. It varies between runs and agents, so trends and batch counts become noise, and it is costly across many repositories. An agent accuracy review can be added later, reported beside the score and never folded into it.
- **Points only**: rejected. A batch question like "how many repositories are at the bar?" needs a meaningful cut-off, not 70 versus 69.
- **Levels only**: rejected. Small improvements would be invisible until a whole level is reached.
- **Separate scoring skill or CLI package**: rejected. Scoring runs inside the improvement loop, before and after the baseline, so it ships as one script in the same skill.
- **History file or central CSV**: rejected. Git trailers keep git as the single source of truth (ADR-0001).

## Consequences

- The score measures structure, not truth. Check 3.2 (referenced paths exist) is the only accuracy proxy.
- Phase 1 aims for L3, which can raise scores. The skill must never write documentation only to pass a check.
