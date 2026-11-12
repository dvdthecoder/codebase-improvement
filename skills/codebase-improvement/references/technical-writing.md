# Technical Writing Standards

## Purpose

Produce useful, accurate documentation of the verified implementation. Documentation is part of the engineering deliverable and must be updated with code changes.

## 1. Choose the document type

Use the Diátaxis model as a practical classification:

- **Tutorial:** learning-oriented, guided experience.
- **How-to guide:** task-oriented instructions for a specific goal.
- **Reference:** factual description of APIs, configuration, schemas or commands.
- **Explanation:** conceptual context, architecture and rationale.

Do not force every document into a category when a concise README is sufficient. Keep each document's purpose clear.

## 2. Writing style

- Put the most important information first.
- Use direct, specific headings.
- Prefer active voice and concrete verbs.
- Keep sentences focused.
- Explain unfamiliar domain terms.
- Use consistent names for components, interfaces and concepts.
- Distinguish requirements, defaults, examples and optional behaviour.
- State prerequisites and expected outcomes for procedures.
- Include error conditions and limitations where relevant.
- Avoid marketing language, vague claims and unnecessary repetition.

Use the terminology and conventions of the repository. Apply a consistent developer-documentation style rather than mechanically enforcing a style guide that conflicts with project conventions.

## 3. Accuracy and evidence

- Derive interfaces from actual declarations, schemas or route definitions.
- Verify commands against project scripts and CI.
- Verify configuration names against code and deployment manifests.
- Verify diagrams against source relationships.
- Use examples that are executable or clearly marked illustrative.
- Never invent availability, performance, security guarantees, SLAs or production topology.
- Label assumptions and unresolved questions.
- Do not include secret values or personal data.

Where useful, cite source paths and symbols. Avoid fragile line-number references unless the documentation tooling keeps them current.

## 4. Architecture documents

A useful architecture overview may include:
- Scope and system purpose.
- Context and external actors.
- Containers/processes or deployable units.
- Components and responsibilities.
- Important runtime/data flows.
- Interfaces and dependency direction.
- Key constraints and trade-offs.
- Links to detailed references and ADRs.

Use diagrams when they explain a relationship better than prose. Label diagrams as current state or proposed state. Keep them synchronized with implementation.

## 5. API and configuration reference

For each interface, document applicable:
- Purpose and owner.
- Method, route, operation or event name.
- Inputs and validation.
- Outputs and schemas.
- Authentication/authorization.
- Errors and retry semantics.
- Versioning and compatibility.
- Examples.

For configuration, document:
- Name.
- Purpose.
- Required/optional status.
- Default, if verified.
- Accepted format.
- Where it is consumed.
- Safe example without secret values.

## 6. Decision records

Use ADRs for consequential decisions, not every code change. Include context, decision, alternatives, consequences, status and date. Supersede old decisions rather than silently rewriting history when the decision history matters.

## 7. File and token budgets

- Hard maximum: fewer than 5,000 tokens per generated Markdown/text file.
- Target: no more than 4,200 tokens.
- Count the complete file, including frontmatter, headings, code blocks, tables and links.
- Use a tokenizer compatible with the target model when available.
- Otherwise use the provided conservative estimator and disclose that it is an estimate.
- Do not confuse bytes, characters, lines or words with tokens.
- Split only at coherent topic boundaries.
- Add a clear index and cross-links after splitting.
- Never truncate important content just to satisfy the limit.

## 8. Suggested structure

Adapt to repository size and conventions:

```text
docs/
  README.md
  architecture/
    overview.md
    components.md
    data-flows.md
  reference/
    interfaces.md
    configuration.md
  development/
    testing.md
  operations/
    runbook.md
  adr/
    README.md
    0001-example-decision.md
```

Do not create empty, duplicate or speculative files.

## 9. Documentation change review

Review documentation as code:
- Does each statement match the implementation?
- Are names, paths and commands valid?
- Are links working?
- Are examples safe and accurate?
- Are diagrams current?
- Are old claims removed or marked historical?
- Does each file have one coherent purpose?
- Does every file satisfy the token budget?
