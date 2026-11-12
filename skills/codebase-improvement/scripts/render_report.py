#!/usr/bin/env python3
"""Render a run report (HTML) from a run's Baseline and Improvement commits."""
from __future__ import annotations

import argparse
import html
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TRAILER = "Codebase-Improvement"
DOC_SUFFIXES = {".md", ".mdx", ".txt", ".rst"}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout


def run_commits(repo: Path) -> tuple[dict, list[dict]]:
    """Return (baseline, later commits oldest-first) for the most recent run reachable from HEAD."""
    fmt = f"%H%x1f%s%x1f%(trailers:key={TRAILER},valueonly,separator=%x2C)%x1f%B%x1e"
    newer: list[dict] = []
    for record in git(repo, "log", f"--format={fmt}", "HEAD").split("\x1e"):
        if not record.strip():
            continue
        sha, subject, trailer, body = record.strip("\n").split("\x1f", 3)
        commit = {"sha": sha, "subject": subject, "id": trailer.strip(), "body": body.strip()}
        if commit["id"] == "baseline":
            return commit, list(reversed(newer))
        newer.append(commit)
    raise LookupError(f"no commit with trailer '{TRAILER}: baseline' is reachable from HEAD")


def changed_files(repo: Path, sha: str) -> list[str]:
    return [p for p in git(repo, "show", "--format=", "--name-only", sha).splitlines() if p]


def pre(text: str, cls: str = "") -> str:
    return f'<pre class="{cls}">{html.escape(text)}</pre>'


def diff_block(repo: Path, sha: str) -> str:
    rows = []
    for line in git(repo, "show", "--format=", "--patch", "--no-color", sha).splitlines():
        cls = ""
        if line.startswith(("diff ", "index ", "--- ", "+++ ")):
            cls = "f"
        elif line.startswith("@@"):
            cls = "h"
        elif line.startswith("+"):
            cls = "a"
        elif line.startswith("-"):
            cls = "d"
        rows.append(f'<span class="{cls}">{html.escape(line) or " "}</span>')
    return '<div class="diff">' + "\n".join(rows) + "</div>"


def commit_section(repo: Path, c: dict, heading: str) -> str:
    files = changed_files(repo, c["sha"])
    return (
        f'<section><h3>{html.escape(heading)}</h3>'
        f'<p class="meta"><code>{c["sha"][:10]}</code> · {len(files)} file(s)</p>'
        f'<details open><summary>Commit message</summary>{pre(c["body"])}</details>'
        f'<details><summary>Diff</summary>{diff_block(repo, c["sha"])}</details></section>'
    )


def render(repo: Path) -> str:
    baseline, later = run_commits(repo)
    improvements = [c for c in later if c["id"]]
    others = [c for c in later if not c["id"]]
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    try:
        base = git(repo, "rev-parse", "--short", f"{baseline['sha']}^").strip()
    except subprocess.CalledProcessError:
        base = "(root)"  # baseline is the repository's first commit

    docs = []
    for path in changed_files(repo, baseline["sha"]):
        if Path(path).suffix.lower() not in DOC_SUFFIXES:
            continue
        try:
            text = git(repo, "show", f"{baseline['sha']}:{path}")
        except subprocess.CalledProcessError:
            continue  # deleted in the baseline commit
        docs.append(f'<details><summary><code>{html.escape(path)}</code></summary>{pre(text, "doc")}</details>')

    parts = [
        "<h2>Documentation</h2>",
        commit_section(repo, baseline, baseline["subject"]),
        "<h3>Baseline documents</h3>" + ("".join(docs) or "<p>No documentation files in this commit.</p>"),
        f"<h2>Improvements ({len(improvements)})</h2>",
        "".join(commit_section(repo, c, f'{c["id"]}: {c["subject"]}') for c in improvements)
        or "<p>No Improvement commits in this run.</p>",
    ]
    if others:
        parts.append(f"<h2>Other commits ({len(others)})</h2><p>Commits after the baseline without a "
                     f"<code>{TRAILER}</code> trailer.</p>")
        parts += [commit_section(repo, c, c["subject"]) for c in others]

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return PAGE.format(
        title=html.escape(repo.resolve().name),
        branch=html.escape(branch), base=html.escape(base), generated=generated,
        body="\n".join(parts),
    )


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Run report: {title}</title>
<style>
:root {{ --bg:#f7f8f7; --fg:#1d2420; --muted:#5d6b63; --line:#dde3df; --code:#eef1ef;
  --add:#e6f4ea; --add-fg:#1f6b35; --del:#fbe9e7; --del-fg:#a3352a; --accent:#2f6f5a; color-scheme:light; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#121614; --fg:#e3e9e5; --muted:#95a39b; --line:#2b3430;
  --code:#1d2421; --add:#16301f; --add-fg:#8fd6a2; --del:#3a1d1a; --del-fg:#f0a59b; --accent:#7cc3a6; color-scheme:dark; }} }}
body {{ background:var(--bg); color:var(--fg); font:15px/1.55 system-ui, sans-serif; margin:0; }}
main {{ max-width:1000px; margin:0 auto; padding:28px 16px 64px; }}
h1 {{ margin:0 0 4px; font-size:26px; }} h2 {{ margin-top:36px; border-bottom:1px solid var(--line); padding-bottom:6px; }}
.meta {{ color:var(--muted); margin:0 0 10px; }}
code, pre, .diff {{ font-family:ui-monospace, Menlo, monospace; font-size:12.5px; }}
pre {{ background:var(--code); padding:12px 14px; border-radius:6px; overflow-x:auto; white-space:pre-wrap; }}
pre.doc {{ white-space:pre-wrap; font-size:13px; line-height:1.5; }}
details {{ margin:8px 0; }} summary {{ cursor:pointer; color:var(--accent); }}
section {{ border:1px solid var(--line); border-radius:8px; padding:4px 16px 12px; margin:14px 0; }}
.diff {{ background:var(--code); border-radius:6px; overflow-x:auto; padding:8px 0; white-space:pre; }}
.diff span {{ display:block; padding:0 14px; min-width:max-content; }}
.diff .a {{ background:var(--add); color:var(--add-fg); }} .diff .d {{ background:var(--del); color:var(--del-fg); }}
.diff .h {{ color:var(--accent); }} .diff .f {{ color:var(--muted); }}
</style></head><body><main>
<h1>Run report: {title}</h1>
<p class="meta">Branch <code>{branch}</code> · base <code>{base}</code> · generated {generated} from git history</p>
{body}
</main></body></html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    try:
        page = render(args.repo)
        out = Path(git(args.repo, "rev-parse", "--absolute-git-dir").strip()) / "codebase-improvement" / "report.html"
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git failed: {exc.stderr.strip()}", file=sys.stderr)
        return 1
    except LookupError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
