# Baseline Documentation

## Purpose

Establish a trustworthy description of the repository's current implementation before architectural assessment. Baseline documentation is a model of what exists, not a design proposal.

## 1. Inventory documentation

Find and inspect:

- Root and nested README files.
- `docs/`, wiki exports and developer portals.
- Architecture diagrams and system context documents.
- ADRs and design proposals.
- API specifications and schema documentation.
- Deployment, operations and incident runbooks.
- Configuration and environment references.
- Test strategy and contributor guides.
- Inline comments and docstrings for critical or surprising behaviour.

Record each document's scope, apparent owner, last relevant update (if available), and whether its claims match source.

Do not assume a recently modified document is accurate or an old document is wrong.

## 2. Build an implementation map

Inspect evidence in a deliberate order:

1. Project manifests and lockfiles.
2. Build, test and CI configuration.
3. Runtime entry points and application bootstrap.
4. Routing, command handlers, event consumers and scheduled jobs.
5. Domain models, services and business rules.
6. Persistence adapters, schemas and migrations.
7. External API clients, queues and integration boundaries.
8. Authentication, authorization and secret/configuration handling.
9. Logging, metrics, tracing and error handling.
10. Tests and fixtures that demonstrate expected behaviour.

Use repository-native tools when available. Do not run arbitrary scripts simply because they are present; inspect them first.

## 3. Minimum baseline contents

Adapt to the system; do not create empty sections.

### System overview

- What the system does and does not do.
- Main users or calling systems, if evidenced.
- Runtime/deployment shape.
- Main technology choices and versions when relevant.

### Architecture

- System context and trust boundaries.
- Major components and responsibilities.
- Dependency direction and important interfaces.
- Startup and request/event execution paths.
- Important synchronous and asynchronous flows.

### Data

- Key entities and ownership.
- Persistence systems and important schemas.
- Data lifecycle, transformations and consistency expectations.
- External data exchanges.

### Interfaces and integrations

- Public APIs, commands, events or extension points.
- Authentication and authorization boundaries.
- External services and failure behaviour.
- Versioning and compatibility notes.

### Operation and development

- Configuration and environment variables (never include secret values).
- Build, test and local development commands.
- Deployment and runtime requirements.
- Observability and operational failure modes.

### Known limitations

- Verified architectural constraints.
- Missing tests or documentation.
- Unresolved questions and assumptions.
- Areas not inspected.

### Glossary

Record the repository's domain vocabulary in `docs/glossary.md`, using `assets/documentation-template/glossary.md`. If the repository already has a glossary or a `CONTEXT.md`, update that file instead of creating a second one.

- Include domain terms: the nouns and verbs a domain expert would use (for example *merge request*, *candidate*, *enrichment*). Exclude general programming terms and implementation details such as class names, frameworks or file layout.
- Give each term a one-line definition, the code symbol that evidences it, and the synonyms to avoid.
- When the code uses several words for one concept (*MR*, *merge request*, *PR*), pick the canonical term and list the others under *Avoid*.
- When one word means different things in different places, flag it under *Ambiguities* rather than guessing.
- Skip the glossary only when the repository has no domain vocabulary beyond general programming terms, and say so in the final report.

## 4. Evidence and confidence

Use explicit labels in working notes and, where helpful, in documents:

- **Verified:** directly supported by source, tests, schema, configuration or an executed observation.
- **Inferred:** plausible interpretation supported by multiple clues, but not directly proven.
- **Unknown:** evidence is absent, contradictory or inaccessible.

For important claims, record source paths and symbols. Prefer stable references such as `src/orders/service.py::OrderService.create` over line numbers that will quickly drift.

Tests show intended or asserted behaviour; they do not prove every production path. Configuration shows possible deployment settings; it does not prove which values are used in production.

## 5. Documentation maturity gate

Rate critical areas:

| Status | Meaning | Action |
|---|---|---|
| Adequate | Accurate enough for the scoped assessment | Proceed |
| Needs improvement | Useful but incomplete or stale in material areas | Repair critical gaps |
| Missing | No usable documentation or map | Reverse-engineer and create |
| Unable to verify | Evidence unavailable or contradictory | Ask, constrain scope or record uncertainty |

Critical areas normally include entry points, component boundaries, key data ownership and major execution flows. What is critical depends on the repository and requested scope.

Do not block on missing low-impact details. Do block when unresolved uncertainty could reverse an architectural recommendation or create material risk.

## 6. Baseline outputs

Prefer a compact structure aligned to existing repository conventions. A possible layout:

```text
docs/
  README.md
  glossary.md
  architecture/
    overview.md
    components.md
    data-flows.md
  reference/
    interfaces.md
    configuration.md
    operations.md
  development/
    testing.md
  adr/
    README.md
```

Use fewer documents when the system is small. Split documents when topics have distinct audiences or the token budget requires it.

## 7. Baseline integrity

- Do not silently replace existing documents; inspect and preserve useful context.
- Do not present proposed future architecture as current.
- Do not invent deployment details, SLAs, scale, security controls or operational practices.
- Do not expose credentials, tokens, private keys or sensitive user data.
- Mark diagrams as current-state diagrams and include enough detail to trace them to code.
- Record unresolved questions instead of filling gaps with plausible fiction.
- Keep each generated text/Markdown file strictly below 5,000 tokens; target 4,200.
