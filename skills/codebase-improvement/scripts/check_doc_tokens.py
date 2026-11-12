#!/usr/bin/env python3
"""Check per-file text/Markdown token budgets.

Exact counting requires `tiktoken` and an explicit encoding. Without it, this
script uses a conservative heuristic and labels results as estimates.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DEFAULT_EXTENSIONS = {".md", ".mdx", ".txt", ".rst", ".adoc"}


def heuristic_count(text: str) -> int:
    """Conservative approximation; not a model tokenizer."""
    # Count lexical chunks, punctuation, and whitespace-heavy/code fragments.
    chunks = re.findall(r"[A-Za-z0-9_]+|[^\w\s]|\s+", text, flags=re.UNICODE)
    estimate = 0
    for chunk in chunks:
        if chunk.isspace():
            # Whitespace rarely maps 1:1 to tokens; count line breaks lightly.
            estimate += chunk.count("\n")
        elif re.match(r"^[A-Za-z0-9_]+$", chunk):
            # Long identifiers/words often split into multiple subword tokens.
            estimate += max(1, (len(chunk) + 3) // 4)
        else:
            estimate += 1
    return estimate


def count_tokens(text: str, encoding_name: str | None) -> tuple[int, str]:
    if encoding_name:
        try:
            import tiktoken  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "An encoding was requested but tiktoken is not installed. "
                "Install it with: python -m pip install tiktoken"
            ) from exc
        try:
            encoding = tiktoken.get_encoding(encoding_name)
        except Exception as exc:
            raise RuntimeError(f"Unable to load tiktoken encoding {encoding_name!r}: {exc}") from exc
        return len(encoding.encode(text)), f"tiktoken:{encoding_name}"
    return heuristic_count(text), "heuristic-estimate"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path("."))
    parser.add_argument("--max-tokens", type=int, default=5000)
    parser.add_argument("--target-tokens", type=int, default=4200)
    parser.add_argument("--encoding", help="tiktoken encoding, e.g. cl100k_base")
    parser.add_argument("--extensions", default=",".join(sorted(DEFAULT_EXTENSIONS)))
    parser.add_argument("--include-hidden", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    if args.max_tokens <= 0 or args.target_tokens <= 0:
        parser.error("token limits must be positive")
    if args.target_tokens >= args.max_tokens:
        parser.error("--target-tokens must be less than --max-tokens")
    if not args.directory.exists() or not args.directory.is_dir():
        parser.error(f"not a directory: {args.directory}")

    extensions = {("." + item.strip().lstrip(".")).lower()
                  for item in args.extensions.split(",") if item.strip()}
    files = sorted(
        p for p in args.directory.rglob("*")
        if p.is_file()
        and p.suffix.lower() in extensions
        and (args.include_hidden or not any(part.startswith(".") for part in p.relative_to(args.directory).parts))
    )

    failures = 0
    warnings = 0
    if not files:
        if not args.quiet:
            print(f"No files found under {args.directory} for {sorted(extensions)}")
        return 0

    for path in files:
        try:
            content = path.read_text(encoding="utf-8")
            count, method = count_tokens(content, args.encoding)
        except (OSError, UnicodeError, RuntimeError) as exc:
            failures += 1
            print(f"ERROR {path}: {exc}", file=sys.stderr)
            continue

        status = "PASS"
        if count >= args.max_tokens:
            status = "FAIL"
            failures += 1
        elif count > args.target_tokens:
            status = "WARN"
            warnings += 1

        if not args.quiet:
            print(f"{status:4} {count:5} tokens [{method}] {path}")

    if not args.quiet:
        print(f"\nFiles: {len(files)} | Warnings: {warnings} | Failures: {failures}")
        if not args.encoding:
            print("NOTE: Counts are heuristic estimates, not exact model token counts.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
