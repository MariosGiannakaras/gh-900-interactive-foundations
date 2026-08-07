#!/usr/bin/env python3
"""Verify on-demand workspace, assessment, and runtime resilience contracts."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GH900 = ROOT / ".gh900"
TEMPLATES = GH900 / "templates"
sys.path.insert(0, str(GH900))

import course_unit_state as state  # noqa: E402
import validate_assessment as assessment_validator  # noqa: E402

EXPECTED_ACTIVITY_MODULES = {1, 2, 4, 5, 6, 8, 9, 10, 11, 14, 15, 16}
LEGACY_ASSESSMENT_MARKERS = (
    "ACTIVITY_STATUS",
    "REPLACE_ME",
    "EVIDENCE_",
    "Read `modules/",
    "Work on branch `lab/module-",
)


def main() -> int:
    errors: list[str] = []
    workspace = (GH900 / "workspace.py").read_text(encoding="utf-8")

    # Keep copy_template() calls and actual exercise fixtures in lock-step.
    calls = re.findall(r'copy_template\((\d+),\s*"([^"]+)",\s*"([^"]+)"\)', workspace)
    if not calls:
        errors.append("workspace.py contains no parseable copy_template contracts")
    for module_text, source_name, destination in calls:
        module = int(module_text)
        source = TEMPLATES / "labs" / f"module-{module:02d}" / source_name
        if not source.exists():
            errors.append(
                f"Module {module} workspace requests missing fixture {source.relative_to(ROOT)} -> {destination}"
            )

    devcontainer = TEMPLATES / "devcontainer" / "devcontainer.json"
    if not devcontainer.exists():
        errors.append("Codespaces workspace template is missing .gh900/templates/devcontainer/devcontainer.json")

    activity_modules = {u.module for u in state.load_units() if u.mode == "activity"}
    if activity_modules != EXPECTED_ACTIVITY_MODULES:
        errors.append(
            "Activity-module contract changed unexpectedly: "
            f"expected {sorted(EXPECTED_ACTIVITY_MODULES)}, got {sorted(activity_modules)}"
        )

    # Every practical module must have a provisioning branch in workspace.py.
    for module in sorted(EXPECTED_ACTIVITY_MODULES):
        marker = "if module == 1:" if module == 1 else f"elif module == {module}:"
        if marker not in workspace:
            errors.append(f"workspace.py has no provisioning branch for activity Module {module}")

    # Assessments are Issue-native. Hidden Markdown files are question sources only;
    # old evidence/submission worksheet instructions must never return.
    assessment_hashes = json.loads((GH900 / "data" / "assessment-hashes.json").read_text(encoding="utf-8"))
    expected_modules = {f"{module:02d}" for module in range(1, 17)}
    if set(assessment_hashes) != expected_modules:
        errors.append(
            "Assessment hash store must contain exactly Modules 01-16: "
            f"got {sorted(assessment_hashes)}"
        )

    for module in range(1, 17):
        source = TEMPLATES / "labs" / f"module-{module:02d}" / ("assessment.md" if module == 1 else "submission.md")
        if not source.exists():
            errors.append(f"Module {module} assessment source is missing: {source.relative_to(ROOT)}")
            continue
        source_text = source.read_text(encoding="utf-8")
        for marker in LEGACY_ASSESSMENT_MARKERS:
            if marker in source_text:
                errors.append(f"Module {module} assessment source still contains legacy worksheet marker: {marker}")
        try:
            _, count = state.assessment_questions(module)
        except Exception as exc:
            errors.append(f"Module {module} assessment source cannot render: {exc}")
            continue
        expected = 12 if module == 1 else 6
        if count != expected:
            errors.append(f"Module {module} expected {expected} assessment questions, got {count}")

        module_hashes = assessment_hashes.get(f"{module:02d}", {})
        expected_questions = {f"Q{i}" for i in range(1, expected + 1)}
        if set(module_hashes) != expected_questions:
            errors.append(
                f"Module {module} assessment hashes do not match its {expected} question IDs"
            )
        for question, value in module_hashes.items():
            if not re.fullmatch(r"[0-9a-f]{64}", str(value)):
                errors.append(f"Module {module} {question} has an invalid SHA-256 answer hash")
                continue
            matches = [
                answer
                for answer in "ABC"
                if assessment_validator.digest(module, question, answer) == value
            ]
            if len(matches) != 1:
                errors.append(
                    f"Module {module} {question} hash must resolve to exactly one valid A/B/C answer; got {matches}"
                )

    # Critical final-module fixture alignment: these files are generated together.
    for name in ("app.py", "test_app.py", "requirements.txt"):
        path = TEMPLATES / "labs" / "module-16" / name
        if not path.exists():
            errors.append(f"Module 16 FastAPI fixture is missing {path.relative_to(ROOT)}")

    # Runtime anti-stall/idempotency contracts. These are deliberately text-level so
    # a future refactor cannot silently remove the safeguards without replacing them.
    start = (ROOT / ".github" / "workflows" / "00-start-course.yml").read_text(encoding="utf-8")
    engine = (ROOT / ".github" / "workflows" / "01-course-engine.yml").read_text(encoding="utf-8")
    for marker in (
        "concurrency:",
        "gh900-start-${{ github.repository }}",
        "cancel-in-progress: false",
    ):
        if marker not in start:
            errors.append(f"Step 0 startup serialization contract is missing: {marker}")
    for marker in (
        "COMMENT_ID:",
        "comment_matches_current_unit()",
        "Ignoring a stale/ambiguous course command",
        "timeout --signal=TERM --kill-after=5s 90s python3 .gh900/validate_activity.py",
        "cleanup_stale_course_branches()",
    ):
        if marker not in engine:
            errors.append(f"Course engine resilience contract is missing: {marker}")

    if errors:
        print("Fixture/runtime contract failures:")
        for item in errors:
            print(f"- {item}")
        return 1

    print(
        f"Fixture/runtime contracts passed: {len(calls)} copied fixtures, 12 activity modules, "
        "16 clean assessments with complete/decodable hash coverage, serialized/idempotent runtime."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
