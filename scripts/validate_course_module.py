#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HASH_FILE = ROOT / "curriculum" / "assessment-hashes.json"

MODULE_TITLES = {
    2: "Introduction to GitHub",
    3: "Introduction to GitHub's products",
    4: "Configure code scanning on GitHub",
    5: "Introduction to GitHub Copilot",
    6: "Code with GitHub Codespaces",
    7: "Manage your work with GitHub Projects",
    8: "Communicate effectively on GitHub using Markdown",
    9: "Contribute to an open-source project on GitHub",
    10: "Manage an InnerSource program by using GitHub",
    11: "Maintain a secure repository by using GitHub best practices",
    12: "Introduction to GitHub administration",
    13: "Authenticate and authorize user identities on GitHub",
    14: "Manage repository changes by using pull requests on GitHub",
    15: "Search and organize repository history by using GitHub",
    16: "Using GitHub Copilot with Python",
}

REQUIRED_ARTIFACTS = {
    8: ["labs/module-08/markdown-practice.md"],
    10: ["labs/module-10/innersource-program.md"],
    11: ["SECURITY.md", ".github/CODEOWNERS"],
    12: ["labs/module-12/admin-matrix.md"],
    13: ["labs/module-13/identity-scenarios.md"],
}


def digest(module: int, question: str, answer: str) -> str:
    raw = f"m{module:02d}:{question}:{answer}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def module_from_ref() -> int | None:
    ref = os.environ.get("GITHUB_REF_NAME", "")
    match = re.fullmatch(r"lab/module-(\d{2})", ref)
    return int(match.group(1)) if match else None


def parse_answers(text: str) -> tuple[dict[str, str], list[str]]:
    sections = re.split(r"(?=^### Q\d+\s*$)", text, flags=re.MULTILINE)
    parsed: dict[str, str] = {}
    malformed: list[str] = []
    for section in sections:
        header = re.match(r"^### (Q\d+)\s*$", section, flags=re.MULTILINE)
        if not header:
            continue
        question = header.group(1)
        checked = re.findall(r"^- \[[xX]\] ([A-C])\.", section, flags=re.MULTILINE)
        if len(checked) != 1:
            malformed.append(question)
        else:
            parsed[question] = checked[0]
    return parsed, malformed


def validate_markdown_practice(errors: list[str]) -> None:
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
            errors.append(f"Module 8 Markdown practice is missing: {label}.")


def validate_python_exercise(errors: list[str]) -> None:
    app = ROOT / "labs/module-16/app.py"
    if not app.exists():
        errors.append("Module 16 Python exercise file is missing.")
        return
    if "NotImplementedError" in app.read_text(encoding="utf-8"):
        errors.append("Module 16 summarize_scores is still unimplemented.")
        return
    result = subprocess.run(
        [sys.executable, "test_app.py"],
        cwd=ROOT / "labs/module-16",
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        details = (result.stdout + "\n" + result.stderr).strip()
        errors.append("Module 16 Python tests failed:\n" + details[-1500:])


def validate(module: int) -> tuple[bool, str]:
    if module not in MODULE_TITLES:
        return False, f"Unsupported module: {module}. This validator covers Modules 2-16."

    submission = ROOT / f"labs/module-{module:02d}/submission.md"
    if not submission.exists():
        return False, f"Missing submission file: {submission.relative_to(ROOT)}"

    text = submission.read_text(encoding="utf-8")
    errors: list[str] = []

    if "ACTIVITY_STATUS: COMPLETE" not in text:
        errors.append("Set ACTIVITY_STATUS to COMPLETE only after finishing the hands-on activities.")
    if "REPLACE_ME" in text:
        errors.append("Replace every REPLACE_ME evidence placeholder with your own evidence/notes.")

    for rel in REQUIRED_ARTIFACTS.get(module, []):
        if not (ROOT / rel).exists():
            errors.append(f"Required hands-on artifact is missing: {rel}")

    parsed, malformed = parse_answers(text)
    expected = json.loads(HASH_FILE.read_text(encoding="utf-8"))[f"{module:02d}"]
    if malformed or set(parsed) != set(expected):
        bad = sorted(set(malformed) | (set(expected) - set(parsed)))
        errors.append("Select exactly one answer for every question. Needs attention: " + ", ".join(bad))
    else:
        wrong = [q for q, a in parsed.items() if digest(module, q, a) != expected[q]]
        if wrong:
            errors.append("Knowledge check needs review: " + ", ".join(sorted(wrong)))

    if module == 8:
        validate_markdown_practice(errors)
    if module == 16:
        validate_python_exercise(errors)

    if errors:
        return False, "\n".join(f"- {item}" for item in errors)

    return True, f"Module {module} complete — {MODULE_TITLES[module]}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", type=int)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    module = args.module or module_from_ref()
    if module is None:
        message = "Cannot infer module. Use --module N or run on branch lab/module-NN."
        if args.json:
            print(json.dumps({"passed": False, "module": None, "message": message}))
        else:
            print(message)
        return 2

    passed, message = validate(module)
    if args.json:
        print(json.dumps({"passed": passed, "module": module, "title": MODULE_TITLES.get(module), "message": message}))
    else:
        print(message)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
