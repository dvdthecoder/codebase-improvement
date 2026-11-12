# Codebase Improvement

A portable Agent Skill for understanding an existing repository, establishing trustworthy baseline documentation, improving architecture through evidence-based and approved changes, and keeping documentation synchronized with implementation.

The workflow is deliberately **documentation-first**:

1. Discover the repository and its existing evidence.
2. Establish or repair baseline documentation of the current system.
3. Assess architecture against the verified baseline and source code.
4. Propose improvements and obtain approval at the configured decision gates.
5. Implement selected changes and validate them.
6. Update documentation to describe the verified new state.
7. Run consistency and token-budget checks.
8. Repeat only when another worthwhile improvement exists.

## Key guarantees

- No architectural recommendations based solely on undocumented assumptions.
- No application-code changes before the user approves the proposed improvement.
- No claims that tests, builds, or checks passed unless they were executed.
- Every generated Markdown/text documentation file must remain below **5,000 tokens**.
- A preferred target of **4,200 tokens** leaves room for tokenizer differences and later edits.
- Existing repository conventions and user changes are preserved.
- The skill does not refactor indefinitely; it stops when remaining opportunities are low-value or speculative.

## Repository layout

```text
codebase-improvement/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── SECURITY.md
├── CONTEXT.md
├── skills/
│   └── codebase-improvement/
│       ├── SKILL.md
│       ├── references/
│       │   ├── baseline-documentation.md
│       │   ├── architecture-assessment.md
│       │   ├── refactoring-guidelines.md
│       │   ├── technical-writing.md
│       │   └── quality-gates.md
│       ├── scripts/
│       │   ├── check_doc_tokens.py
│       │   ├── check_documentation.py
│       │   └── validate_links.py
│       └── assets/
│           └── documentation-template/
│               ├── architecture.md
│               ├── component.md
│               └── adr.md
├── examples/
│   ├── sample-assessment/
│   │   ├── README.md
│   │   ├── findings.md
│   │   └── traceability.md
│   └── fixtures/
│       ├── missing-docs/
│       │   └── src/
│       │       └── main.py
│       └── stale-docs/
│           ├── README.md
│           └── src/
│               └── main.py
└── .github/
    └── workflows/
        └── validate-skill.yml
```

## Installation

Install with the [`skills` CLI](https://github.com/vercel-labs/skills) (Node.js 22.20+). From the target repository root:

```bash
npx skills add dvdthecoder/codebase-improvement -a claude-code -a codex -a opencode
```

Add `-g` to install globally instead of into the current project. The CLI copies `skills/codebase-improvement/` into each agent's skill directory:

| Agent | Project | Global (`-g`) |
|-------|---------|---------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| OpenCode | `.agents/skills/` | `~/.config/opencode/skills/` |

Other Agent Skills-compatible tools supported by the CLI work the same way; pass their agent name with `-a`.

### Manual install

Without Node.js, copy the skill folder yourself. Keep the folder name `codebase-improvement`, because it is the skill's discovery name.

```bash
git clone https://github.com/dvdthecoder/codebase-improvement.git /tmp/codebase-improvement
mkdir -p .claude/skills   # or .agents/skills for Codex and OpenCode
cp -R /tmp/codebase-improvement/skills/codebase-improvement .claude/skills/
```

### Updating

Re-run `npx skills add dvdthecoder/codebase-improvement` (or the copy step) to pick up the latest release. Review local customizations before replacing an installed skill.

## Running the validators

Python 3.10+ is sufficient. The scripts use the standard library by default.

```bash
# Conservative built-in estimate; no third-party dependency
python skills/codebase-improvement/scripts/check_doc_tokens.py \
  --directory skills/codebase-improvement \
  --max-tokens 5000 \
  --target-tokens 4200

# Check documentation structure and common quality signals
python skills/codebase-improvement/scripts/check_documentation.py \
  --directory skills/codebase-improvement

# Check relative Markdown links
python skills/codebase-improvement/scripts/validate_links.py \
  --directory .
```

For a model-specific token count, install `tiktoken` and pass an encoding:

```bash
python -m pip install tiktoken
python skills/codebase-improvement/scripts/check_doc_tokens.py \
  --directory . \
  --max-tokens 5000 \
  --target-tokens 4200 \
  --encoding cl100k_base
```

The built-in estimator is intentionally conservative but is not an exact tokenizer. For strict model-specific enforcement, configure the encoding used by your target model and keep the 4,200-token working target.

## Example workflow

Try the skill against the supplied fixtures:

- `examples/fixtures/missing-docs/` demonstrates a repository with source code but no documentation.
- `examples/fixtures/stale-docs/` has a README claim that conflicts with the implementation. A correct run fixes the README and leaves `src/main.py` unchanged. The fixture itself does not reveal the mismatch.
- `examples/sample-assessment/` shows an illustrative assessment and evidence-to-change traceability format.

These examples are teaching fixtures, not a claim that the skill has been run against a production repository.

## Design principles

- **Source code is authoritative for current behaviour.** Documentation is evidence about intent and a navigation aid, not proof that implementation matches it.
- **Baseline before redesign.** Document enough of the existing system to make architectural reasoning grounded.
- **Approval before material changes.** The default workflow is interactive.
- **Small, reversible changes.** Prefer focused changes with clear validation.
- **Documentation as a maintained artifact.** Update it in the same change as the implementation.
- **Bounded context.** Load supporting references only when the task needs them.

## Customization

The default workflow is interactive. A user may explicitly request autonomous execution or assessment-only mode. Even in autonomous mode, do not perform destructive, externally visible, security-sensitive, data-migrating, or public-contract changes without explicit approval.

The 5,000-token limit applies to each generated documentation file, not to the combined repository. Do not split a document mechanically: split by coherent topic and preserve navigation.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Report security issues using [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
