#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

MANIFEST = Path("curriculum/official-curriculum.yml")
EXPECTED_MODULES = 16
EXPECTED_UNITS = 106


def main() -> int:
    text = MANIFEST.read_text(encoding="utf-8")

    modules = re.findall(r"^\s+- id: (m\d{2})\s*$", text, flags=re.MULTILINE)
    units = re.findall(r"\{ id: (m\d{2}-u\d{2}),", text)
    declared_unit_counts = [
        int(value)
        for value in re.findall(r"^\s+unit_count:\s*(\d+)\s*$", text, flags=re.MULTILINE)
    ]

    errors: list[str] = []

    if len(modules) != EXPECTED_MODULES:
        errors.append(f"expected {EXPECTED_MODULES} modules, found {len(modules)}")
    if len(set(modules)) != len(modules):
        errors.append("duplicate module IDs found")

    if len(units) != EXPECTED_UNITS:
        errors.append(f"expected {EXPECTED_UNITS} units, found {len(units)}")
    if len(set(units)) != len(units):
        errors.append("duplicate unit IDs found")

    if len(declared_unit_counts) != EXPECTED_MODULES:
        errors.append(
            f"expected {EXPECTED_MODULES} module unit_count declarations, "
            f"found {len(declared_unit_counts)}"
        )
    elif sum(declared_unit_counts) != EXPECTED_UNITS:
        errors.append(
            f"declared unit_count total is {sum(declared_unit_counts)}, "
            f"expected {EXPECTED_UNITS}"
        )

    if "modules: 16" not in text or "units: 106" not in text:
        errors.append("coverage_target must explicitly remain 16 modules / 106 units")

    if errors:
        print("Curriculum manifest validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Curriculum manifest validated: {len(modules)} modules / "
        f"{len(units)} units."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
