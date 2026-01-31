# -*- coding: utf-8 -*-
"""
Fail if Python files contain hardcoded IPv4 addresses.

Mirrors the intent of the gixy pre-commit hook (SonarCloud S1313-like).
"""

import re
import sys

IP_RE = re.compile(r"(?<![\\w.])(\\d{1,3}(?:\\.\\d{1,3}){3})(?![\\w.])")


def _is_valid_ipv4(candidate):
    parts = candidate.split(".")
    if len(parts) != 4:
        return False
    try:
        nums = [int(p) for p in parts]
    except ValueError:
        return False
    return all(0 <= n <= 255 for n in nums)


def main(argv):
    paths = argv[1:]
    bad = []

    for path in paths:
        try:
            with open(path, "rb") as f:
                raw = f.read()
        except OSError:
            continue

        try:
            text = raw.decode("utf-8", errors="replace")
        except Exception:
            text = raw.decode("latin-1", errors="replace")

        for lineno, line in enumerate(text.splitlines(), 1):
            for match in IP_RE.finditer(line):
                ip = match.group(1)
                if _is_valid_ipv4(ip):
                    bad.append((path, lineno, ip, line.strip()))

    if bad:
        for path, lineno, ip, line in bad:
            sys.stderr.write("%s:%d: hardcoded IP %s: %s\n" % (path, lineno, ip, line))
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
