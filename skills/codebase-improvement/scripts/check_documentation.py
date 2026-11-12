#!/usr/bin/env python3
"""Perform lightweight structural checks on Markdown documentation."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DEFAULT_IGNORES = {".git", ".venv", "node_modules", "__pycache__", "dist", "build"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path("docs"))
    parser.add_argument("--max-tokens", type=int, default=5000)
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args()

    if not args.directory.exists() or not args.directory.is_dir():
        parser.error(f"not a directory: {args.directory}")

    markdown_files = sorted(
        p for p in args.directory.rglob("*.md")
        # Relative parts: an ancestor named "build" must not hide the whole repo.
        # Hidden dirs (.claude/, .agents/) hold installed skills, not the repo's docs.
        if not any(part in DEFAULT_IGNORES or part.startswith(".")
                   for part in p.relative_to(args.directory).parts)
    )
    errors: list[str] = []
    warnings: list[str] = []

    if not markdown_files:
        warnings.append(f"No Markdown files found under {args.directory}")

    for path in markdown_files:
        rel = path.relative_to(args.directory)
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{rel}: cannot read UTF-8 content: {exc}")
            continue

        if not content.strip():
            errors.append(f"{rel}: empty Markdown file")
            continue

        if not re.search(r"(?m)^#\s+\S", content):
            warnings.append(f"{rel}: missing a top-level '# ' heading")

        if len(content) > 100_000:
            warnings.append(f"{rel}: unusually large source file; check token budget")

        if re.search(r"(?i)\b(TODO|TBD|FIXME)\b", content):
            warnings.append(f"{rel}: contains TODO/TBD/FIXME markers")

        if re.search(r"(?i)(api[_-]?key|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}", content):
            errors.append(f"{rel}: possible credential-like value; inspect and remove secrets")

        # Catch common placeholders in documents that otherwise look complete.
        if re.search(r"\b(path/to/|YOUR-ORG|example\.com/replace)\b", content):
            warnings.append(f"{rel}: contains template placeholder(s)")

    for item in warnings:
        print(f"WARN: {item}")
    for item in errors:
        print(f"ERROR: {item}", file=sys.stderr)

    print(f"Checked {len(markdown_files)} Markdown file(s): "
          f"{len(warnings)} warning(s), {len(errors)} error(s).")

    return 1 if errors or (args.fail_on_warning and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
