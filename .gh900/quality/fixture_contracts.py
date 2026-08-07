#!/usr/bin/env python3
"""Verify that every on-demand workspace dependency exists before release."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GH900 = ROOT / ".gh900"
TEMPLATES = GH900 / "templates"
sys.path.insert(0, str(GH900))

import course_unit_state as state  # noqa: E402

EXPECTED_ACTIVITY_MODULES = {1, 2, 4, 5, 6, 8, 9, 10, 11, 14, 15, 16}


def main() -> int:
    errors: list[str] = []
    workspace = (GH900 / "workspace.py").read_text(encoding="utf-8")

    # Keep copy_template() calls and hidden source fixtures in lock-step.
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

    # The v2 runtime is Issue-first. Legacy answer/submission worksheets are not
    # runtime dependencies and must not accumulate in the hidden template package.
    legacy_worksheets = sorted(TEMPLATES.glob("labs/module-*/submission.md"))
    legacy_worksheets += sorted(TEMPLATES.glob("labs/module-*/assessment.md"))
    for path in legacy_worksheets:
        errors.append(f"Legacy worksheet must be removed: {path.relative_to(ROOT)}")

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

    # Assessments are rendered from canonical lesson/detail data and answer hashes;
    # learner worksheets must never be required. Verify all 16 remain renderable.
    for module in range(1, 17):
        try:
            _, count = state.assessment_questions(module)
        except Exception as exc:
            errors.append(f"Module {module} assessment fixture cannot render: {exc}")
            continue
        expected = 12 if module == 1 else 6
        if count != expected:
            errors.append(f"Module {module} expected {expected} assessment questions, got {count}")

    # Critical final-module fixture alignment: these files are generated together.
    for name in ("app.py", "test_app.py", "requirements.txt"):
        path = TEMPLATES / "labs" / "module-16" / name
        if not path.exists():
            errors.append(f"Module 16 FastAPI fixture is missing {path.relative_to(ROOT)}")

    if errors:
        print("Fixture contract failures:")
        for item in errors:
            print(f"- {item}")
        return 1

    print(f"Fixture contracts passed: {len(calls)} copied fixtures, 12 activity modules, 16 assessments, no legacy worksheets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
