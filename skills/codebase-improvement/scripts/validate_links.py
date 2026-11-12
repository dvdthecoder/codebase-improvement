#!/usr/bin/env python3
"""Validate relative Markdown links and image references."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK_RE = re.compile(r"!?\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+['\"][^'\"]*['\"])?\)")
REF_RE = re.compile(r"(?m)^\s*\[[^\]]+\]:\s*(\S+)")


def strip_anchor_and_query(target: str) -> str:
    parsed = urlsplit(target)
    return unquote(parsed.path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path("."))
    parser.add_argument("--extensions", default=".md,.mdx")
    parser.add_argument("--include-hidden", action="store_true")
    args = parser.parse_args()

    root = args.directory.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    extensions = {x.strip().lower() for x in args.extensions.split(",") if x.strip()}
    files = sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in extensions
        and (args.include_hidden or not any(part.startswith(".") for part in p.relative_to(root).parts))
        and not any(part in {".git", "node_modules", ".venv"} for part in p.relative_to(root).parts)
    )

    errors: list[str] = []
    checked = 0

    for source in files:
        try:
            text = source.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{source}: cannot read: {exc}")
            continue

        targets = [m.group(1) or m.group(2) for m in LINK_RE.finditer(text)]
        targets += [m.group(1) for m in REF_RE.finditer(text)]

        for target in targets:
            checked += 1
            target = target.strip()
            if not target or target.startswith("#"):
                continue
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            path_part = strip_anchor_and_query(target)
            if not path_part:
                continue
            candidate = (source.parent / path_part).resolve()
            # A relative link must remain inside the checked repository.
            try:
                candidate.relative_to(root)
            except ValueError:
                errors.append(f"{source.relative_to(root)}: link escapes repository: {target}")
                continue
            if not candidate.exists():
                errors.append(f"{source.relative_to(root)}: broken link: {target}")

    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"Checked {checked} local link(s) across {len(files)} file(s); "
          f"{len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
