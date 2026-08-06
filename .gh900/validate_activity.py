#!/usr/bin/env python3
"""Hardened entrypoint for GH-900 hands-on validation.

The large module-specific implementation lives in validate_activity_core.py. This
entrypoint patches cross-cutting runtime contracts that are easier to test and reason
about centrally: immutable setup baselines, full Issue-comment pagination, and direct
behavior checks for generated Python exercises.
"""
from __future__ import annotations

import argparse
import os
import py_compile
import subprocess
import sys
from pathlib import Path

import validate_activity_core as core

ROOT = Path(__file__).resolve().parents[1]


def changed_from_sandbox(unit: str, rel: str) -> bool:
    """Compare learner output with the immutable [gh900 setup] commit.

    PR exercises may already have been merged into the sandbox by the time validation
    runs. Comparing HEAD to the *current* sandbox would therefore erase the learner
    diff and incorrectly fail a valid exercise.
    """
    baseline = core.baseline_commit(unit)
    if not baseline:
        return False
    return core.git("diff", "--quiet", f"{baseline}...HEAD", "--", rel).returncode == 1


def course_comment_bodies(prefix: str) -> list[str]:
    """Read every course comment, not only the first page returned by gh issue view."""
    if not os.environ.get("GITHUB_ACTIONS"):
        return []
    issue = core.course_issue()
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not issue or not repo:
        return []
    number = issue.get("number")
    if not number:
        return []
    result = subprocess.run(
        [
            "gh", "api", "--paginate",
            f"repos/{repo}/issues/{number}/comments",
            "--jq", ".[].body",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip().lower().startswith(prefix.lower())]


def _run_python(code: str, cwd: Path) -> tuple[bool, str]:
    result = subprocess.run([sys.executable, "-c", code], cwd=cwd, text=True, capture_output=True)
    return result.returncode == 0, (result.stdout + "\n" + result.stderr).strip()


def validate_module5(unit: str, errors: list[str]) -> None:
    core._validate_module5_original(unit, errors)
    ok, details = _run_python(
        "from copilot_practice import summarize_items; "
        "assert summarize_items(['beta','alpha']) == '2 items: alpha, beta'; "
        "\ntry:\n summarize_items([])\nexcept ValueError:\n pass\nelse:\n raise AssertionError('empty input must raise ValueError')",
        ROOT / "exercise",
    )
    if not ok:
        errors.append("The Copilot practice behavior checks failed." + (f"\n{details[-800:]}" if details else ""))


def validate_module8(unit: str, errors: list[str]) -> None:
    core._validate_module8_original(unit, errors)
    path = ROOT / "exercise" / "markdown-showcase.md"
    if path.exists() and "TODO" in path.read_text(encoding="utf-8"):
        errors.append("Remove the Markdown starter TODO after completing the showcase.")


def validate_module14(unit: str, errors: list[str]) -> None:
    core._validate_module14_original(unit, errors)
    ok, details = _run_python(
        "from review_fixture import normalized_name; "
        "assert normalized_name('  Ada Lovelace ') == 'ada lovelace'; "
        "\ntry:\n normalized_name('   ')\nexcept ValueError:\n pass\nelse:\n raise AssertionError('blank input must raise ValueError')",
        ROOT / "exercise",
    )
    if not ok:
        errors.append("The Pull Request review fixture behavior checks failed." + (f"\n{details[-800:]}" if details else ""))


def validate_module16(unit: str, errors: list[str]) -> None:
    core._validate_module16_original(unit, errors)
    requirements = ROOT / "exercise" / "requirements.txt"
    if not requirements.exists():
        errors.append("The FastAPI exercise requirements.txt file is missing.")
    else:
        text = requirements.read_text(encoding="utf-8").lower()
        for dependency in ("fastapi", "uvicorn", "httpx"):
            if dependency not in text:
                errors.append(f"requirements.txt must retain the `{dependency}` dependency for this exercise.")
    for rel in ("exercise/app.py", "exercise/test_app.py"):
        path = ROOT / rel
        if not path.exists():
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{rel} must remain valid Python: {exc.msg}")


# Preserve original implementations, then install the hardened contracts into the
# core module's global namespace. Functions defined in the core resolve these names
# at call time, so all existing module validators inherit the fixes.
core._validate_module5_original = core.validate_module5
core._validate_module8_original = core.validate_module8
core._validate_module14_original = core.validate_module14
core._validate_module16_original = core.validate_module16
core.changed_from_sandbox = changed_from_sandbox
core.course_comment_bodies = course_comment_bodies
core.validate_module5 = validate_module5
core.validate_module8 = validate_module8
core.validate_module14 = validate_module14
core.validate_module16 = validate_module16


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", required=True)
    args = parser.parse_args()
    errors = core.validate(args.unit)
    if errors:
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print(f"{args.unit} hands-on checkpoint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
