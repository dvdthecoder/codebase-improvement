# Phase commits are the run record

A run must show documentation and improvement as separate outcomes, and must produce a reviewable report in Claude Code, Codex and OpenCode alike. The skill therefore commits on a branch it creates (`codebase-improvement/<date>`): one Baseline commit (documentation only) at the end of Phase 1, then one Improvement commit per approved change at the end of Phase 6. Each commit carries a `Codebase-Improvement:` trailer and a structured message body. The Run report is generated from those commits by a standard-library script, written inside `.git/` and never committed, so git stays the single source of truth.

## Considered options

- **Branch or PR per outcome**: rejected. PR tooling differs per host, and the improvement depends on the baseline anyway.
- **Run-record folder of Markdown/JSON files**: rejected for now. It duplicates what commit messages can hold, and can drift from the code.
- **Two separate skills**: rejected. Double the packaging, and the improve phase cannot run without a baseline.
- **Agent-written HTML report**: rejected. Output varies by agent and costs tokens every run. A script is deterministic and portable.
- **Self-scoring in the report**: rejected. Grading belongs to the human reviewer.

## Consequences

- The skill now creates a branch and commits in the target repository. It stops if the working tree is dirty, and asks before initialising git in a non-git directory. Headless runs skip the record instead.
- Commit message format becomes part of the skill's contract, because `render_report.py` parses the trailers.
