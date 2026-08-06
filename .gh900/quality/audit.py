#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GH900 = ROOT / ".gh900"
DATA = GH900 / "data"
sys.path.insert(0, str(GH900))

import course_unit_state as state  # noqa: E402

EXPECTED_MODULE_UNITS = {
    1: 6, 2: 8, 3: 9, 4: 7, 5: 7, 6: 7, 7: 8, 8: 5,
    9: 7, 10: 5, 11: 6, 12: 7, 13: 7, 14: 5, 15: 5, 16: 7,
}
ALLOWED_TOP_LEVEL = {".gh900", ".github", "LICENSE", "README.md"}
SOURCE_ONLY_FORBIDDEN = {
    "modules", "unit-details", "labs", "curriculum", "scripts", "docs",
    "course", "course-content", ".devcontainer",
}


def error(errors: list[str], message: str) -> None:
    errors.append(message)


def check_workflows(errors: list[str]) -> None:
    workflows = ROOT / ".github" / "workflows"
    for path in sorted(workflows.glob("*.y*ml")):
        text = path.read_text(encoding="utf-8")
        if "pull_request_target:" in text:
            error(errors, f"{path.relative_to(ROOT)} must not use pull_request_target")
        for match in re.finditer(r"(?m)^\s*uses:\s*([^\s#]+)", text):
            ref = match.group(1)
            if ref.startswith("./"):
                continue
            if "@" not in ref:
                error(errors, f"{path.relative_to(ROOT)} has malformed action reference: {ref}")
                continue
            _, version = ref.rsplit("@", 1)
            if not re.fullmatch(r"[0-9a-f]{40}", version):
                error(errors, f"{path.relative_to(ROOT)} must pin external Actions to a full commit SHA: {ref}")

    start = (workflows / "00-start-course.yml").read_text(encoding="utf-8")
    engine = (workflows / "01-course-engine.yml").read_text(encoding="utf-8")
    quality = (workflows / "quality.yml").read_text(encoding="utf-8")
    if "!github.event.repository.is_template" not in start:
        error(errors, "Step 0 must run only in non-template learner copies")
    if "!github.event.repository.is_template" not in engine:
        error(errors, "Course engine must run only in non-template learner copies")
    if "github.event.repository.is_template" not in quality:
        error(errors, "Course Quality must be source-template-only")
    if 'branches:\n      - "lab/**"' not in engine:
        error(errors, "Course engine must limit push progression to temporary lab branches")


def check_public_surface(errors: list[str]) -> None:
    top = {p.name for p in ROOT.iterdir() if p.name not in {".git", "_microsoft_learn"}}
    unexpected = sorted(top - ALLOWED_TOP_LEVEL)
    missing = sorted(ALLOWED_TOP_LEVEL - top)
    if unexpected:
        error(errors, "Unexpected top-level learner/source clutter: " + ", ".join(unexpected))
    if missing:
        error(errors, "Required top-level paths missing: " + ", ".join(missing))
    for rel in SOURCE_ONLY_FORBIDDEN:
        if (ROOT / rel).exists():
            error(errors, f"Legacy duplicate source path must be removed: {rel}")

    required = [
        "README.md", "LICENSE",
        ".github/CONTRIBUTING.md", ".github/CODE_OF_CONDUCT.md", ".github/SECURITY.md",
        ".github/ARCHITECTURE.md", ".github/MAINTAINING.md",
        ".gh900/course_unit_state.py", ".gh900/workspace.py",
        ".gh900/validate_activity.py", ".gh900/validate_assessment.py", ".gh900/validate_scenario.py",
        ".gh900/data/official-curriculum.yml", ".gh900/data/course-catalog.json",
        ".gh900/data/microsoft-source-lock.json", ".gh900/data/assessment-hashes.json",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            error(errors, f"Required repository file missing: {rel}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in ("Copy Exercise", "16 / 16", "106 / 106", "Issue-first", "Part 1", "Part 2"):
        if phrase not in readme:
            error(errors, f"README must communicate: {phrase}")


def check_curriculum(errors: list[str]) -> None:
    manifest = (DATA / "official-curriculum.yml").read_text(encoding="utf-8")
    rows = re.findall(
        r"\{\s*id:\s*(m\d{2}-u\d{2}),\s*title:\s*(.*?),\s*implementation:\s*[^}]+\}",
        manifest,
    )
    if len(rows) != 106:
        error(errors, f"Official curriculum must contain 106 units, found {len(rows)}")

    ids = [row[0] for row in rows]
    if len(set(ids)) != len(ids):
        error(errors, "Official curriculum unit IDs are not unique")
    if ids and (ids[0] != "m01-u01" or ids[-1] != "m16-u07"):
        error(errors, "Official curriculum endpoints must be m01-u01 through m16-u07")

    units = state.load_units()
    runtime_ids = [u.id for u in units]
    if runtime_ids != ids:
        error(errors, "Runtime state order must match the canonical 106-unit manifest exactly")

    per_module = Counter(u.module for u in units)
    for module, expected in EXPECTED_MODULE_UNITS.items():
        if per_module[module] != expected:
            error(errors, f"Module {module} expected {expected} units, got {per_module[module]}")

    part_counts = Counter(u.part for u in units)
    if part_counts != Counter({1: 57, 2: 49}):
        error(errors, f"Expected Part 1=57 and Part 2=49 units, got {dict(part_counts)}")

    modes = Counter(u.mode for u in units)
    if modes["assessment"] != 16:
        error(errors, f"Expected 16 assessment units, got {modes['assessment']}")
    for module in range(1, 17):
        module_modes = {u.mode for u in units if u.module == module}
        if not ({"activity", "scenario"} & module_modes):
            error(errors, f"Module {module} needs at least one practical activity or explicit scenario")

    catalog = json.loads((DATA / "course-catalog.json").read_text(encoding="utf-8"))
    if set(catalog) != {f"{n:02d}" for n in range(1, 17)}:
        error(errors, "Course catalog must contain exactly Modules 01-16")
    for key, item in catalog.items():
        path = ROOT / str(item["readme"])
        if not path.exists():
            error(errors, f"Catalog content path missing for Module {key}: {item['readme']}")
        detail = item.get("detail")
        if detail and not (ROOT / str(detail)).exists():
            error(errors, f"Catalog detail path missing for Module {key}: {detail}")


def check_rendering(errors: list[str]) -> None:
    units = state.load_units()
    for unit in units:
        try:
            rendered = state.render(unit)
        except Exception as exc:
            error(errors, f"{unit.id} failed to render: {exc}")
            continue
        if unit.title not in rendered:
            error(errors, f"{unit.id} render must show the unit title")
        if f"{unit.ordinal} / 106" not in rendered:
            error(errors, f"{unit.id} render must show total-course progress")
        if f"Part **{unit.part} / 2**" not in rendered:
            error(errors, f"{unit.id} render must show Part {unit.part}")
        if unit.mode in {"read", "summary"} and "/next" not in rendered:
            error(errors, f"{unit.id} must expose /next in the Issue")
        if unit.mode == "assessment":
            if "/answer" not in rendered or "Question 1" not in rendered:
                error(errors, f"{unit.id} assessment must be fully Issue-native")
        if unit.mode == "scenario" and "/scenario" not in rendered:
            error(errors, f"{unit.id} scenario must be Issue-native")
        if unit.mode == "activity":
            if "exercise" not in rendered.lower():
                error(errors, f"{unit.id} hands-on unit must present its exercise in the Issue")
            if not unit.branch or not unit.sandbox:
                error(errors, f"{unit.id} activity must have isolated lab/sandbox branches")

    for module in range(1, 17):
        questions, count = state.assessment_questions(module)
        expected = 12 if module == 1 else 6
        if count != expected:
            error(errors, f"Module {module} expected {expected} original assessment questions, got {count}")
        if "Question 1" not in questions:
            error(errors, f"Module {module} assessment questions could not be rendered")


def main() -> int:
    errors: list[str] = []
    check_public_surface(errors)
    check_workflows(errors)
    check_curriculum(errors)
    check_rendering(errors)

    if errors:
        print("Repository/course audit failures:")
        for item in errors:
            print(f"- {item}")
        return 1

    units = state.load_units()
    modes = Counter(u.mode for u in units)
    print("Public/source repository audit passed.")
    print("Top level: README.md, LICENSE, .github/, .gh900/")
    print("Curriculum: 2/2 parts, 16/16 modules, 106/106 units")
    print("Part split: 57 + 49")
    print("Modes: " + ", ".join(f"{k}={v}" for k, v in sorted(modes.items())))
    print("All learner units render directly into the course Issue.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
