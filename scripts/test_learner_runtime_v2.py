#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".gh900"


def load_state_module():
    path = RUNTIME / "course_unit_state.py"
    spec = importlib.util.spec_from_file_location("gh900_runtime_state", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load .gh900/course_unit_state.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    errors: list[str] = []

    required_runtime = [
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
    for rel in required_runtime:
        if not (ROOT / rel).exists():
            errors.append(f"runtime component missing: {rel}")

    if (ROOT / "course-content").exists():
        errors.append("obsolete learner-facing course-content/ directory must be removed")
    if (ROOT / "course").exists():
        errors.append("obsolete duplicate course/ directory must be removed")

    try:
        state = load_state_module()
        units = state.load_units()
    except Exception as exc:
        errors.append(f"new learner runtime cannot load: {exc}")
        units = []
        state = None

    if len(units) != 106:
        errors.append(f"new learner runtime must contain 106 states; found {len(units)}")

    ids = [u.id for u in units]
    if ids and (ids[0] != "m01-u01" or ids[-1] != "m16-u07"):
        errors.append("new runtime boundaries must be m01-u01 through m16-u07")
    if len(ids) != len(set(ids)):
        errors.append("new runtime unit IDs must be unique")

    part_counts = Counter(u.part for u in units)
    if part_counts != Counter({1: 57, 2: 49}):
        errors.append(f"runtime parts must be Part 1=57 and Part 2=49; found {dict(part_counts)}")

    mode_counts = Counter(u.mode for u in units)
    expected_modes = Counter({"read": 58, "activity": 12, "scenario": 4, "assessment": 16, "summary": 16})
    if mode_counts != expected_modes:
        errors.append(f"unexpected runtime mode counts: {dict(mode_counts)}")

    if set(u.module for u in units) != set(range(1, 17)):
        errors.append("runtime must contain Modules 1-16 exactly")

    if state is not None:
        for unit in units:
            try:
                rendered = state.render(unit)
            except Exception as exc:
                errors.append(f"{unit.id} cannot render in Issue format: {exc}")
                continue

            if f"Part **{unit.part} / 2**" not in rendered:
                errors.append(f"{unit.id} does not show Part 1/2 progress")
            if f"**{unit.ordinal} / 106**" not in rendered:
                errors.append(f"{unit.id} does not show 106-unit progress")
            if unit.mode in {"read", "summary"} and "/next" not in rendered:
                errors.append(f"{unit.id} missing /next Issue command")
            if unit.mode == "assessment" and "/answer" not in rendered:
                errors.append(f"{unit.id} assessment is not Issue-native")
            if unit.mode == "scenario" and "/scenario" not in rendered:
                errors.append(f"{unit.id} scenario is not Issue-native")
            if unit.mode == "activity":
                if unit.branch != f"lab/{unit.id}" or unit.sandbox != f"sandbox/{unit.id}":
                    errors.append(f"{unit.id} must use isolated per-unit lab/sandbox branches")
                if "The course engine has prepared only what this unit needs" not in rendered:
                    errors.append(f"{unit.id} does not describe on-demand workspace behavior")

        for module in range(1, 17):
            assessment = next((u for u in units if u.module == module and u.mode == "assessment"), None)
            if assessment is None:
                errors.append(f"Module {module} has no assessment")
                continue
            try:
                questions, count = state.assessment_questions(module)
            except Exception as exc:
                errors.append(f"Module {module} assessment cannot render: {exc}")
                continue
            expected = 12 if module == 1 else 6
            if count != expected:
                errors.append(f"Module {module} assessment should render {expected} questions; found {count}")
            if "[ ]" in questions or "[x]" in questions.lower():
                errors.append(f"Module {module} still exposes file-checkbox assessment UI")

    workspace = (RUNTIME / "workspace.py").read_text(encoding="utf-8") if (RUNTIME / "workspace.py").exists() else ""
    for source_only in ["docs", "modules", "unit-details", "curriculum", "labs", "scripts", "course-content"]:
        if f'"{source_only}"' not in workspace:
            errors.append(f"learner bootstrap does not remove source-only {source_only}/ content")
    for temporary in ["exercise", ".devcontainer", "SECURITY.md", ".github/CODEOWNERS"]:
        if temporary not in workspace:
            errors.append(f"workspace cleanup contract missing temporary artifact: {temporary}")

    engine = (ROOT / ".github/workflows/01-course-engine.yml").read_text(encoding="utf-8")
    for required in [
        ".gh900/course_unit_state.py",
        ".gh900/workspace.py",
        ".gh900/validate_activity.py",
        ".gh900/validate_assessment.py",
        ".gh900/validate_scenario.py",
        "git push origin --delete",
        "/answer",
        "/scenario",
    ]:
        if required not in engine:
            errors.append(f"course engine v2 contract missing: {required}")
    if "labs/module-" in engine or "scripts/course_unit_state.py" in engine:
        errors.append("learner engine must not depend on old learner-facing lab/source paths")

    start = (ROOT / ".github/workflows/00-start-course.yml").read_text(encoding="utf-8")
    if ".gh900/workspace.py bootstrap" not in start:
        errors.append("Step 0 must clean a template copy into the learner workspace")
    if "contents: write" not in start:
        errors.append("Step 0 needs contents: write to commit learner bootstrap cleanup")

    if units:
        visited: list[str] = []
        current = units[0]
        while current is not None:
            if current.id in visited:
                errors.append(f"new runtime cycle detected at {current.id}")
                break
            visited.append(current.id)
            current = state.next_unit(current.id)
        if visited != ids:
            errors.append("new runtime next_unit chain does not match all 106 canonical units")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Learner runtime v2 audit passed.")
    print("Parts: 2/2 (57 + 49 units)")
    print("Modules: 16/16")
    print("Units: 106/106")
    print("Learner UX: Issue-native lessons/assessments + per-unit temporary workspaces")
    print("Cleanup: temporary exercise state removed after validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
