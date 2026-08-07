#!/usr/bin/env python3
"""Verify curated concept coverage in the actual learner-visible Issue rendering."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GH900 = ROOT / ".gh900"
sys.path.insert(0, str(GH900))

import course_unit_state as state  # noqa: E402

MANIFEST = GH900 / "data" / "concept-coverage.json"


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    mapping = data.get("units", {})
    units = state.load_units()
    expected = {u.id for u in units}
    actual = set(mapping)
    errors: list[str] = []

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append("Units missing concept contracts: " + ", ".join(missing))
    if extra:
        errors.append("Unknown units in concept contracts: " + ", ".join(extra))

    passed = 0
    for unit in units:
        groups = mapping.get(unit.id)
        if not isinstance(groups, list) or not groups:
            continue
        rendered = state.render(unit).lower()
        failed_groups: list[list[str]] = []
        for group in groups:
            if not isinstance(group, list) or not group or not all(isinstance(term, str) and term for term in group):
                errors.append(f"{unit.id}: invalid concept group {group!r}")
                continue
            if not any(term.lower() in rendered for term in group):
                failed_groups.append(group)
        if failed_groups:
            for group in failed_groups:
                errors.append(f"{unit.id}: learner rendering is missing concept group: {' | '.join(group)}")
        else:
            passed += 1

    print(f"Concept coverage contracts present: {len(actual)}/106")
    print(f"Units passing required concept groups: {passed}/106")
    if errors:
        print("Concept coverage failures:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Concept-level Microsoft Learn coverage passed: 106/106 units.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
