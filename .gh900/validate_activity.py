#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PR_MODULES = {2, 9, 14}


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)


def fetch_sandbox(unit: str) -> bool:
    remote = f"refs/heads/sandbox/{unit}"
    local = f"refs/remotes/origin/sandbox/{unit}"
    return git("fetch", "origin", f"{remote}:{local}").returncode == 0


def baseline_commit(unit: str) -> str | None:
    if not fetch_sandbox(unit):
        return None
    ref = f"origin/sandbox/{unit}"
    result = git(
        "log",
        ref,
        "--format=%H",
        "-n",
        "1",
        "--fixed-strings",
        f"--grep=[gh900 setup] {unit}",
    )
    value = result.stdout.strip() if result.returncode == 0 else ""
    return value or None


def changed_from_baseline(unit: str, rel: str) -> bool:
    baseline = baseline_commit(unit)
    if not baseline:
        return False
    result = git("diff", "--quiet", f"{baseline}...HEAD", "--", rel)
    return result.returncode == 1


def learner_commit_count(unit: str) -> int:
    baseline = baseline_commit(unit)
    if not baseline:
        return 0
    result = git("rev-list", "--count", f"{baseline}..HEAD")
    return int(result.stdout.strip() or "0") if result.returncode == 0 else 0


def learner_merge_count(unit: str) -> int:
    baseline = baseline_commit(unit)
    if not baseline:
        return 0
    result = git("rev-list", "--count", "--merges", f"{baseline}..HEAD")
    return int(result.stdout.strip() or "0") if result.returncode == 0 else 0


def require_changed(unit: str, rel: str, errors: list[str]) -> None:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"Required exercise file is missing: {rel}")
    elif not changed_from_baseline(unit, rel):
        errors.append(f"Make a real change to {rel} on the learner branch.")


def validate_module1(unit: str, errors: list[str]) -> None:
    for rel in [
        "exercise/version-control-notes.md",
        "exercise/diff-practice.txt",
        "exercise/vscode-branch.txt",
    ]:
        require_changed(unit, rel, errors)
    notes = ROOT / "exercise/version-control-notes.md"
    diff = ROOT / "exercise/diff-practice.txt"
    vscode = ROOT / "exercise/vscode-branch.txt"
    if notes.exists() and "TODO:" in notes.read_text(encoding="utf-8"):
        errors.append("Finish every TODO in exercise/version-control-notes.md.")
    if diff.exists() and "Temporary status line" in diff.read_text(encoding="utf-8"):
        errors.append("Remove the temporary status line after completing the diff/stage/unstage exercise.")
    if vscode.exists() and "TODO:" in vscode.read_text(encoding="utf-8"):
        errors.append("Finish the VS Code branch exercise TODO.")
    if learner_commit_count(unit) < 3:
        errors.append("Create at least three learner commits during the Git exercise.")
    if learner_merge_count(unit) < 1:
        errors.append("Create and merge the temporary practice branch so the merge is visible in history.")


def validate_code_scanning(unit: str, errors: list[str]) -> None:
    rel = "exercise/code-scanning-simulation.yml"
    require_changed(unit, rel, errors)
    path = ROOT / rel
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if "TODO" in text:
        errors.append("Complete every TODO in the code-scanning simulation.")
    checks = {
        "SARIF 2.1.0": r"(?i)sarif_version:\s*['\"]?2\.1\.0",
        "upload-sarif": r"(?i)upload_action:.*upload-sarif",
        "5,000 result limit": r"(?i)max_results_per_upload_in_pinned_lesson:\s*['\"]?5[,]?000",
        "10 MB compressed limit": r"(?i)max_gzip_size_mb_in_pinned_lesson:\s*['\"]?10",
    }
    for label, pattern in checks.items():
        if not re.search(pattern, text):
            errors.append(f"Code-scanning exercise is missing: {label}.")


def validate_copilot(unit: str, errors: list[str]) -> None:
    rel = "exercise/copilot-practice.py"
    require_changed(unit, rel, errors)
    path = ROOT / rel
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if "TODO" in text or "NotImplementedError" in text or len(text.strip()) < 180:
            errors.append("Complete the Python practice implementation and remove the TODO/NotImplementedError.")


def validate_devcontainer(unit: str, errors: list[str]) -> None:
    rel = ".devcontainer/devcontainer.json"
    require_changed(unit, rel, errors)
    path = ROOT / rel
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"devcontainer.json is invalid JSON: {exc}")
        return
    if "TODO" in json.dumps(data):
        errors.append("Customize devcontainer.json and remove the TODO marker.")
    if not data.get("name"):
        errors.append("devcontainer.json needs a descriptive name.")
    if not any(k in data for k in ("customizations", "features", "postCreateCommand", "forwardPorts")):
        errors.append("Make at least one meaningful dev-container customization.")


def validate_markdown(unit: str, errors: list[str]) -> None:
    rel = "exercise/markdown-practice.md"
    require_changed(unit, rel, errors)
    path = ROOT / rel
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    checks = {
        "two heading levels": len(set(re.findall(r"(?m)^(#{1,6})\s+\S", text))) >= 2,
        "bold": bool(re.search(r"\*\*[^*\n]+\*\*", text)),
        "ordered list": bool(re.search(r"(?m)^\s*\d+\.\s+\S", text)),
        "task list": bool(re.search(r"(?m)^\s*- \[[ xX]\] ", text)),
        "fenced code": "```" in text,
        "link": bool(re.search(r"\[[^\]]+\]\([^)]+\)", text)),
        "table": bool(re.search(r"(?m)^\s*\|?.+\|.+\|\s*$", text)),
        "blockquote": bool(re.search(r"(?m)^>\s+", text)),
    }
    for label, ok in checks.items():
        if not ok:
            errors.append(f"Markdown exercise is missing: {label}.")


def validate_innersource(unit: str, errors: list[str]) -> None:
    rel = "exercise/innersource-program.md"
    require_changed(unit, rel, errors)
    path = ROOT / rel
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8").lower()
    groups = {
        "purpose": ("purpose", "goal"),
        "discoverability": ("discover", "catalog"),
        "contribution process": ("contribut", "pull request"),
        "ownership": ("maintainer", "owner"),
        "review": ("review",),
        "support": ("support", "response"),
        "governance/security": ("governance", "security", "least privilege"),
    }
    if len(text.strip()) < 500:
        errors.append("InnerSource program artifact is too short.")
    for label, terms in groups.items():
        if not any(t in text for t in terms):
            errors.append(f"InnerSource artifact must address {label}.")


def validate_security(unit: str, errors: list[str]) -> None:
    security = ROOT / "SECURITY.md"
    owners = ROOT / ".github/CODEOWNERS"
    if not security.exists():
        errors.append("Create SECURITY.md as instructed.")
    else:
        text = security.read_text(encoding="utf-8").lower()
        if len(text.strip()) < 200 or "vulnerab" not in text or not any(x in text for x in ("report", "contact", "disclos")):
            errors.append("SECURITY.md needs a meaningful vulnerability reporting/disclosure policy.")
    if not owners.exists():
        errors.append("Create .github/CODEOWNERS as instructed.")
    else:
        lines = [x for x in owners.read_text(encoding="utf-8").splitlines() if x.strip() and not x.lstrip().startswith("#")]
        if not lines or not any("@" in x for x in lines):
            errors.append("CODEOWNERS needs at least one real path-to-owner rule.")
    if security.exists() and not changed_from_baseline(unit, "SECURITY.md"):
        errors.append("SECURITY.md must be created on the learner branch.")
    if owners.exists() and not changed_from_baseline(unit, ".github/CODEOWNERS"):
        errors.append("CODEOWNERS must be created on the learner branch.")


def gh_json(args: list[str]) -> object | None:
    if not os.environ.get("GITHUB_ACTIONS") or not shutil.which("gh"):
        return None
    result = subprocess.run(["gh", *args], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def validate_pr_activity(unit: str, module: int, errors: list[str]) -> None:
    rel = {
        2: "exercise/github-flow.md",
        9: "exercise/open-source-pr.md",
        14: "exercise/review_fixture.py",
    }[module]
    require_changed(unit, rel, errors)
    if not os.environ.get("GITHUB_ACTIONS") or not shutil.which("gh"):
        return

    prs = gh_json([
        "pr", "list", "--state", "merged", "--limit", "100",
        "--json", "number,headRefName,baseRefName,body,title"
    ]) or []
    expected_head = f"lab/{unit}"
    expected_base = f"sandbox/{unit}"
    matches = [p for p in prs if p.get("headRefName") == expected_head and p.get("baseRefName") == expected_base]
    if not matches:
        errors.append(f"Merge a Pull Request from {expected_head} into {expected_base}.")
        return
    pr = matches[-1]
    if module in {2, 14}:
        issues = gh_json(["issue", "list", "--state", "all", "--limit", "100", "--json", "number,title"]) or []
        tag = f"[GH-900 {unit}]"
        matching_issues = [i for i in issues if tag.lower() in i.get("title", "").lower()]
        if not matching_issues:
            errors.append(f"Create an Issue whose title includes {tag}.")
        elif module == 14:
            nums = {str(i["number"]) for i in matching_issues}
            body = pr.get("body", "")
            if not any(re.search(rf"(?<!\d)#{re.escape(n)}(?!\d)", body) for n in nums):
                errors.append("The Module 14 PR body must reference the exercise Issue number.")


def validate_history(unit: str, errors: list[str]) -> None:
    rel = "exercise/history-practice.txt"
    require_changed(unit, rel, errors)
    if learner_commit_count(unit) < 2:
        errors.append("Create at least two learner commits for the history exercise.")
    tag = f"gh900-{unit}"
    git("fetch", "origin", f"refs/tags/{tag}:refs/tags/{tag}")
    ref = git("rev-parse", "--verify", f"refs/tags/{tag}")
    if ref.returncode != 0:
        errors.append(f"Create tag {tag} and push it before running /check.")
    else:
        ancestor = git("merge-base", "--is-ancestor", ref.stdout.strip(), "HEAD")
        if ancestor.returncode != 0:
            errors.append(f"Tag {tag} must point to a commit in the learner branch history.")


def validate_python(unit: str, errors: list[str]) -> None:
    for rel in ("exercise/app.py", "exercise/test_app.py"):
        if not (ROOT / rel).exists():
            errors.append(f"Missing {rel}.")
    if errors:
        return
    if "NotImplementedError" in (ROOT / "exercise/app.py").read_text(encoding="utf-8"):
        errors.append("Complete the Python implementation.")
        return
    result = subprocess.run([sys.executable, "test_app.py"], cwd=ROOT / "exercise", text=True, capture_output=True)
    if result.returncode != 0:
        errors.append("Python tests are not passing yet.")


def validate(unit: str) -> list[str]:
    module = int(unit[1:3])
    errors: list[str] = []
    if module == 1:
        validate_module1(unit, errors)
    elif module in PR_MODULES:
        validate_pr_activity(unit, module, errors)
    elif module == 4:
        validate_code_scanning(unit, errors)
    elif module == 5:
        validate_copilot(unit, errors)
    elif module == 6:
        validate_devcontainer(unit, errors)
    elif module == 8:
        validate_markdown(unit, errors)
    elif module == 10:
        validate_innersource(unit, errors)
    elif module == 11:
        validate_security(unit, errors)
    elif module == 15:
        validate_history(unit, errors)
    elif module == 16:
        validate_python(unit, errors)
    else:
        if learner_commit_count(unit) < 1:
            errors.append("Make and push at least one meaningful learner commit for this exercise.")
    return errors


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--unit", required=True)
    args = p.parse_args()
    errors = validate(args.unit)
    if errors:
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print(f"{args.unit} hands-on checkpoint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
