# Codebase Improvement

A portable Agent Skill for understanding an existing repository, establishing trustworthy baseline documentation, improving architecture through evidence-based and approved changes, and keeping documentation synchronized with implementation.

For an agent, a repository's code and documentation are the context it works from. This skill makes that context trustworthy, measures it with the **Steer score**, and then improves the code against it.

The workflow is deliberately **documentation-first**:

1. Discover the repository, record its starting Steer score, and create a run branch.
2. Establish or repair baseline documentation of the current system: architecture, glossary and agent instructions (`AGENTS.md`), aiming for Steer level L3. Commit it as the **Baseline commit**.
3. Assess architecture against the verified baseline and source code.
4. Propose improvements and obtain approval at the configured decision gates.
5. Implement selected changes and validate them.
6. Update documentation to describe the verified new state, and commit each approved improvement as its own **Improvement commit**.
7. Run consistency, token-budget and Steer checks.
8. Repeat only when another worthwhile improvement exists, then generate the run report.

## Key guarantees

- No architectural recommendations based solely on undocumented assumptions.
- No application-code changes before the user approves the proposed improvement.
- No claims that tests, builds, or checks passed unless they were executed.
- Every generated Markdown/text documentation file must remain below **5,000 tokens**.
- A preferred target of **4,200 tokens** leaves room for tokenizer differences and later edits.
- Existing repository conventions and user changes are preserved.
- The skill does not refactor indefinitely; it stops when remaining opportunities are low-value or speculative.
- The skill commits only on its own run branch, never on the branch you had checked out, and never pushes or merges.
- No documentation is written just to pass a Steer check; a check that cannot be passed honestly stays failed, with the reason.

## Repository layout

| Path | Contents |
|---|---|
| `skills/codebase-improvement/` | The skill: `SKILL.md`, `references/` (loaded per phase), `scripts/` (validators, `score_steer.py`, `render_report.py`) and `assets/` (doc templates) |
| `docs/adr/` | Decisions about this skill's design |
| `examples/` | Fixtures and a sample assessment |
| `tests/` | Self-checks for the scripts |
| `CONTEXT.md` | Glossary of this project's terms |
| `AGENTS.md` | Instructions for agents working on this repository |

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

## Usage

After installing, open the target repository in your agent and ask for the skill by name. The mode decides how far it goes.

| Mode | What it does | Example prompt |
|---|---|---|
| **Interactive** (default) | Full loop. Stops for your approval before any code change. | `Use the codebase-improvement skill on this repository. Limit this run to one improvement.` |
| **Assessment-only** | Baseline docs and findings; no code changes. | `Use the codebase-improvement skill in assessment-only mode. You may write documentation.` |
| **Score-only** | Steer score explained; changes nothing. | `Use the codebase-improvement skill in score-only mode.` |
| **Autonomous** | Implements low-risk changes without asking. Still stops for risky ones. | `Use the codebase-improvement skill in autonomous mode.` |

The prompts work the same in Claude Code, Codex and OpenCode. Claude Code also accepts `/codebase-improvement`.

What you get from an interactive run:

1. A branch `codebase-improvement/<date>` with one Baseline commit (docs only) and one Improvement commit per approved change.
2. Updated `docs/` (including `docs/glossary.md`) and `AGENTS.md`.
3. A final report in the chat, including the Steer score before and after.
4. An HTML run report at `.git/codebase-improvement/report.html`.

Review the branch, then merge or delete it.

### Running the scripts directly

The scripts need only Python 3.10+. After installing, they are in the skill folder, for example `.claude/skills/codebase-improvement/scripts/` or `.agents/skills/codebase-improvement/scripts/`. To score many repositories, install globally (`-g`) or use a clone of this repository:

```bash
git clone https://github.com/dvdthecoder/codebase-improvement.git ~/codebase-improvement
python ~/codebase-improvement/skills/codebase-improvement/scripts/score_steer.py --batch ~/projects/*/
```

## Steer score

For an agent, a repository's documentation is the context it works from. The Steer score measures how well that documentation steers an agent: 13 read-only checks give points out of 100 and a level on a ladder.

| Level | Name | Meaning |
|---|---|---|
| L0 | Undescribed | No usable README |
| L1 | Described | A human can tell what it is and how to run it |
| L2 | Engineered | Architecture, glossary, test command and working links |
| L3 | Steerable | Agent instructions, references that resolve, coverage, context-sized docs |
| L4 | Self-maintaining | Decision records, fresh docs and CI documentation checks |

A level counts only when it and every lower level pass in full.

```bash
# One repository, check by check
python skills/codebase-improvement/scripts/score_steer.py --repo <target-repo>

# Many repositories: one row each, then a count per level
python skills/codebase-improvement/scripts/score_steer.py --batch ~/projects/*/
```

Ask the agent for **score-only** mode to get the score explained. Improvement runs score before and after, aim for L3 during the baseline, and record the score in commit trailers. See [references/steer-score.md](skills/codebase-improvement/references/steer-score.md).

## Run record and report

The skill records each run on its own branch, `codebase-improvement/<date>`, and never touches the branch you had checked out:

- one **Baseline commit**: documentation of the current system, with no code changes;
- one **Improvement commit** per approved change: code, tests and updated documentation, with the finding, evidence and validation results in the commit message.

At the end of the run it generates an HTML report from those commits:

```bash
python skills/codebase-improvement/scripts/render_report.py --repo <target-repo>
# Wrote <target-repo>/.git/codebase-improvement/report.html
```

The report lives inside `.git/`, so it is never committed. Rebuild it at any time from the branch. Review the branch, then merge or discard it as one unit.

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

These are teaching fixtures. A headless assessment-only run on a git copy of `missing-docs` moved it from Steer **8 L0** to **77 L1** in one Baseline commit. It stayed at L1 because the fixture has no test suite, and the skill did not invent a test command.

## Design principles

- **Source code is authoritative for current behaviour.** Documentation is evidence about intent and a navigation aid, not proof that implementation matches it.
- **Baseline before redesign.** Document enough of the existing system to make architectural reasoning grounded.
- **Approval before material changes.** The default workflow is interactive.
- **Small, reversible changes.** Prefer focused changes with clear validation.
- **Documentation as a maintained artifact.** Update it in the same change as the implementation.
- **Bounded context.** Load supporting references only when the task needs them.

## Customization

The default workflow is interactive. A user may explicitly request autonomous, assessment-only or score-only mode (see [Usage](#usage)). Even in autonomous mode, do not perform destructive, externally visible, security-sensitive, data-migrating, or public-contract changes without explicit approval.

The 5,000-token limit applies to each generated documentation file, not to the combined repository. Do not split a document mechanically: split by coherent topic and preserve navigation.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Report security issues using [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
