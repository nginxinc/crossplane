# -*- coding: utf-8 -*-
"""
Fail if files contain obvious hardcoded absolute local paths.

This is intentionally conservative and only run on code/config files via
pre-commit's `files:` filter.
"""

import io
import re
import sys


PATTERNS = [
    re.compile(r"/Users/[^\\s'\"]+"),
    re.compile(r"\\b[A-Za-z]:\\\\Users\\\\[^\\s'\"]+"),
]


def main(argv):
    paths = argv[1:]
    violations = []

    for path in paths:
        try:
            with io.open(path, "r", encoding="utf-8", errors="replace") as f:
                for lineno, line in enumerate(f, 1):
                    # Don't flag examples in comments.
                    if line.lstrip().startswith("#"):
                        continue
                    for rx in PATTERNS:
                        m = rx.search(line)
                        if m:
                            violations.append((path, lineno, m.group(0).strip()))
        except OSError:
            continue

    if violations:
        for path, lineno, match in violations:
            sys.stderr.write("%s:%d: hardcoded absolute path: %s\n" % (path, lineno, match))
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))


