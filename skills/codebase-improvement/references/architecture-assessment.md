# Architecture Assessment

## Objective

Identify architectural changes that reduce the cost and risk of future change while preserving required behaviour. Assess the actual code and verified baseline, not aesthetics or fashionable patterns.

## 1. Assessment dimensions

### Module depth and interface leverage

A deep module hides substantial implementation complexity behind a small, stable interface. A shallow module exposes a complicated interface while providing little implementation value.

Ask:
- Does the interface simplify the caller's task?
- Are callers forced to understand internal sequencing or data structures?
- Does the module own a coherent responsibility?
- Can implementation change without forcing widespread caller changes?

### Cohesion and responsibility

Look for modules that combine unrelated reasons to change, and responsibilities scattered across many modules. Identify the domain concept or invariant that should own the behaviour.

### Coupling and dependency direction

Inspect:
- Direct and transitive dependencies.
- Cycles and bidirectional knowledge.
- Shared mutable state.
- Callbacks and event contracts.
- Import-time side effects.
- Dependencies on implementation details.
- Cross-layer or cross-domain access.

A dependency is not automatically harmful. Explain the change cost or constraint it creates.

### Change locality

Trace representative changes through code. Count the modules, files, contracts and tests a change touches. Use Git history as one signal: repeated coordinated edits may indicate a boundary problem, but can also reflect normal feature work.

### Data and consistency boundaries

Determine who owns data, who may mutate it, and where invariants are enforced. Look for duplicated validation, competing sources of truth, unclear transaction boundaries and implicit lifecycle coupling.

### Failure and operational boundaries

Where relevant, assess retries, timeouts, idempotency, error translation, observability, resource ownership and degradation behaviour.

### Testability

Assess whether module contracts can be tested independently, whether tests assert externally meaningful behaviour, and whether integration boundaries can be exercised without fragile global setup.

## 2. Useful heuristics

### Deletion test

If a module were removed, would its complexity disappear behind a smaller interface or spread across its callers? The latter may indicate that the module is shallow or its responsibility is misplaced.

### Change propagation test

Choose a representative change. Trace the required edits and explain why each location changes. Repeated synchronized edits may indicate missing encapsulation or an unstable contract.

### Knowledge test

How many implementation details must a caller know to use the module correctly? A caller that must reproduce internal sequencing or error handling may indicate a leaky boundary.

### Ownership test

Can one component explain and enforce a domain invariant? If several components partially own it, identify the resulting inconsistency risk.

### Counterfactual test

Would the proposed abstraction still be useful if the immediate feature request disappeared? Avoid abstractions created solely to make one diff look cleaner.

## 3. Evidence requirements

Each finding should include:

- Unique ID.
- Priority and confidence.
- Paths and symbols.
- Observed call/dependency/data flow.
- Relevant tests or history, if used.
- Current cost or risk.
- Proposed intervention.
- Expected result and validation method.
- Alternatives considered.
- Risks and migration effort.

Avoid unsupported labels such as "monolith", "spaghetti code" or "poor architecture". Describe observable properties.

## 4. Prioritization

Use qualitative scoring unless the repository provides meaningful metrics. Consider:

- Impact on delivery, reliability, security or operability.
- Frequency of change and number of affected callers.
- Blast radius and severity of failure.
- Confidence in the diagnosis.
- Cost and reversibility of the change.
- Opportunity to reduce repeated work.

Prioritize high-impact, high-confidence, bounded improvements. Do not use an arbitrary numeric score as a substitute for rationale.

## 5. Findings format

```markdown
## ARCH-001 — [Short finding]

- Priority: High / Medium / Low
- Confidence: Strong / Moderate / Speculative
- Evidence: `path/to/file.ext::Symbol`
- Current behaviour: ...
- Problem: ...
- Why it matters: ...
- Proposed change: ...
- Expected benefit: ...
- Validation: ...
- Risks and migration: ...
- Alternatives: ...
```

## 6. Approval boundary

Present the assessment and recommend a small first increment. Wait for approval before changing application code in the default interactive mode.

Seek explicit approval for changes to:
- Public APIs, events or extension contracts.
- Persistent schemas, migrations or data retention.
- Authentication, authorization or security posture.
- Deployment topology or infrastructure.
- Externally visible behaviour.
- Destructive operations or irreversible transformations.

## 7. Avoid

- Refactoring only to match personal style.
- Introducing patterns without a demonstrated problem.
- Splitting modules into many tiny wrappers.
- Replacing a working design solely because a different architecture is fashionable.
- Optimizing based on guessed performance bottlenecks.
- Treating file count or lines of code as direct measures of quality.
- Using generated diagrams as evidence without checking source relationships.
