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

REQUIRED_ARTIFACTS = {
    4: ["labs/module-04/code-scanning-simulation.yml"],
    6: [".devcontainer/devcontainer.json"],
    8: ["labs/module-08/markdown-practice.md"],
    10: ["labs/module-10/innersource-program.md"],
    11: ["SECURITY.md", ".github/CODEOWNERS"],
    12: ["labs/module-12/admin-matrix.md"],
    13: ["labs/module-13/identity-scenarios.md"],
}


def evidence_value(text: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*(.+?)\s*$", text)
    return match.group(1).strip() if match else None


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)


def validate_recorded_commit(submission: str, field: str, errors: list[str]) -> None:
    value = evidence_value(submission, field) or ""
    if value == "REPLACE_ME" or not re.fullmatch(r"[0-9a-fA-F]{7,40}", value):
        errors.append(f"{field} must contain the Git commit SHA produced by that checkpoint.")
        return
    resolved = git("rev-parse", "--verify", f"{value}^{{commit}}")
    if resolved.returncode != 0:
        errors.append(f"{field} does not resolve to a commit in this repository.")
        return
    ancestor = git("merge-base", "--is-ancestor", value, "HEAD")
    if ancestor.returncode != 0:
        errors.append(f"{field} must identify a commit contained in the current lab branch history.")


def validate_module1(errors: list[str]) -> None:
    submission_path = ROOT / "labs/module-01/submission.md"
    notes_path = ROOT / "labs/module-01/version-control-notes.md"
    diff_path = ROOT / "labs/module-01/diff-practice.txt"
    vscode_path = ROOT / "labs/module-01/vscode-branch.txt"

    for path in [submission_path, notes_path, diff_path, vscode_path]:
        if not path.exists():
            errors.append(f"Required Module 1 lab file is missing: {path.relative_to(ROOT)}")
    if errors:
        return

    submission = submission_path.read_text(encoding="utf-8")
    if "ACTIVITY_STATUS: COMPLETE" not in submission:
        errors.append("Set ACTIVITY_STATUS to COMPLETE only after all six Module 1 checkpoints are done.")
    if "REPLACE_ME" in submission:
        errors.append("Replace every Module 1 EVIDENCE_* placeholder with your own durable evidence.")

    notes = notes_path.read_text(encoding="utf-8")
    if "TODO:" in notes:
        errors.append("Finish every TODO in labs/module-01/version-control-notes.md.")
    if "Temporary status line" in diff_path.read_text(encoding="utf-8"):
        errors.append("Remove the Temporary status line from diff-practice.txt after completing the diff/stage/unstage exercise.")
    if "TODO:" in vscode_path.read_text(encoding="utf-8"):
        errors.append("Complete the TODO in labs/module-01/vscode-branch.txt.")

    fetch = git("fetch", "origin", "main")
    if fetch.returncode == 0:
        count = git("rev-list", "--count", "origin/main..HEAD")
        if count.returncode == 0 and int(count.stdout.strip() or "0") < 4:
            errors.append("Module 1 requires at least four learner commits beyond main (CLI, VS Code, diff, and branch practice).")
        merges = git("rev-list", "--merges", "origin/main..HEAD")
        if merges.returncode == 0 and not merges.stdout.strip():
            errors.append("Create and merge the temporary practice branch with a visible merge commit.")
        for rel in [
            "labs/module-01/version-control-notes.md",
            "labs/module-01/diff-practice.txt",
            "labs/module-01/vscode-branch.txt",
        ]:
            changed = git("diff", "--quiet", "origin/main...HEAD", "--", rel)
            if changed.returncode == 0:
                errors.append(f"The lab branch must contain a real change to {rel}.")

    for field in ["EVIDENCE_CLI_COMMIT", "EVIDENCE_VSCODE_COMMIT", "EVIDENCE_DIFF_COMMIT", "EVIDENCE_MERGE_COMMIT"]:
        validate_recorded_commit(submission, field, errors)


def validate_code_scanning_simulation(errors: list[str]) -> None:
    path = ROOT / "labs/module-04/code-scanning-simulation.yml"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if "TODO" in text:
        errors.append("Complete every TODO in labs/module-04/code-scanning-simulation.yml.")
    required_facts = {
        "SARIF version 2.1.0": r"(?i)sarif_version:\s*['\"]?2\.1\.0",
        "upload-sarif action": r"(?i)upload_action:.*upload-sarif",
        "5,000-result pinned limit": r"(?i)max_results_per_upload_in_pinned_lesson:\s*['\"]?5[,]?000",
        "10 MB compressed pinned limit": r"(?i)max_gzip_size_mb_in_pinned_lesson:\s*['\"]?10",
    }
    for label, pattern in required_facts.items():
        if not re.search(pattern, text):
            errors.append(f"Code-scanning simulation is missing the {label} from the pinned lesson.")


def validate_devcontainer(errors: list[str]) -> None:
    path = ROOT / ".devcontainer/devcontainer.json"
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f".devcontainer/devcontainer.json must remain valid JSON: {exc}")
        return
    serialized = json.dumps(data)
    if "TODO" in serialized:
        errors.append("Customize .devcontainer/devcontainer.json and remove the TODO marker.")
    if not data.get("name"):
        errors.append("devcontainer.json needs a descriptive name.")
    if not any(key in data for key in ("image", "build", "dockerFile")):
        errors.append("devcontainer.json must identify an image/build configuration.")
    if not any(key in data for key in ("customizations", "features", "postCreateCommand", "forwardPorts")):
        errors.append("Make at least one meaningful dev-container customization.")


def validate_markdown(errors: list[str]) -> None:
    path = ROOT / "labs/module-08/markdown-practice.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    heading_levels = set(re.findall(r"(?m)^(#{1,6})\s+\S", text))
    if len(heading_levels) < 2:
        errors.append("Markdown practice needs at least two distinct heading levels.")
    checks = {
        "bold emphasis": r"\*\*[^*\n]+\*\*|__[^_\n]+__",
        "italic emphasis": r"(?<!\*)\*[^*\n]+\*(?!\*)|(?<!_)_[^_\n]+_(?!_)",
        "ordered list": r"(?m)^\s*\d+\.\s+\S",
        "unordered list": r"(?m)^\s*[-*]\s+\S",
        "task list": r"(?m)^\s*- \[[ xX]\] ",
        "inline code": r"(?<!`)`[^`\n]+`(?!`)",
        "fenced code": r"```",
        "link": r"\[[^\]]+\]\([^\)]+\)",
        "image": r"!\[[^\]]*\]\([^\)]+\)",
        "blockquote": r"(?m)^>\s+",
        "table": r"(?m)^\s*\|?.+\|.+\|\s*$",
        "GitHub-flavored collaboration reference": r"(?m)(?:^|\s)(?:#\d+|@[A-Za-z0-9-]+|[0-9a-f]{7,40})(?:\s|$)",
    }
    for label, pattern in checks.items():
        if not re.search(pattern, text):
            errors.append(f"Markdown practice is missing: {label}.")


def require_terms(path: Path, groups: dict[str, tuple[str, ...]], errors: list[str], minimum_length: int = 300) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8").lower()
    if len(text.strip()) < minimum_length:
        errors.append(f"{path.relative_to(ROOT)} is too short to demonstrate the requested scenario.")
    for label, alternatives in groups.items():
        if not any(term.lower() in text for term in alternatives):
            errors.append(f"{path.relative_to(ROOT)} must address {label}.")


def validate_innersource(errors: list[str]) -> None:
    require_terms(
        ROOT / "labs/module-10/innersource-program.md",
        {
            "purpose": ("purpose", "goal"),
            "discoverability": ("discover", "catalog", "find"),
            "contribution process": ("contribut", "pull request"),
            "maintainers/ownership": ("maintainer", "owner"),
            "review": ("review",),
            "support expectations": ("support", "response"),
            "governance/security": ("governance", "security", "least privilege"),
        },
        errors,
        500,
    )


def validate_security_files(errors: list[str]) -> None:
    security = ROOT / "SECURITY.md"
    if security.exists():
        text = security.read_text(encoding="utf-8").lower()
        if len(text.strip()) < 200 or "vulnerab" not in text or not any(x in text for x in ("report", "contact", "disclos")):
            errors.append("SECURITY.md must provide a meaningful vulnerability-reporting/disclosure policy.")
    codeowners = ROOT / ".github/CODEOWNERS"
    if codeowners.exists():
        effective = [line for line in codeowners.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")]
        if not effective or not any("@" in line for line in effective):
            errors.append(".github/CODEOWNERS must contain at least one real path-to-owner rule using an @owner/team token.")


def validate_admin_matrix(errors: list[str]) -> None:
    require_terms(
        ROOT / "labs/module-12/admin-matrix.md",
        {
            "repository scope": ("repository",),
            "organization scope": ("organization",),
            "enterprise scope": ("enterprise",),
            "least privilege": ("least privilege", "least-privilege"),
            "roles/permissions": ("role", "permission"),
            "EMU": ("emu", "enterprise managed user"),
            "governance/policy": ("governance", "policy"),
        },
        errors,
        600,
    )


def validate_identity_scenarios(errors: list[str]) -> None:
    require_terms(
        ROOT / "labs/module-13/identity-scenarios.md",
        {
            "2FA": ("2fa", "two-factor"),
            "passkeys": ("passkey", "webauthn"),
            "PAT/HTTPS or SSH": ("pat", "personal access token", "ssh"),
            "OAuth/GitHub Apps": ("oauth", "github app"),
            "SAML SSO": ("saml", "sso"),
            "SCIM": ("scim",),
            "team synchronization": ("team sync", "team synchronization"),
            "authentication vs authorization": ("authentication", "authorization"),
        },
        errors,
        700,
    )


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


def parse_issue_or_pr(value: str, kind: str) -> str | None:
    pattern = r"(?:#|/issues/)(\d+)" if kind == "issue" else r"(?:#|/pull/)(\d+)"
    match = re.search(pattern, value)
    return match.group(1) if match else None


def verify_issue(field_value: str, errors: list[str], label: str = "Issue") -> str | None:
    number = parse_issue_or_pr(field_value, "issue")
    if not number:
        errors.append(f"{label} evidence must reference a real Issue number or URL.")
        return None
    check = subprocess.run(["gh", "issue", "view", number], cwd=ROOT, capture_output=True)
    if check.returncode != 0:
        errors.append(f"The recorded {label} cannot be found in this learner repository.")
        return None
    return number


def verify_pr(field_value: str, errors: list[str], expected_head: str | None = None) -> tuple[str | None, dict[str, str] | None]:
    number = parse_issue_or_pr(field_value, "pr")
    if not number:
        errors.append("Pull Request evidence must reference a real PR number or URL.")
        return None, None
    check = subprocess.run(
        ["gh", "pr", "view", number, "--json", "body,headRefName,baseRefName,url"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if check.returncode != 0:
        errors.append("The recorded Pull Request cannot be found in this learner repository.")
        return None, None
    data = json.loads(check.stdout)
    if expected_head and data.get("headRefName") != expected_head:
        errors.append(f"The recorded Pull Request must use head branch {expected_head}.")
    return number, data


def validate_repo_evidence(module: int, text: str, errors: list[str]) -> None:
    if module == 7:
        project = evidence_value(text, "EVIDENCE_PROJECT_URL") or ""
        if not re.match(r"https://github\.com/(?:users|orgs)/[^/]+/projects/\d+(?:/.*)?$", project):
            errors.append("EVIDENCE_PROJECT_URL must be a GitHub user/org Project URL.")

    if module == 15:
        commit = evidence_value(text, "EVIDENCE_HISTORY_COMMIT") or ""
        if not re.fullmatch(r"[0-9a-fA-F]{7,40}", commit) or git("rev-parse", "--verify", f"{commit}^{{commit}}").returncode != 0:
            errors.append("EVIDENCE_HISTORY_COMMIT must be a real commit SHA in this repository.")
        tag = evidence_value(text, "EVIDENCE_TAG_NAME") or ""
        if tag == "REPLACE_ME" or not tag or git("rev-parse", "--verify", f"refs/tags/{tag}").returncode != 0:
            errors.append("EVIDENCE_TAG_NAME must name a tag that exists in this repository (push the practice tag).")

    # GitHub-object verification needs Actions + gh credentials.
    if not os.environ.get("GITHUB_ACTIONS") or not shutil.which("gh"):
        return

    if module == 2:
        verify_issue(evidence_value(text, "EVIDENCE_ISSUE") or "", errors)
        verify_pr(evidence_value(text, "EVIDENCE_PR") or "", errors, "lab/module-02")

    if module == 9:
        pr_value = evidence_value(text, "EVIDENCE_COURSE_PR") or ""
        verify_pr(pr_value, errors, "lab/module-09")
        external = evidence_value(text, "EVIDENCE_OPEN_SOURCE_REPO") or ""
        if not re.match(r"https://github\.com/[^/\s]+/[^/\s#?]+/?$", external):
            errors.append("EVIDENCE_OPEN_SOURCE_REPO must be a GitHub repository URL you inspected.")

    if module == 14:
        issue_num = verify_issue(evidence_value(text, "EVIDENCE_ISSUE") or "", errors)
        _, pr = verify_pr(evidence_value(text, "EVIDENCE_PR") or "", errors, "lab/module-14")
        if pr and issue_num and not re.search(rf"(?<!\d)#{re.escape(issue_num)}(?!\d)", pr.get("body", "")):
            errors.append("The Module 14 PR body must explicitly reference the recorded Issue number.")
        if pr and pr.get("baseRefName") != "main":
            errors.append("The Module 14 PR should target main for this lab.")


def validate_evidence_quality(text: str, errors: list[str]) -> None:
    for name, value in re.findall(r"(?m)^(EVIDENCE_[A-Z0-9_]+):\s*(.+?)\s*$", text):
        value = value.strip()
        if value == "REPLACE_ME":
            continue
        structural = any(token in name for token in ("_FILE", "_POLICY", "CODEOWNERS", "_URL", "_ISSUE", "_PR", "_COMMIT", "_TAG"))
        if not structural and len(value) < 20:
            errors.append(f"{name} is too brief; record meaningful evidence/observation rather than a one-word completion marker.")


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

    activity_part = text.split("## Knowledge check", 1)[0]
    if "REPLACE_ME" in activity_part:
        errors.append("Replace every hands-on REPLACE_ME evidence placeholder with your own evidence/notes.")
    validate_evidence_quality(activity_part, errors)

    for rel in REQUIRED_ARTIFACTS.get(module, []):
        if not (ROOT / rel).exists():
            errors.append(f"Required hands-on artifact is missing: {rel}")

    if module == 4:
        validate_code_scanning_simulation(errors)
    if module == 6:
        validate_devcontainer(errors)
    if module == 8:
        validate_markdown(errors)
    if module == 10:
        validate_innersource(errors)
    if module == 11:
        validate_security_files(errors)
    if module == 12:
        validate_admin_matrix(errors)
    if module == 13:
        validate_identity_scenarios(errors)
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
