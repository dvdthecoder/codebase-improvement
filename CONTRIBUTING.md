# Contributing

Thanks for helping improve Codebase Improvement.

## Principles

- Keep the skill portable across Agent Skills-compatible tools.
- Keep `SKILL.md` concise; put detailed procedures in `references/`.
- Preserve the documentation-first workflow.
- Do not weaken approval or validation gates without explaining the trade-off.
- Keep every individual Markdown/text file below 5,000 tokens.
- Prefer no new runtime dependencies for validation scripts.

## Changes

1. Open an issue describing the problem or proposed improvement.
2. Make a focused change.
3. Update relevant references and examples.
4. Run all validators:

   ```bash
   python skills/codebase-improvement/scripts/check_doc_tokens.py --directory .
   python skills/codebase-improvement/scripts/check_documentation.py --directory skills/codebase-improvement
   python skills/codebase-improvement/scripts/validate_links.py --directory .
   ```

5. Explain compatibility impact for any changes to skill metadata or installation instructions.

## Pull requests

Include:
- Problem and motivation.
- Behavioural change to the skill.
- Example before/after, where useful.
- Validation commands and results.
- Any known limitation.

Do not claim checks passed unless they were run.
