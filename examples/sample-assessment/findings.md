# Illustrative Architecture Findings

> Fictional example. Paths and symbols below are illustrative, not claims about a real codebase.

## ARCH-001 — Order validation is duplicated across route handlers

- Priority: Medium
- Confidence: Strong (within this fictional scenario)
- Evidence: `src/routes/create_order.py::create_order`; `src/routes/replace_order.py::replace_order`
- Current behaviour: both handlers parse order details and independently enforce the same domain constraints.
- Problem: a rule change can be implemented in one route but missed in the other.
- Why it matters: behaviour can diverge and change requires coordinated edits.
- Proposed change: move the shared invariant into an order-domain operation with a narrow input/output contract.
- Expected benefit: one authoritative implementation and focused tests.
- Validation: unit tests for the domain operation plus route-level tests for both handlers.
- Risks and migration: preserve existing response codes and error payloads.
- Alternatives: leave duplication if the rules are expected to diverge; evidence should decide.

## Approval

In interactive mode, present this finding and wait for the user to approve the selected improvement and implementation approach before changing application code.
