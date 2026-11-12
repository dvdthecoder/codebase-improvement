# Quality Gates and Completion Criteria

## Purpose

Define evidence required to move between phases and to report completion.

## Gate A — Repository discovery

Required:
- Repository root and requested scope identified.
- Working-tree changes noted.
- Main languages, runtimes and build/test entry points identified.
- Existing docs and relevant code areas inventoried.

If repository access is incomplete, state the limitation.

## Gate B — Baseline documentation

Required:
- Current-state map grounded in source.
- Critical entry points, components, interfaces and data ownership understood.
- Important execution flows described.
- Critical unknowns recorded.
- Documentation maturity assessed.
- Generated docs below the token limit.

Do not pass this gate if unresolved uncertainty could materially invalidate architecture analysis.

## Gate C — Architecture proposal

Required:
- Each finding has evidence and affected paths/symbols.
- Impact, confidence, cost and risk are explained.
- Proposed change has a validation strategy.
- User approval is obtained before application-code changes in interactive mode.

## Gate D — Implementation

Required:
- Change stays within approved scope.
- Relevant tests are added or updated.
- Compatibility and migration implications are handled.
- Full diff reviewed.
- No unapproved destructive or externally visible action.

## Gate E — Implementation validation

Required:
- Relevant checks executed where possible.
- Exact outcomes recorded.
- Failures resolved or explicitly reported.
- Environment-blocked checks distinguished from code failures.

A skipped check is not a pass.

## Gate F — Documentation synchronization

Required:
- Docs describe verified current behaviour.
- Interfaces, diagrams, configuration and operations references are updated where affected.
- ADRs record consequential decisions.
- Stale claims are removed or marked historical.
- Links and file paths validated.
- Per-file token counts checked.

## Token budget policy

The hard rule is **strictly fewer than 5,000 tokens per file**. A file with exactly 5,000 tokens fails.

Preferred target is 4,200 tokens. The target is a buffer, not a second hard failure threshold unless a repository owner configures it as such.

The supplied checker:
- Counts Markdown/text files by default.
- Uses `tiktoken` when an encoding is supplied and the package is installed.
- Otherwise uses a conservative heuristic estimator.
- Reports whether counts are exact-tokenizer results or estimates.
- Returns non-zero if any file reaches or exceeds the hard maximum.

Do not claim an estimate is an exact model token count.

## Documentation structure checks

The supplied checker can report:
- Empty Markdown files.
- Missing top-level headings.
- Oversized files.
- Broken local Markdown links (handled by the link validator).
- Files without an obvious focused purpose (manual review remains necessary).

Automated checks cannot prove technical accuracy. Compare key claims to source and review examples and diagrams.

## Completion report template

```markdown
## Completion report

### Scope
- Repository:
- Directories/modules:
- Operating mode:

### Baseline
- Maturity:
- Documents created/updated:
- Unresolved unknowns:

### Architecture
- Findings:
- Approved improvement:

### Implementation
- Files changed:
- Behaviour/invariants preserved:
- Risks/migration:

### Validation
| Check | Command | Result |
|---|---|---|
| Unit tests | ... | Passed/Failed/Not run |
| Integration tests | ... | ... |
| Type/lint/build | ... | ... |

### Documentation
| File | Token count | Method | Result |
|---|---:|---|---|

### Remaining work
- Risks:
- Deferred opportunities:
- Next recommended increment:
```

## Repeat/stop criteria

Repeat only when:
- A remaining issue has meaningful impact.
- Evidence is sufficient to justify action.
- A feasible validation path exists.
- The user has approved the next change where required.

Stop when remaining opportunities are speculative, low-impact, too costly, outside scope or lack a safe validation path.
