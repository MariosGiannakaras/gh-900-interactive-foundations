#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "curriculum" / "official-curriculum.yml"
CATALOG = ROOT / "curriculum" / "course-catalog.json"
HASHES = ROOT / "curriculum" / "assessment-hashes.json"
SOURCE_LOCK = ROOT / "curriculum" / "microsoft-source-lock.json"


def fail(messages: list[str]) -> int:
    for message in messages:
        print(f"ERROR: {message}")
    return 1


def main() -> int:
    errors: list[str] = []
    manifest = MANIFEST.read_text(encoding="utf-8")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    hashes = json.loads(HASHES.read_text(encoding="utf-8"))
    source_lock = json.loads(SOURCE_LOCK.read_text(encoding="utf-8"))

    module_counts = {
        int(m): int(c)
        for m, c in re.findall(r"(?ms)^      - id: m(\d{2})\n.*?^        unit_count: (\d+)", manifest)
    }
    unit_ids = re.findall(r"id: m\d{2}-u\d{2}", manifest)

    if len(module_counts) != 16:
        errors.append(f"official curriculum must contain 16 modules; found {len(module_counts)}")
    if sum(module_counts.values()) != 106:
        errors.append(f"official curriculum unit_count total must be 106; found {sum(module_counts.values())}")
    if len(unit_ids) != 106:
        errors.append(f"official curriculum must enumerate 106 unit IDs; found {len(unit_ids)}")
    if set(catalog) != {f"{n:02d}" for n in range(1, 17)}:
        errors.append("course catalog must contain Modules 01-16 exactly")
    if set(source_lock.get("modules", {})) != {f"{n:02d}" for n in range(1, 17)}:
        errors.append("Microsoft source lock must contain Modules 01-16 exactly")
    if sum(int(v["units"]) for v in source_lock.get("modules", {}).values()) != 106:
        errors.append("Microsoft source lock must account for exactly 106 official units")

    for n in range(1, 17):
        key = f"{n:02d}"
        item = catalog.get(key)
        if not item:
            continue
        readme = ROOT / item["readme"]
        if not readme.exists():
            errors.append(f"Module {key} README missing: {item['readme']}")
            continue
        text = readme.read_text(encoding="utf-8")
        headings = re.findall(r"(?m)^## Unit \d+\b", text)
        expected = module_counts.get(n)
        if expected is not None and len(headings) != expected:
            errors.append(f"Module {key} must map {expected} official units; README has {len(headings)} Unit headings")
        if "Official Microsoft Learn module:" not in text:
            errors.append(f"Module {key} README lacks official-source traceability")

        if n == 1:
            required = [ROOT / "labs/module-01/assessment.md"]
        else:
            required = [ROOT / f"labs/module-{key}/submission.md"]
        for path in required:
            if not path.exists():
                errors.append(f"Module {key} interactive artifact missing: {path.relative_to(ROOT)}")

    if set(hashes) != {f"{n:02d}" for n in range(2, 17)}:
        errors.append("assessment hash map must contain Modules 02-16 exactly")
    for key, questions in hashes.items():
        if set(questions) != {f"Q{n}" for n in range(1, 7)}:
            errors.append(f"Module {key} assessment hash map must contain Q1-Q6")

    runtime = [
        ".github/workflows/00-start-course.yml",
        ".github/workflows/01-course-engine.yml",
        "scripts/course_unit_state.py",
        "scripts/validate_unit_activity.py",
        "scripts/validate_module_01.py",
        "scripts/validate_course_module.py",
        "scripts/audit_microsoft_semantic_depth.py",
        "curriculum/course-catalog.json",
        "curriculum/microsoft-source-lock.json",
    ]
    for rel in runtime:
        if not (ROOT / rel).exists():
            errors.append(f"runtime component missing: {rel}")

    if errors:
        return fail(errors)

    print("Course completeness audit passed.")
    print("Learning paths: 2")
    print("Modules: 16/16")
    print("Official units mapped: 106/106")
    print("Interactive module packages: 16/16")
    print("Pinned Microsoft source lock: present")
    print("Automatic Step 0 + unit-by-unit progression runtime: present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
