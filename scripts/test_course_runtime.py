#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import course_unit_state as state  # noqa: E402


def main() -> int:
    errors: list[str] = []
    units = state.load_units()

    if len(units) != 106:
        errors.append(f"Expected 106 runtime units, got {len(units)}")
    ids = [u.id for u in units]
    if len(set(ids)) != len(ids):
        errors.append("Runtime unit IDs are not unique.")
    if ids and ids[0] != "m01-u01":
        errors.append(f"First state must be m01-u01, got {ids[0]}")
    if ids and ids[-1] != "m16-u07":
        errors.append(f"Last state must be m16-u07, got {ids[-1]}")

    per_module: dict[int, Counter[str]] = defaultdict(Counter)
    for unit in units:
        per_module[unit.module][unit.mode] += 1
        try:
            rendered = state.render(unit)
        except Exception as exc:
            errors.append(f"{unit.id} cannot render: {exc}")
            continue
        if unit.id.upper() not in rendered:
            errors.append(f"{unit.id} rendered step does not identify itself.")
        if unit.mode in {"read", "summary"} and "/next" not in rendered:
            errors.append(f"{unit.id} reading step has no /next instruction.")
        if unit.mode == "activity":
            expected = ROOT / f"labs/module-{unit.module:02d}/submission.md"
            if not expected.exists():
                errors.append(f"{unit.id} activity has no {expected.relative_to(ROOT)}")
        if unit.mode == "assessment":
            assessment = ROOT / ("labs/module-01/assessment.md" if unit.module == 1 else f"labs/module-{unit.module:02d}/submission.md")
            if not assessment.exists():
                errors.append(f"{unit.id} assessment artifact missing: {assessment.relative_to(ROOT)}")

    if set(per_module) != set(range(1, 17)):
        errors.append(f"Runtime modules must be exactly 1-16; got {sorted(per_module)}")
    for module in range(1, 17):
        modes = per_module[module]
        if modes["assessment"] != 1:
            errors.append(f"Module {module} must have exactly one assessment checkpoint; got {modes['assessment']}")
        if modes["activity"] < 1:
            errors.append(f"Module {module} must have at least one hands-on/simulation activity checkpoint.")

    # Walk only through next_unit to detect skipped states or cycles independently of list indexing.
    visited: list[str] = []
    current = units[0] if units else None
    while current is not None:
        if current.id in visited:
            errors.append(f"Cycle detected at {current.id}")
            break
        visited.append(current.id)
        current = state.next_unit(current.id)
    if visited != ids:
        errors.append("next_unit chain does not reproduce the canonical 106-unit order exactly.")

    mode_counts = Counter(u.mode for u in units)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Course runtime consistency passed.")
    print(f"States: {len(units)}")
    print("Modes: " + ", ".join(f"{name}={count}" for name, count in sorted(mode_counts.items())))
    print("Modules: 16/16 with >=1 activity and exactly 1 assessment each")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
