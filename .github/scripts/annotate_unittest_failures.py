"""Emit GitHub Actions error annotations from unittest -v output."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "test-results.txt")
    if not path.is_file():
        print(f"::error::Missing test results file: {path}")
        return 1

    lines = path.read_text(errors="replace").splitlines()
    i = 0
    found = False
    while i < len(lines):
        line = lines[i]
        if line.startswith("FAIL:") or line.startswith("ERROR:"):
            found = True
            block = [line]
            i += 1
            while i < len(lines) and not (
                lines[i].startswith("FAIL:")
                or lines[i].startswith("ERROR:")
                or lines[i].startswith("====")
                or lines[i].startswith("FAILED (")
                or lines[i] == "OK"
            ):
                block.append(lines[i])
                i += 1
                if len(block) > 50:
                    break
            message = " | ".join(part.strip() for part in block if part.strip())[:650]
            print(f"::error title=Backend unit test::{message}")
            continue
        i += 1

    if not found:
        tail = " | ".join(lines[-20:])[:650]
        print(f"::error title=Backend unit test::unittest failed; tail: {tail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
