# Refactoring and Implementation Guidelines

## Purpose

Turn an approved architectural finding into a controlled, testable change.

## 1. Define the change contract

Before editing, record:

- Approved finding and scope.
- Existing externally observable behaviour to preserve.
- New or changed interface.
- Invariants and ownership rules.
- Affected callers, data and integrations.
- Tests to add or update.
- Rollback or compatibility approach.
- Explicit non-goals.

If implementation reveals that the approved scope is insufficient or materially different, stop and request approval for the revised plan.

## 2. Prefer incremental transformations

A safe sequence is often:

1. Add or strengthen tests around current behaviour.
2. Introduce the new interface or seam.
3. Move one responsibility behind it.
4. Migrate callers incrementally.
5. Remove obsolete paths only after confirming they are unused.
6. Run targeted and broader validation.
7. Update documentation and ADRs.

This sequence is illustrative; adapt it to the language and system.

## 3. Interface design

A good interface:
- Expresses domain intent rather than implementation mechanics.
- Hides sequencing and representation details where practical.
- Has clear inputs, outputs and error semantics.
- Makes invalid states difficult to express.
- Avoids exposing mutable internals.
- Minimizes caller knowledge.
- Has an explicit ownership and compatibility policy.

Do not add an interface layer that merely forwards every call without reducing coupling or complexity.

## 4. Compatibility and migration

Check:
- Public callers and downstream consumers.
- Serialized formats and persisted records.
- API/event versioning.
- Configuration and environment variable names.
- Deployment ordering and mixed-version operation.
- Data migration, rollback and backup requirements.
- Operational dashboards, alerts and runbooks.

Use expand-and-contract migrations where appropriate. Do not execute migrations, production deployments or destructive data operations without explicit authorization.

## 5. Tests

Choose tests that validate the contract at the right level:

- Unit tests for local rules and invariants.
- Component tests for module interfaces.
- Integration tests for persistence and external boundaries.
- Contract tests for public APIs/events.
- End-to-end tests for critical user journeys.

Avoid rewriting tests merely to make them pass. Explain any changed expectation and why the behaviour contract changed.

## 6. Tool and command safety

- Inspect scripts and commands before running unfamiliar repository automation.
- Prefer targeted commands before broad test suites.
- Do not install dependencies or alter lockfiles without need and approval where required.
- Do not expose secrets in terminal output, diffs or reports.
- Do not use destructive cleanup commands on user data.
- Preserve uncommitted changes.
- Do not commit, push, publish, deploy or open external pull requests unless requested.

## 7. Diff review

Before declaring implementation complete:
- Review the entire diff.
- Check for unrelated formatting or generated files.
- Check imports and dependency direction.
- Check error paths and resource cleanup.
- Check test coverage for the changed contract.
- Check compatibility and migration notes.
- Confirm no temporary debug code or secrets remain.

## 8. Report honestly

List exact checks and results. Separate:
- Passed.
- Failed.
- Not run.
- Blocked by environment or missing dependency.

A code change is not validated merely because it looks correct in a diff.
