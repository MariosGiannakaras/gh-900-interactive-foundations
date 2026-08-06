#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".gh900"
sys.path.insert(0, str(RUNTIME))

import course_unit_state as state  # noqa: E402


def main() -> int:
    errors: list[str] = []
    required = [
        ".gh900/course_unit_state.py",
        ".gh900/workspace.py",
        ".gh900/validate_activity.py",
        ".gh900/validate_assessment.py",
        ".gh900/validate_scenario.py",
        ".gh900/data/official-curriculum.yml",
        ".gh900/data/course-catalog.json",
        ".gh900/data/assessment-hashes.json",
        ".github/workflows/00-start-course.yml",
        ".github/workflows/01-course-engine.yml",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            errors.append(f"runtime component missing: {rel}")

    for obsolete in ("course-content", "course"):
        if (ROOT / obsolete).exists():
            errors.append(f"obsolete duplicate directory must be removed: {obsolete}/")

    try:
        units = state.load_units()
    except Exception as exc:
        errors.append(f"learner runtime cannot load: {exc}")
        units = []

    ids = [u.id for u in units]
    if len(units) != 106:
        errors.append(f"learner runtime must contain 106 states; found {len(units)}")
    if ids and (ids[0] != "m01-u01" or ids[-1] != "m16-u07"):
        errors.append("runtime boundaries must be m01-u01 through m16-u07")
    if len(ids) != len(set(ids)):
        errors.append("runtime unit IDs must be unique")

    parts = Counter(u.part for u in units)
    if parts != Counter({1: 57, 2: 49}):
        errors.append(f"runtime parts must be Part 1=57 and Part 2=49; found {dict(parts)}")
    modes = Counter(u.mode for u in units)
    expected_modes = Counter({"read": 58, "activity": 12, "scenario": 4, "assessment": 16, "summary": 16})
    if modes != expected_modes:
        errors.append(f"unexpected runtime mode counts: {dict(modes)}")
    if set(u.module for u in units) != set(range(1, 17)):
        errors.append("runtime must contain Modules 1-16 exactly")

    for unit in units:
        try:
            rendered = state.render(unit)
        except Exception as exc:
            errors.append(f"{unit.id} cannot render: {exc}")
            continue
        if f"Part **{unit.part} / 2**" not in rendered or f"**{unit.ordinal} / 106**" not in rendered:
            errors.append(f"{unit.id} does not expose Part + 106-unit progress")
        if unit.mode in {"read", "summary"} and "/next" not in rendered:
            errors.append(f"{unit.id} missing /next")
        if unit.mode == "assessment" and "/answer" not in rendered:
            errors.append(f"{unit.id} assessment is not Issue-native")
        if unit.mode == "scenario" and "/scenario" not in rendered:
            errors.append(f"{unit.id} scenario is not Issue-native")
        if unit.mode == "activity":
            if unit.branch != f"lab/{unit.id}" or unit.sandbox != f"sandbox/{unit.id}":
                errors.append(f"{unit.id} does not use isolated unit branches")
            if "prepared only what this unit needs" not in rendered:
                errors.append(f"{unit.id} missing on-demand workspace instruction")

    for module in range(1, 17):
        try:
            questions, count = state.assessment_questions(module)
        except Exception as exc:
            errors.append(f"Module {module} assessment cannot render: {exc}")
            continue
        expected = 12 if module == 1 else 6
        if count != expected:
            errors.append(f"Module {module} assessment expected {expected} questions; found {count}")
        if "[ ]" in questions or "[x]" in questions.lower():
            errors.append(f"Module {module} still exposes checkbox-file assessment UI")

    workspace = (RUNTIME / "workspace.py").read_text(encoding="utf-8")
    for rel in ["docs", "modules", "unit-details", "curriculum", "labs", "scripts", "course-content"]:
        if f'"{rel}"' not in workspace:
            errors.append(f"learner bootstrap does not remove source-only {rel}/")
    for rel in ["exercise", ".devcontainer", "SECURITY.md", ".github/CODEOWNERS"]:
        if rel not in workspace:
            errors.append(f"workspace cleanup contract missing: {rel}")

    engine = (ROOT / ".github/workflows/01-course-engine.yml").read_text(encoding="utf-8")
    for token in [
        ".gh900/course_unit_state.py",
        ".gh900/workspace.py",
        ".gh900/validate_activity.py",
        ".gh900/validate_assessment.py",
        ".gh900/validate_scenario.py",
        "git push origin --delete",
        "/answer",
        "/scenario",
    ]:
        if token not in engine:
            errors.append(f"course engine v2 contract missing: {token}")
    if "labs/module-" in engine or "scripts/course_unit_state.py" in engine:
        errors.append("learner engine still depends on old learner-facing paths")

    start = (ROOT / ".github/workflows/00-start-course.yml").read_text(encoding="utf-8")
    if ".gh900/workspace.py bootstrap" not in start or "contents: write" not in start:
        errors.append("Step 0 does not bootstrap the clean learner workspace")

    if units:
        visited: list[str] = []
        current = units[0]
        while current is not None:
            if current.id in visited:
                errors.append(f"runtime cycle detected at {current.id}")
                break
            visited.append(current.id)
            current = state.next_unit(current.id)
        if visited != ids:
            errors.append("next_unit chain does not reproduce all 106 units exactly")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Learner runtime v2 audit passed.")
    print("Parts: 2/2 (57 + 49 units)")
    print("Modules: 16/16")
    print("Units: 106/106")
    print("Issue-native lessons/assessments + isolated per-unit workspaces: present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
