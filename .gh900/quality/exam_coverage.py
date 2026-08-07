#!/usr/bin/env python3
"""Verify every January-2026 GH-900 objective maps to real learner-visible units."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GH900 = ROOT / ".gh900"
sys.path.insert(0, str(GH900))

import course_unit_state as state  # noqa: E402

MANIFEST = GH900 / "data" / "gh900-objectives.json"


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    units = {u.id: u for u in state.load_units()}
    errors: list[str] = []
    objective_count = 0
    domain_count = 0

    domains = data.get("domains", [])
    if len(domains) != 7:
        errors.append(f"Expected 7 GH-900 domains, found {len(domains)}")

    seen_ids: set[str] = set()
    for domain in domains:
        domain_count += 1
        objectives = domain.get("objectives", [])
        if not objectives:
            errors.append(f"Domain {domain.get('id')} has no objectives")
        for objective in objectives:
            objective_count += 1
            oid = objective.get("id")
            if not isinstance(oid, str) or not oid:
                errors.append(f"Domain {domain.get('id')} has an objective without id")
                continue
            if oid in seen_ids:
                errors.append(f"Duplicate exam objective id: {oid}")
            seen_ids.add(oid)
            mapped = objective.get("units", [])
            terms = objective.get("terms", [])
            if not mapped:
                errors.append(f"{oid}: no mapped course units")
                continue
            unknown = [uid for uid in mapped if uid not in units]
            if unknown:
                errors.append(f"{oid}: unknown mapped units: {', '.join(unknown)}")
                continue
            if not terms:
                errors.append(f"{oid}: no required learner-visible terms")
                continue
            rendered = "\n".join(state.render(units[uid]).lower() for uid in mapped)
            missing = [term for term in terms if str(term).lower() not in rendered]
            if missing:
                errors.append(f"{oid}: mapped units are missing required concepts: {', '.join(missing)}")

    print(f"GH-900 domains mapped: {domain_count}/7")
    print(f"GH-900 objectives mapped and checked: {objective_count}")
    if errors:
        print("GH-900 objective coverage failures:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("GH-900 January-2026 exam-objective coverage passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
