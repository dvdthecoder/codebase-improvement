"""Self-check for render_report.py: builds a throwaway repo with one run and inspects the report."""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/codebase-improvement/scripts/render_report.py"


def sh(repo, *args):
    return subprocess.run(args, cwd=repo, check=True, capture_output=True, text=True).stdout


def commit(repo, files, message):
    for name, text in files.items():
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text)
    sh(repo, "git", "add", "-A")
    (repo / ".msg").write_text(message)
    sh(repo, "git", "commit", "-q", "-F", ".msg")
    (repo / ".msg").unlink()


def main():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        sh(repo, "git", "init", "-q", "-b", "main")
        sh(repo, "git", "config", "user.email", "t@example.invalid")
        sh(repo, "git", "config", "user.name", "test")

        # No run yet: the script must fail clearly.
        commit(repo, {"app.py": "print(1)\n"}, "initial")
        r = subprocess.run([sys.executable, "-B", str(SCRIPT), "--repo", str(repo)], capture_output=True, text=True)
        assert r.returncode == 1 and "no commit with trailer" in r.stderr, r.stderr

        commit(repo, {"docs/README.md": "# Baseline <doc>\n"},
               "docs: baseline documentation\n\nMaturity: Adequate\n\nCodebase-Improvement: baseline\n")
        commit(repo, {"app.py": "print(2)\n"},
               "refactor: tidy (ARCH-001)\n\nFinding: dup\nValidation:\npytest: 1 passed\n\nCodebase-Improvement: ARCH-001\n")
        commit(repo, {"notes.txt": "x\n"}, "user commit without trailer")

        out = sh(repo, sys.executable, "-B", str(SCRIPT), "--repo", str(repo))
        page = (repo / ".git/codebase-improvement/report.html").read_text()
        assert "Wrote" in out
        docs, rest = page.split("<h2>Improvements (1)</h2>")
        improvements, others = rest.split("<h2>Other commits (1)</h2>")
        assert "Baseline &lt;doc&gt;" in docs and "Maturity: Adequate" in docs   # doc content, escaped
        assert "print(2)" not in docs                                            # code stays out of docs section
        assert "ARCH-001: refactor: tidy" in improvements and "pytest: 1 passed" in improvements
        assert "user commit without trailer" in others
        assert not (repo / "report.html").exists() and "report.html" not in sh(repo, "git", "status", "--porcelain")
    print("render_report self-check: OK")


if __name__ == "__main__":
    main()
