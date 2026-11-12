# Illustrative Traceability

> Fictional example. Replace all paths and results with repository evidence.

| Finding | Baseline evidence | Approved change | Validation | Documentation |
|---|---|---|---|---|
| ARCH-001 | Two route handlers duplicate order constraints | Extract domain operation | Domain unit tests and both route tests | `docs/architecture/components.md`; `docs/reference/interfaces.md` |

## Completion evidence

Record actual commands and outcomes:

| Check | Command | Result |
|---|---|---|
| Unit tests | `python -m pytest tests/unit` | Not run in this example |
| Route tests | `python -m pytest tests/routes` | Not run in this example |

Do not turn illustrative results into claims of executed validation.
