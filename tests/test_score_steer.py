"""Self-check for score_steer.py: an L1 repo, an L3 repo, and the ladder gate."""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/codebase-improvement/scripts"))
import score_steer  # noqa: E402

WORDS = " ".join(["word"] * 160)
L1 = {"README.md": f"# Shop\n\n{WORDS}\n\n```bash\npython -m shop\n```\n", "shop/orders.py": "x = 1\n"}
L3 = {
    **L1,
    "README.md": L1["README.md"] + "\nRun tests with `pytest`. See [docs](docs/README.md).\n",
    "docs/README.md": "# Docs\n\n## Architecture\n\n`shop/orders.py` owns orders; `shop/billing.py` bills them.\n",
    "docs/glossary.md": "# Glossary\n\n" + "".join(f"**Term{i}**:\nDef.\n\n" for i in range(5)),
    "shop/billing.py": "y = 2\n",
    "AGENTS.md": "# Agents\n\nRun `pytest` before committing.\n",
}


def build(files, git=False):
    repo = Path(tempfile.mkdtemp())
    for name, text in files.items():
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text)
    if git:
        for cmd in (["init", "-q"], ["add", "-A"],
                    ["-c", "user.name=t", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "init"]):
            subprocess.run(["git", "-C", str(repo), *cmd], check=True)
    return repo


def level_of(files, git=False):
    checks = score_steer.score(build(files, git))
    return score_steer.summarize(checks), {c.id: c.passed for c in checks}


def main():
    (points, level), _ = level_of(L1)
    assert level == 1, (points, level)

    (points3, level3), passed = level_of(L3, git=True)
    assert level3 == 3, passed
    assert points3 > points
    assert passed["4.2"] and not passed["4.1"]          # fresh, but no decision records

    # Gate: agent instructions without architecture/glossary/test docs stay at L1.
    (_, gated), passed = level_of({**L1, "AGENTS.md": "# Agents\n"})
    assert gated == 1 and passed["3.1"], passed

    # A stale reference fails 3.2; prose with a slash is not treated as a path.
    broken = {**L3, "docs/README.md": L3["docs/README.md"] + "`shop/gone.py` and `try/finally`\n"}
    (_, lvl), passed = level_of(broken)
    assert not passed["3.2"] and lvl == 2, passed
    # Uncommitted docs count: scoring before a commit must match scoring after it.
    repo = build(L1, git=True)
    for name in ("AGENTS.md", "docs/glossary.md"):
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(L3[name])
    passed = {c.id: c.passed for c in score_steer.score(repo)}
    assert passed["3.1"] and passed["2.2"] and passed["4.2"], passed
    print("score_steer self-check: OK")


if __name__ == "__main__":
    main()
