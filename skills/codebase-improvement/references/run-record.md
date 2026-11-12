# Run Record

## Purpose

Record each run so that documentation and improvement stay separate and reviewable. Git is the single source of truth. The run report is generated from commits and is never committed.

## Run branch

- Name: `codebase-improvement/<YYYY-MM-DD>`. If the name exists, append `-2`, `-3` and so on.
- Create it from HEAD at the start of the run, before writing any file.
- Never commit to the branch the user had checked out.
- Never push, merge or delete branches. The user decides what happens to the run branch.

## Commits

A run has exactly one Baseline commit, followed by zero or more Improvement commits. Each commit carries a `Codebase-Improvement` trailer in the final paragraph of its message, which `scripts/render_report.py` uses to classify it. Write the message to a file and use `git commit -F <file>`, so formatting survives.

Stage only the files that belong to the commit. Review `git diff --cached` before committing.

### Baseline commit

Contains documentation changes only: new baseline documents and corrections of stale claims. No application code, tests or configuration.

```text
docs: baseline documentation

Maturity:
| Area | Status |
|---|---|
| Entry points | Adequate |
| Data ownership | Unable to verify |

Validators:
check_doc_tokens.py --directory docs: 3 files, 0 failures (heuristic estimate)
validate_links.py --directory .: 7 links, 0 errors

Codebase-Improvement: baseline
```

### Improvement commit

Contains one approved improvement: the code change, its tests and the documentation updates that describe the new state.

```text
refactor: share Qodo enrichment loop across commands (ARCH-001)

Finding: the enrich-compact-sum loop is duplicated three times in cli.main.
Evidence: prtool/cli.py::main (qodo-inline, mr-context, qodo-threshold branches).
Change: extract cli._run_qodo_candidates; callers keep their output lines.
Validation:
python -m pytest: 87 passed
check_doc_tokens.py --directory docs: 0 failures

Codebase-Improvement: ARCH-001
```

Rules:
- Use the finding ID from Phase 3 as the trailer value.
- Under `Validation`, list exact commands and outcomes. Name skipped checks as skipped. A skipped check is not a pass.
- Do not claim results that were not produced by a command in this run.

## Run report

Generate it at the end of the run:

```bash
python <skill-root>/scripts/render_report.py --repo <repository-root>
```

The script finds the most recent Baseline commit reachable from HEAD and writes `.git/codebase-improvement/report.html`. The report has a Documentation section and an Improvements section. Commits after the Baseline commit that carry no trailer are listed separately as other commits. Include the report path in the final report.

## No run record

When the target is not a Git repository and the user declines `git init`, or the run is headless, skip the branch, commits and report. State this in the final report, and keep the documentation and improvement outcomes in separate sections there.
