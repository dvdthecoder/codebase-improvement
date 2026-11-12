# Illustrative Sample Assessment

This example demonstrates the expected shape of an architecture assessment. It is fictional and is not evidence from a real production system.

Scenario: a small service has HTTP route handlers that perform request parsing, business rules and persistence directly. Two routes duplicate the same order validation.

The correct skill workflow would first inspect source, tests and runtime configuration, then document the current behaviour. Only after the baseline maturity gate would it record a finding and ask the user to approve a bounded improvement.

See:
- [Illustrative findings](findings.md)
- [Evidence-to-change traceability](traceability.md)
