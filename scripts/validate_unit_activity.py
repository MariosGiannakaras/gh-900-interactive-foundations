#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ARTIFACTS = {
    8: ["labs/module-08/markdown-practice.md"],
    10: ["labs/module-10/innersource-program.md"],
    11: ["SECURITY.md", ".github/CODEOWNERS"],
    12: ["labs/module-12/admin-matrix.md"],
    13: ["labs/module-13/identity-scenarios.md"],
}


def evidence_value(text: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*(.+?)\s*$", text)
    return match.group(1).strip() if match else None


def validate_module1(errors: list[str]) -> None:
    notes = ROOT / "labs/module-01/version-control-notes.md"
    if not notes.exists():
        errors.append("Module 1 version-control notes are missing.")
        return
    text = notes.read_text(encoding="utf-8")
    if "TODO:" in text:
        errors.append("Finish all TODO items in labs/module-01/version-control-notes.md.")
    try:
        subprocess.run(["git", "fetch", "origin", "main"], cwd=ROOT, check=False, capture_output=True)
        count = subprocess.run(
            ["git", "rev-list", "--count", "origin/main..HEAD"], cwd=ROOT, text=True, capture_output=True
        )
        if count.returncode == 0 and int(count.stdout.strip() or "0") < 2:
            errors.append("Module 1 activity requires at least two learner commits beyond main.")
    except Exception:
        pass


def validate_markdown(errors: list[str]) -> None:
    path = ROOT / "labs/module-08/markdown-practice.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    checks = {
        "heading": r"(?m)^#{1,6}\s+\S",
        "link": r"\[[^\]]+\]\([^\)]+\)",
        "image": r"!\[[^\]]*\]\([^\)]+\)",
        "task list": r"(?m)^\s*- \[[ xX]\] ",
        "fenced code": r"```",
        "table": r"(?m)^\s*\|.+\|\s*$",
        "blockquote": r"(?m)^>\s+",
    }
    for label, pattern in checks.items():
        if not re.search(pattern, text):
            errors.append(f"Markdown practice is missing: {label}.")


def validate_python(errors: list[str]) -> None:
    app = ROOT / "labs/module-16/app.py"
    if not app.exists() or "NotImplementedError" in app.read_text(encoding="utf-8"):
        errors.append("Complete the Module 16 Python implementation.")
        return
    result = subprocess.run(
        [sys.executable, "test_app.py"], cwd=ROOT / "labs/module-16", text=True, capture_output=True
    )
    if result.returncode != 0:
        errors.append("Module 16 Python tests are not passing yet.")


def validate_repo_evidence(module: int, text: str, errors: list[str]) -> None:
    # Stronger verification when the course runs on GitHub Actions. The static evidence
    # remains useful for features that cannot be inspected from a normal public repo.
    if not os.environ.get("GITHUB_ACTIONS") or not shutil.which("gh"):
        return
    if module == 2:
        issue = evidence_value(text, "EVIDENCE_ISSUE") or ""
        pr = evidence_value(text, "EVIDENCE_PR") or ""
        issue_num = re.search(r"(?:#|/issues/)(\d+)", issue)
        pr_num = re.search(r"(?:#|/pull/)(\d+)", pr)
        if not issue_num:
            errors.append("EVIDENCE_ISSUE must reference a real Issue number or URL.")
        else:
            check = subprocess.run(["gh", "issue", "view", issue_num.group(1)], cwd=ROOT, capture_output=True)
            if check.returncode != 0:
                errors.append("The recorded Module 2 Issue cannot be found in this repository.")
        if not pr_num:
            errors.append("EVIDENCE_PR must reference a real Pull Request number or URL.")
        else:
            check = subprocess.run(["gh", "pr", "view", pr_num.group(1)], cwd=ROOT, capture_output=True)
            if check.returncode != 0:
                errors.append("The recorded Module 2 Pull Request cannot be found in this repository.")


def validate(module: int) -> list[str]:
    errors: list[str] = []
    if module == 1:
        validate_module1(errors)
        return errors

    submission = ROOT / f"labs/module-{module:02d}/submission.md"
    if not submission.exists():
        return [f"Missing {submission.relative_to(ROOT)}"]
    text = submission.read_text(encoding="utf-8")

    if "ACTIVITY_STATUS: COMPLETE" not in text:
        errors.append("Set ACTIVITY_STATUS to COMPLETE after finishing this module's practical work.")

    # Assessment checkboxes are intentionally excluded from this phase. Evidence placeholders are not.
    activity_part = text.split("## Knowledge check", 1)[0]
    if "REPLACE_ME" in activity_part:
        errors.append("Replace every hands-on REPLACE_ME evidence placeholder with your own evidence/notes.")

    for rel in REQUIRED_ARTIFACTS.get(module, []):
        if not (ROOT / rel).exists():
            errors.append(f"Required hands-on artifact is missing: {rel}")

    if module == 8:
        validate_markdown(errors)
    if module == 16:
        validate_python(errors)
    validate_repo_evidence(module, text, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True, type=int)
    args = parser.parse_args()
    errors = validate(args.module)
    if errors:
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print(f"Module {args.module} hands-on checkpoint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
