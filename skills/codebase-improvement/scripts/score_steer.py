#!/usr/bin/env python3
"""Score how well a repository's documentation steers an agent (Steer score and level).

Read-only: inspects files and git history, never runs code from the scored repository.

    score_steer.py --repo <path>          one repository, check by check
    score_steer.py --batch <dir> [...]    one row per repository, then a count per level
"""
from __future__ import annotations

import argparse
import re
import subprocess
import time
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_doc_tokens import heuristic_count  # noqa: E402
from validate_links import LINK_RE, REF_RE, strip_anchor_and_query  # noqa: E402

# Tunable thresholds.
README_MIN_WORDS = 150
GLOSSARY_MIN_TERMS = 5
REFS_RESOLVE_MIN = 0.90
COVERAGE_MIN = 0.80
MAX_DOC_TOKENS = 5000
FRESH_DAYS = 90

LEVEL_NAMES = {0: "Undescribed", 1: "Described", 2: "Engineered", 3: "Steerable", 4: "Self-maintaining"}
DOC_SUFFIXES = {".md", ".mdx", ".rst"}
SOURCE_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".go", ".rs", ".java", ".kt", ".rb", ".php",
                   ".cs", ".swift", ".scala", ".c", ".cc", ".cpp", ".h", ".hpp", ".ex", ".exs", ".dart"}
MIN_DIR_MODULES = 5  # below this, coverage counts individual source files instead of directories
NOT_DOC_DIRS = {"template", "templates", "fixtures", "testdata", "documentation-template"}
SKIP_DIRS = {"node_modules", "vendor", "venv", "dist", "build", "third_party", "site-packages", "target", "out"}
NON_MODULE_DIRS = {"tests", "test", "__tests__", "spec", "specs", "testdata", "fixtures", "examples", "example",
                   "docs", "doc", "migrations", "__pycache__"}
TEST_CMD_RE = re.compile(
    r"\b(pytest|python3? -m (pytest|unittest)|(npm|yarn|pnpm|bun) (run )?test|go test|cargo test|make test|"
    r"mvn (\S+ )*test|\./gradlew (\S+ )*test|gradle test|dotnet test|rspec|tox|nox|deno test|vitest|jest|"
    r"phpunit|mix test|swift test)\b")
DOC_CI_RE = re.compile(
    r"markdownlint|markdown-link-check|lychee|\bvale\b|remark-lint|linkcheck|mkdocs build|sphinx-build|"
    r"validate_links|check_documentation|check_doc_tokens|score_steer", re.I)
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
FENCE_RE = re.compile(r"^```.*?\n(.+?)^```", re.M | re.S)
GLOSSARY_TERM_RE = re.compile(r"^\s*(?:[-*]\s+)?\*\*[^*\n]+\*\*|^\|(?!\s*-)[^|\n]+\|", re.M)
ARCH_HEADING_RE = re.compile(r"^#{2,3}\s*(architecture|components|system overview|modules)\b", re.M | re.I)


@dataclass
class Check:
    id: str
    level: int
    name: str
    passed: bool
    detail: str


def git(repo: Path, *args: str) -> str | None:
    try:
        return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                              text=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def list_files(repo: Path) -> list[str]:
    """Working-tree files not ignored by git (tracked plus new, uncommitted ones), else a filtered walk."""
    listed = (git(repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
              if git(repo, "rev-parse", "--show-toplevel") is not None else None)
    if listed is not None:
        # Score the working tree as it is now, so a run can score before committing.
        files = sorted({f for f in listed.split("\0") if f and (repo / f).is_file()})
    else:
        files = [p.relative_to(repo).as_posix() for p in repo.rglob("*") if p.is_file()]
    return [f for f in files if not any(part in SKIP_DIRS for part in f.split("/"))]


def is_doc(path: str) -> bool:
    parts = path.split("/")
    if any(p.startswith(".") for p in parts):
        return False  # installed skills, CI config and tool folders are not the repo's docs
    if any(p.lower() in NOT_DOC_DIRS for p in parts[:-1]):
        return False  # templates and fixtures describe other repositories
    return Path(path).suffix.lower() in DOC_SUFFIXES or parts[-1].upper() == "README"


def read(repo: Path, rel: str) -> str:
    try:
        return (repo / rel).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def source_modules(files: list[str]) -> set[str]:
    """Directories holding source files, or individual source files when there are few directories."""
    sources = []
    for f in files:
        p = Path(f)
        if p.suffix.lower() not in SOURCE_SUFFIXES or any(part.startswith(".") for part in p.parts):
            continue
        if any(part.lower() in NON_MODULE_DIRS for part in p.parts[:-1]) or p.name.startswith("test_"):
            continue
        if p.stem != "__init__":
            sources.append(p)
    dirs = {p.parent.as_posix() for p in sources if p.parent != Path(".")}
    if len(dirs) >= MIN_DIR_MODULES:
        return dirs | {p.stem for p in sources if p.parent == Path(".")}
    return {p.with_suffix("").as_posix() for p in sources}


def path_refs(text: str) -> list[str]:
    """Backticked spans that look like repository paths, with ::Symbol and :line suffixes removed."""
    refs = []
    for span in CODE_SPAN_RE.findall(text):
        token = span.strip().split("::")[0]
        token = re.sub(r":\d+(-\d+)?$", "", token)
        if (" " in token or "://" in token or token.startswith(("/", "~", "$", "-", "<"))
                or any(c in token for c in "*{}<>[]()=|,'\"")):
            continue
        if "/" in token or Path(token).suffix.lower() in SOURCE_SUFFIXES | DOC_SUFFIXES:
            refs.append(token.rstrip("/"))
    return refs


def score(repo: Path) -> list[Check]:
    files = list_files(repo)
    file_set = set(files)
    dirs = {str(Path(f).parent.as_posix()) for f in files} | {
        "/".join(f.split("/")[:i]) for f in files for i in range(1, f.count("/") + 1)}
    docs = [f for f in files if is_doc(f)]
    texts = {d: read(repo, d) for d in docs}
    all_text = "\n".join(texts.values())
    lower_names = {f.lower(): f for f in files}
    checks: list[Check] = []

    def add(cid: str, level: int, name: str, passed: bool, detail: str) -> None:
        checks.append(Check(cid, level, name, passed, detail))

    # L1 Described
    readme = next((lower_names[n] for n in ("readme.md", "readme.rst", "readme.mdx", "readme")
                   if n in lower_names), None)
    readme_text = texts.get(readme, "") if readme else ""
    words = len(readme_text.split())
    add("1.1", 1, "README", words >= README_MIN_WORDS,
        f"{readme}: {words} words (need {README_MIN_WORDS})" if readme else "no root README")
    # ponytail: any fenced block counts as a run command; tighten to shell-language fences if it over-passes.
    fences = [b for b in FENCE_RE.findall(readme_text) if b.strip()]
    add("1.2", 1, "How to run", bool(fences),
        f"{len(fences)} code block(s) in README" if fences else "no code block with a command in README")

    # L2 Engineered
    arch = [d for d in docs if re.search(r"(^|/)architecture(/|\.(md|mdx|rst)$)", d, re.I)] or \
           [d for d, t in texts.items() if ARCH_HEADING_RE.search(t)]
    add("2.1", 2, "Architecture", bool(arch), f"found in {arch[0]}" if arch else "no architecture doc or section")
    glossaries = [lower_names[n] for n in ("docs/glossary.md", "glossary.md", "context.md") if n in lower_names]
    terms = max((len(GLOSSARY_TERM_RE.findall(texts.get(g, read(repo, g)))) for g in glossaries), default=0)
    add("2.2", 2, "Glossary", terms >= GLOSSARY_MIN_TERMS,
        f"{glossaries[0]}: {terms} terms (need {GLOSSARY_MIN_TERMS})" if glossaries else "no glossary")
    test_cmd = TEST_CMD_RE.search(all_text)
    add("2.3", 2, "How to test", bool(test_cmd),
        f"documents `{test_cmd.group(0)}`" if test_cmd else "no test command in docs")
    broken = []
    for d, t in texts.items():
        targets = [m.group(1) or m.group(2) for m in LINK_RE.finditer(t)] + REF_RE.findall(t)
        for target in targets:
            parsed = urlsplit(target.strip())
            path = strip_anchor_and_query(target.strip())
            if parsed.scheme or parsed.netloc or not path:
                continue
            if not (repo / Path(d).parent / path).exists():
                broken.append(f"{d} -> {target}")
    add("2.4", 2, "Links", not broken, f"{len(broken)} broken, e.g. {broken[0]}" if broken else "no broken links")

    # L3 Steerable
    agent_files = [p for p in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md",
                               ".cursorrules") if p in file_set or (repo / p).is_file()]
    if (repo / ".cursor" / "rules").is_dir():
        agent_files.append(".cursor/rules/")
    add("3.1", 3, "Agent instructions", bool(agent_files),
        ", ".join(agent_files) if agent_files else "no AGENTS.md, CLAUDE.md or equivalent")
    # ponytail: suffix match is lenient (a same-named file elsewhere counts); match full paths if that over-passes.
    # A reference resolves when some file or directory ends with it, with or without the file extension,
    # so `webserver/server.py`, `server.py` and `listeners/OrderEventListener` match deeper paths.
    suffixes: set[str] = set()
    for f in [*files, *dirs]:
        parts = f.split("/")
        for i in range(len(parts)):
            tail = "/".join(parts[i:])
            suffixes.update({tail, str(Path(tail).with_suffix("")) if Path(tail).suffix else tail})
    top_level = {f.split("/")[0] for f in files}
    refs = []
    for d, t in texts.items():
        for r in path_refs(t):
            found = r in suffixes or (repo / Path(d).parent / r).exists()
            looks_like_path = Path(r).suffix.lower() in SOURCE_SUFFIXES | DOC_SUFFIXES or r.split("/")[0] in top_level
            if found or looks_like_path:  # skip prose such as `try/finally` or `read/write`
                refs.append((r, found))
    resolved = [r for r, found in refs if found]
    ratio = len(resolved) / len(refs) if refs else 0.0
    missing = [r for r, found in refs if not found]
    add("3.2", 3, "References are real", bool(refs) and ratio >= REFS_RESOLVE_MIN,
        f"{len(resolved)}/{len(refs)} resolve ({ratio:.0%}, need {REFS_RESOLVE_MIN:.0%})"
        + (f"; e.g. missing `{missing[0]}`" if missing else "") if refs else "docs name no code paths")
    modules = source_modules(files)
    mentioned = {m for m in modules if m in all_text or re.search(rf"\b{re.escape(Path(m).name)}\b", all_text)}
    # ponytail: a module counts as mentioned when its name appears anywhere; common names (utils) over-pass.
    cov = len(mentioned) / len(modules) if modules else 1.0
    unmentioned = sorted(modules - mentioned)
    add("3.3", 3, "Coverage", cov >= COVERAGE_MIN,
        f"{len(mentioned)}/{len(modules)} source modules mentioned ({cov:.0%}, need {COVERAGE_MIN:.0%})"
        + (f"; e.g. `{unmentioned[0]}`" if unmentioned else ""))
    sizes = {d: heuristic_count(t) for d, t in texts.items()
             if not re.match(r"(changelog|license|history)", Path(d).name, re.I)}
    big = sorted((s, d) for d, s in sizes.items() if s >= MAX_DOC_TOKENS)
    add("3.4", 3, "Fits in context", bool(docs) and not big,
        (f"{len(big)} doc(s) over {MAX_DOC_TOKENS} tokens, largest {big[-1][1]} (~{big[-1][0]})" if big
         else f"all {len(sizes)} doc(s) under {MAX_DOC_TOKENS} tokens (estimate)") if docs else "no docs")

    # L4 Self-maintaining
    adrs = [f for f in docs if re.match(r"(docs?/)?(adr|decisions)/", f, re.I) and not f.lower().endswith("readme.md")]
    add("4.1", 4, "Decisions", bool(adrs), f"{len(adrs)} decision record(s)" if adrs else "no docs/adr/ records")
    doc_time = git(repo, "log", "-1", "--format=%ct", "--", *docs) if docs else None
    if docs and (git(repo, "status", "--porcelain", "--", *docs) or "").strip():
        doc_time = str(int(time.time()))  # docs edited in the working tree are fresh as of now
    code_time = git(repo, "log", "-1", "--format=%ct", "--", ".", *[f":(exclude){d}" for d in docs])
    if doc_time and doc_time.strip() and code_time and code_time.strip():
        lag = (int(code_time) - int(doc_time)) / 86400
        add("4.2", 4, "Fresh", lag <= FRESH_DAYS,
            f"docs trail code by {max(lag, 0):.0f} days (limit {FRESH_DAYS})")
    else:
        add("4.2", 4, "Fresh", False, "no git history for docs and code")
    ci_files = [f for f in files if f.startswith(".github/workflows/") or f in
                (".gitlab-ci.yml", ".circleci/config.yml", "azure-pipelines.yml", "Jenkinsfile")]
    enforced = [f for f in ci_files if DOC_CI_RE.search(read(repo, f))]
    add("4.3", 4, "Enforced", bool(enforced),
        f"docs checked in {enforced[0]}" if enforced else "no CI step checks docs")
    return checks


def summarize(checks: list[Check]) -> tuple[int, int]:
    """Return (points, level). A level counts only when it and every lower level pass in full."""
    points = round(100 * sum(c.passed for c in checks) / len(checks))
    level = 0
    for lvl in sorted(LEVEL_NAMES)[1:]:
        if not all(c.passed for c in checks if c.level == lvl):
            break
        level = lvl
    return points, level


def trailer(points: int, level: int) -> str:
    return f"{points} L{level}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--repo", type=Path)
    group.add_argument("--batch", type=Path, nargs="+")
    args = parser.parse_args()

    if args.repo:
        if not args.repo.is_dir():
            parser.error(f"not a directory: {args.repo}")
        checks = score(args.repo)
        points, level = summarize(checks)
        for lvl in sorted(LEVEL_NAMES)[1:]:
            print(f"L{lvl} {LEVEL_NAMES[lvl]}")
            for c in (c for c in checks if c.level == lvl):
                print(f"  {'PASS' if c.passed else 'FAIL'}  {c.id} {c.name}: {c.detail}")
        print(f"\nSteer score: {points}/100, level L{level} {LEVEL_NAMES[level]}")
        print(f"Steer-Score: {trailer(points, level)}")
        return 0

    repos = sorted(p for p in args.batch if p.is_dir())
    counts = {lvl: 0 for lvl in LEVEL_NAMES}
    width = max((len(p.name) for p in repos), default=4)
    print(f"{'repo':<{width}}  points  level  failed checks")
    for repo in repos:
        checks = score(repo)
        points, level = summarize(checks)
        counts[level] += 1
        failed = " ".join(c.id for c in checks if not c.passed) or "-"
        print(f"{repo.name:<{width}}  {points:>6}  L{level:<4}  {failed}")
    print()
    for lvl, name in LEVEL_NAMES.items():
        print(f"L{lvl} {name:<16} {counts[lvl]}")
    at_bar = sum(n for lvl, n in counts.items() if lvl >= 3)
    print(f"L3 or above: {at_bar} of {len(repos)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
