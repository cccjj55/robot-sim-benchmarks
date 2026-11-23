#!/usr/bin/env python3
"""Validate data/claims.yaml before anything lands in README.md.

The rules are the ones in docs/evidence-rules.md, made executable:
  - every claim has id, engine, task, claim, hardware, source.url, label
  - label is one of UPSTREAM / 3P / MEASURED
  - MEASURED rows must also name an artifact
Rows that fail are printed and the process exits 1.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("need pyyaml: pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)

REQUIRED = ("id", "engine", "task", "claim", "hardware", "source", "label")
LABELS = {"UPSTREAM", "3P", "MEASURED"}


def check(path: Path = Path("data/claims.yaml")) -> int:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    claims = data.get("claims") or []
    if not claims:
        print("no claims found", file=sys.stderr)
        return 1

    problems: list[str] = []
    seen: set[str] = set()

    for i, c in enumerate(claims):
        where = c.get("id", f"claims[{i}]")
        for key in REQUIRED:
            if not c.get(key):
                problems.append(f"{where}: missing {key}")
        if c.get("label") not in LABELS:
            problems.append(f"{where}: label {c.get('label')!r} not in {sorted(LABELS)}")
        url = (c.get("source") or {}).get("url", "")
        if url and not url.startswith("http"):
            problems.append(f"{where}: source.url is not a link ({url!r})")
        if c.get("label") == "MEASURED" and not c.get("artifact"):
            problems.append(f"{where}: MEASURED rows must name an artifact")
        if c.get("id") in seen:
            problems.append(f"{where}: duplicate id")
        seen.add(c.get("id"))

    counts: dict[str, int] = {}
    for c in claims:
        counts[c.get("label", "?")] = counts.get(c.get("label", "?"), 0) + 1

    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1

    print(f"ok: {len(claims)} claims · " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
