#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_TITLE = "GH-900 Interactive Foundations — Course"


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
    result = git("log", "--format=%H", "-n", "1", "--fixed-strings", f"--grep=[gh900 setup] {unit}", ref)
    value = result.stdout.strip() if result.returncode == 0 else ""
    return value or None


def changed_from_baseline(unit: str, rel: str) -> bool:
    baseline = baseline_commit(unit)
    if not baseline:
        return False
    return git("diff", "--quiet", f"{baseline}...HEAD", "--", rel).returncode == 1


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


def require_no_todo(rel: str, errors: list[str]) -> str:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"Required exercise file is missing: {rel}")
        return ""
    text = path.read_text(encoding="utf-8")
    if re.search(r"(?i)\bTODO\b", text):
        errors.append(f"Finish every TODO in {rel}.")
    return text


def gh_json(args: list[str]) -> object | None:
    if not os.environ.get("GITHUB_ACTIONS"):
        return None
    result = subprocess.run(["gh", *args], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def gh_api_json(endpoint: str) -> object | None:
    if not os.environ.get("GITHUB_ACTIONS"):
        return None
    result = subprocess.run(["gh", "api", endpoint], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def course_issue() -> dict[str, object] | None:
    rows = gh_json(["issue", "list", "--state", "all", "--limit", "100", "--json", "number,title"])
    if not isinstance(rows, list):
        return None
    hit = next((row for row in rows if row.get("title") == COURSE_TITLE), None)
    if not hit:
        return None
    data = gh_json(["issue", "view", str(hit["number"]), "--json", "number,comments"])
    return data if isinstance(data, dict) else None


def course_comment_bodies(prefix: str) -> list[str]:
    issue = course_issue()
    if not issue:
        return []
    bodies: list[str] = []
    for comment in issue.get("comments", []):
        body = str(comment.get("body", "")).strip()
        if body.lower().startswith(prefix.lower()):
            bodies.append(body)
    return bodies


def require_reflection(groups: dict[str, tuple[str, ...]], errors: list[str], minimum: int = 100) -> None:
    bodies = course_comment_bodies("/reflection ")
    if not bodies:
        errors.append("Post the required `/reflection ...` response in the course Issue, then run `/check`.")
        return
    text = bodies[-1].lower()
    if len(text) < minimum:
        errors.append("The latest /reflection response is too short; explain what you did/observed and why.")
    for label, alternatives in groups.items():
        if not any(term.lower() in text for term in alternatives):
            errors.append(f"The /reflection response must address {label}.")


def find_issue_by_title(fragment: str) -> dict[str, object] | None:
    rows = gh_json(["issue", "list", "--state", "all", "--limit", "100", "--json", "number,title"])
    if not isinstance(rows, list):
        return None
    hit = next((row for row in rows if fragment.lower() in str(row.get("title", "")).lower()), None)
    if not hit:
        return None
    data = gh_json(["issue", "view", str(hit["number"]), "--json", "number,title,body,state,comments,labels,milestone,assignees"])
    return data if isinstance(data, dict) else None


def merged_pr_for_unit(unit: str) -> dict[str, object] | None:
    rows = gh_json(["pr", "list", "--state", "merged", "--limit", "100", "--json", "number,title,headRefName,baseRefName,body,comments,commits,mergeCommit"])
    if not isinstance(rows, list):
        return None
    head = f"lab/{unit}"
    base = f"sandbox/{unit}"
    return next((row for row in reversed(rows) if row.get("headRefName") == head and row.get("baseRefName") == base), None)


def validate_module1(unit: str, errors: list[str]) -> None:
    for rel in ["exercise/version-control-notes.md", "exercise/diff-practice.txt", "exercise/vscode-branch.txt"]:
        require_changed(unit, rel, errors)
    require_no_todo("exercise/version-control-notes.md", errors)
    require_no_todo("exercise/vscode-branch.txt", errors)
    diff = (ROOT / "exercise/diff-practice.txt").read_text(encoding="utf-8") if (ROOT / "exercise/diff-practice.txt").exists() else ""
    if "Temporary status line" in diff:
        errors.append("Remove the temporary status line after the diff/stage/unstage exercise.")
    if learner_commit_count(unit) < 3:
        errors.append("Create at least three learner commits during the Git exercise.")
    if learner_merge_count(unit) < 1:
        errors.append("Create and merge the temporary practice branch with a visible merge commit.")


def validate_module2(unit: str, errors: list[str]) -> None:
    require_changed(unit, "exercise/github-flow.md", errors)
    pr = merged_pr_for_unit(unit)
    issue = find_issue_by_title(f"[GH-900 {unit}]")
    if os.environ.get("GITHUB_ACTIONS") and not pr:
        errors.append(f"Merge a Pull Request from lab/{unit} into sandbox/{unit}.")
        return
    if os.environ.get("GITHUB_ACTIONS") and not issue:
        errors.append(f"Create an Issue whose title includes [GH-900 {unit}].")
        return
    if pr and issue and not re.search(rf"(?<!\d)#{issue['number']}(?!\d)", str(pr.get("body", ""))):
        errors.append("Link the training Pull Request to the exercise Issue in the PR body.")


def validate_module4(unit: str, errors: list[str]) -> None:
    workflow = ".github/workflows/module-04-codeql.yml"
    simulation = "exercise/code-scanning-simulation.yml"
    require_changed(unit, workflow, errors)
    require_changed(unit, simulation, errors)
    wtext = require_no_todo(workflow, errors).lower()
    stext = require_no_todo(simulation, errors)
    for label, token in {
        "push trigger": "push:",
        "pull-request trigger": "pull_request:",
        "scheduled trigger": "schedule:",
        "CodeQL initialization": "github/codeql-action/init",
        "CodeQL analysis": "github/codeql-action/analyze",
    }.items():
        if token.lower() not in wtext:
            errors.append(f"Temporary CodeQL workflow is missing {label}.")
    for label, pattern in {
        "SARIF 2.1.0": r"(?i)sarif_version:\s*['\"]?2\.1\.0",
        "upload-sarif": r"(?i)upload_action:.*upload-sarif",
        "5,000 result limit": r"(?i)max_results_per_upload_in_pinned_lesson:\s*['\"]?5[,]?000",
        "10 MB compressed limit": r"(?i)max_gzip_size_mb_in_pinned_lesson:\s*['\"]?10",
    }.items():
        if not re.search(pattern, stext):
            errors.append(f"Code-scanning simulation is missing {label}.")
    try:
        data = json.loads((ROOT / "exercise/sample.sarif.json").read_text(encoding="utf-8"))
        if data.get("version") != "2.1.0":
            errors.append("sample.sarif.json must remain SARIF 2.1.0.")
    except (OSError, json.JSONDecodeError):
        errors.append("Inspectable sample.sarif.json is missing or invalid.")
    require_reflection({
        "default setup": ("default",),
        "advanced setup": ("advanced",),
        "external/SARIF scanner": ("sarif", "external"),
        "Security or Actions observation": ("security", "actions", "workflow", "run"),
    }, errors, 140)


def validate_module5(unit: str, errors: list[str]) -> None:
    require_changed(unit, "exercise/copilot-practice.py", errors)
    require_changed(unit, "exercise/test_copilot_practice.py", errors)
    code = require_no_todo("exercise/copilot-practice.py", errors)
    tests = require_no_todo("exercise/test_copilot_practice.py", errors)
    if "NotImplementedError" in code:
        errors.append("Complete the Copilot practice implementation.")
    if len(tests.strip()) < 200 or "test_" not in tests:
        errors.append("Add meaningful tests to test_copilot_practice.py.")
    result = subprocess.run([sys.executable, "test_copilot_practice.py"], cwd=ROOT / "exercise", text=True, capture_output=True)
    if result.returncode != 0:
        errors.append("The Copilot practice tests are not passing.")
    require_reflection({
        "Copilot or fallback mode": ("copilot", "fallback", "unavailable"),
        "interaction mode": ("inline", "chat", "agent", "suggestion"),
        "review/rejection": ("reject", "changed", "modified", "review"),
    }, errors, 120)


def validate_module6(unit: str, errors: list[str]) -> None:
    rel = ".devcontainer/devcontainer.json"
    require_changed(unit, rel, errors)
    try:
        data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"devcontainer.json must be valid JSON: {exc}")
        return
    if "TODO" in json.dumps(data):
        errors.append("Customize devcontainer.json and remove its TODO marker.")
    if not data.get("name"):
        errors.append("devcontainer.json needs a descriptive name.")
    if not any(k in data for k in ("customizations", "features", "postCreateCommand", "forwardPorts")):
        errors.append("Make at least one meaningful dev-container customization.")
    require_reflection({
        "Codespaces terminal/compute": ("codespace", "terminal", "compute"),
        "github.dev distinction": ("github.dev",),
        "stop versus delete": ("stop", "stopping", "delete", "deleting"),
        "rebuild/container customization": ("rebuild", "devcontainer", "container"),
    }, errors, 120)


def validate_module8(unit: str, errors: list[str]) -> None:
    rel = "exercise/markdown-showcase.md"
    require_changed(unit, rel, errors)
    text = (ROOT / rel).read_text(encoding="utf-8") if (ROOT / rel).exists() else ""
    checks = {
        "two heading levels": len(set(re.findall(r"(?m)^(#{1,6})\s+\S", text))) >= 2,
        "bold": bool(re.search(r"\*\*[^*\n]+\*\*", text)),
        "italic": bool(re.search(r"(?<!\*)\*[^*\n]+\*(?!\*)|(?<!_)_[^_\n]+_(?!_)", text)),
        "ordered list": bool(re.search(r"(?m)^\s*\d+\.\s+\S", text)),
        "unordered list": bool(re.search(r"(?m)^\s*[-*]\s+\S", text)),
        "checked task": bool(re.search(r"(?m)^\s*- \[[xX]\] ", text)),
        "unchecked task": bool(re.search(r"(?m)^\s*- \[ \] ", text)),
        "external link": bool(re.search(r"\[[^\]]+\]\(https?://[^)]+\)", text)),
        "image alt text": bool(re.search(r"!\[[^\]]+\]\([^)]+\)", text)),
        "inline code": bool(re.search(r"(?<!`)`[^`\n]+`(?!`)", text)),
        "fenced code": bool(re.search(r"```[A-Za-z0-9_-]+", text)),
        "table": bool(re.search(r"(?m)^\s*\|?.+\|.+\|\s*$", text)),
        "blockquote": bool(re.search(r"(?m)^>\s+", text)),
        "Issue/PR reference": bool(re.search(r"(?<!\w)#\d+", text)),
        "mention syntax": bool(re.search(r"@[A-Za-z0-9-]+", text)),
        "GitHub alert": bool(re.search(r"(?m)^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", text)),
        "Mermaid/rich Markdown": "```mermaid" in text.lower() or "$$" in text,
    }
    for label, ok in checks.items():
        if not ok:
            errors.append(f"Markdown showcase is missing: {label}.")


def validate_module9(unit: str, errors: list[str]) -> None:
    require_changed(unit, "exercise/open-source-pr.md", errors)
    if learner_commit_count(unit) < 2:
        errors.append("Make an initial contribution commit and at least one update after review feedback.")
    pr = merged_pr_for_unit(unit)
    issue = find_issue_by_title(f"[GH-900 {unit}]")
    if os.environ.get("GITHUB_ACTIONS") and not pr:
        errors.append(f"Merge the temporary PR from lab/{unit} into sandbox/{unit}.")
        return
    if os.environ.get("GITHUB_ACTIONS") and not issue:
        errors.append("The temporary Module 9 contribution Issue is missing.")
        return
    if issue:
        intent = any(str(c.get("author", {}).get("login", "")).lower() != "github-actions[bot]" and len(str(c.get("body", "")).strip()) >= 10 for c in issue.get("comments", []))
        if not intent:
            errors.append("Comment your intent on the temporary Module 9 Issue before contributing.")
    if pr and issue:
        if not re.search(rf"(?<!\d)#{issue['number']}(?!\d)", str(pr.get("body", ""))):
            errors.append("Link the Module 9 Pull Request to the temporary Issue.")
        comments = pr.get("comments", [])
        if not any(f"gh900-review:{unit}" in str(c.get("body", "")) for c in comments):
            errors.append("The automated training review comment was not recorded on the PR.")
        learner_response = any(str(c.get("author", {}).get("login", "")).lower() != "github-actions[bot]" and any(word in str(c.get("body", "")).lower() for word in ("review", "address", "updated", "fixed")) for c in comments)
        if not learner_response:
            errors.append("Respond to the automated training review comment in the PR after updating the branch.")


def validate_module10(unit: str, errors: list[str]) -> None:
    files = [
        "exercise/README-sample.md", "exercise/CONTRIBUTING.md", "exercise/CODEOWNERS",
        "exercise/ISSUE_TEMPLATE/feature.yml", "exercise/PULL_REQUEST_TEMPLATE.md",
        "exercise/discoverability-plan.md", "exercise/access-visibility-matrix.md", "exercise/success-metrics.md",
    ]
    texts: dict[str, str] = {}
    for rel in files:
        require_changed(unit, rel, errors)
        texts[rel] = require_no_todo(rel, errors).lower()
    requirements = {
        "exercise/README-sample.md": ("purpose", "setup", "support", "contribut"),
        "exercise/CONTRIBUTING.md": ("branch", "pull request", "test", "review"),
        "exercise/CODEOWNERS": ("@",),
        "exercise/ISSUE_TEMPLATE/feature.yml": ("textarea", "label", "description"),
        "exercise/PULL_REQUEST_TEMPLATE.md": ("validation", "review"),
        "exercise/discoverability-plan.md": ("topic", "readme", "description", "support"),
        "exercise/access-visibility-matrix.md": ("read", "write", "maintain", "admin", "least privilege"),
        "exercise/success-metrics.md": ("contribut", "response", "reuse", "onboarding"),
    }
    for rel, terms in requirements.items():
        for term in terms:
            if term not in texts.get(rel, ""):
                errors.append(f"{rel} must address `{term}`.")


def validate_module11(unit: str, errors: list[str]) -> None:
    for rel in ["SECURITY.md", ".gitignore", ".github/dependabot.yml", ".github/CODEOWNERS"]:
        require_changed(unit, rel, errors)
    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8").lower() if (ROOT / "SECURITY.md").exists() else ""
    if len(security.strip()) < 200 or "vulnerab" not in security or not any(x in security for x in ("report", "contact", "disclos")):
        errors.append("SECURITY.md needs a meaningful responsible vulnerability-disclosure process.")
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8").lower() if (ROOT / ".gitignore").exists() else ""
    if "local-secret" not in ignore:
        errors.append(".gitignore must protect the local-secret training path.")
    dependabot = (ROOT / ".github/dependabot.yml").read_text(encoding="utf-8").lower() if (ROOT / ".github/dependabot.yml").exists() else ""
    for token in ("npm", "directory", "schedule", "weekly"):
        if token not in dependabot:
            errors.append(f"dependabot.yml must include {token} for the supplied package fixture.")
    owners = (ROOT / ".github/CODEOWNERS").read_text(encoding="utf-8") if (ROOT / ".github/CODEOWNERS").exists() else ""
    if "/exercise/sensitive/" not in owners or "@" not in owners:
        errors.append("CODEOWNERS must assign /exercise/sensitive/ to an @owner/team.")
    if not (ROOT / "package.json").exists():
        errors.append("The supplied package manifest is missing from the temporary exercise.")
    require_reflection({
        "pull-request rule": ("pull request", "pr"),
        "required checks": ("check", "status"),
        "review": ("review", "approval"),
        "secret revocation/rotation": ("revoke", "rotate", "rotation"),
        "history handling": ("history", "rewrite", "remove sensitive"),
    }, errors, 160)


def validate_module14(unit: str, errors: list[str]) -> None:
    require_changed(unit, "exercise/review_fixture.py", errors)
    require_changed(unit, "exercise/test_review_fixture.py", errors)
    if learner_commit_count(unit) < 2:
        errors.append("The PR review exercise requires multiple learner commits, including an update after review.")
    result = subprocess.run([sys.executable, "test_review_fixture.py"], cwd=ROOT / "exercise", text=True, capture_output=True)
    if result.returncode != 0:
        errors.append("The review fixture tests are not passing.")
    pr = merged_pr_for_unit(unit)
    if os.environ.get("GITHUB_ACTIONS") and not pr:
        errors.append(f"Merge the reviewed PR from lab/{unit} into sandbox/{unit}.")
        return
    if pr:
        comments = pr.get("comments", [])
        if not any(f"gh900-draft-seen:{unit}" in str(c.get("body", "")) for c in comments):
            errors.append("Open/convert the training PR as a draft so the course can record the draft stage.")
        if not any(f"gh900-ready-seen:{unit}" in str(c.get("body", "")) for c in comments):
            errors.append("Mark the draft PR Ready for review before merging.")
        repo = os.environ.get("GITHUB_REPOSITORY", "")
        inline = gh_api_json(f"repos/{repo}/pulls/{pr['number']}/comments") if repo else []
        if not isinstance(inline, list) or not any(str(c.get("user", {}).get("type", "")) != "Bot" and str(c.get("body", "")).strip() for c in inline):
            errors.append("Add at least one inline review comment on the Pull Request diff.")
    require_reflection({
        "merge commit": ("merge commit",), "squash": ("squash",), "rebase": ("rebase",),
        "history implication": ("history", "commit", "linear"),
    }, errors, 120)


def validate_module15(unit: str, errors: list[str]) -> None:
    if not os.environ.get("GITHUB_ACTIONS"):
        return
    issue = find_issue_by_title(f"[GH-900 {unit}] History regression")
    prs = gh_json(["pr", "list", "--state", "merged", "--limit", "100", "--json", "number,title,commits,mergeCommit"])
    pr = next((p for p in prs if f"[GH-900 {unit}] History fixture PR" in str(p.get("title", ""))), None) if isinstance(prs, list) else None
    if not issue:
        errors.append("The temporary Module 15 regression Issue is missing.")
        return
    if not pr:
        errors.append("The prepared Module 15 historical Pull Request is missing.")
        return
    labels = {str(x.get("name", "")) for x in issue.get("labels", [])}
    if "gh900-history" not in labels:
        errors.append("Apply the prepared `gh900-history` label to the regression Issue.")
    milestone = issue.get("milestone") or {}
    if str(milestone.get("title", "")) != f"GH-900 {unit}":
        errors.append(f"Apply milestone `GH-900 {unit}` to the regression Issue.")
    if not issue.get("assignees"):
        errors.append("Assign the regression Issue to yourself.")
    commits = pr.get("commits", [])
    commit_ids = [str(c.get("oid", "")) for c in commits if c.get("oid")]
    if not commit_ids:
        errors.append("Historical PR commit metadata is unavailable.")
        return
    target_commit = commit_ids[-1]
    crosslinked = any(f"#{pr['number']}" in str(c.get("body", "")) and "@" in str(c.get("body", "")) and target_commit[:7] in str(c.get("body", "")) for c in issue.get("comments", []))
    if not crosslinked:
        errors.append("Add an Issue comment connecting an @mention, the historical PR number, and the relevant commit SHA.")
    investigations = course_comment_bodies("/investigation ")
    if not investigations:
        errors.append("Submit `/investigation issue=#N pr=#N commit=<sha> explanation=<...>` in the course Issue.")
        return
    text = investigations[-1]
    if f"#{issue['number']}" not in text or f"#{pr['number']}" not in text:
        errors.append("The latest /investigation must name the prepared Issue and PR numbers.")
    if target_commit[:7].lower() not in text.lower():
        errors.append("The latest /investigation must identify the commit that introduced the regression marker.")
    if "explanation=" not in text.lower() or len(text) < 120:
        errors.append("The /investigation response needs a reasoned explanation of the connected history.")


def validate_module16(unit: str, errors: list[str]) -> None:
    require_changed(unit, "exercise/app.py", errors)
    require_changed(unit, "exercise/test_app.py", errors)
    app = (ROOT / "exercise/app.py").read_text(encoding="utf-8") if (ROOT / "exercise/app.py").exists() else ""
    tests = (ROOT / "exercise/test_app.py").read_text(encoding="utf-8") if (ROOT / "exercise/test_app.py").exists() else ""
    for label, pattern in {
        "FastAPI application": r"\bFastAPI\b", "Pydantic model": r"\bBaseModel\b", "text field": r"text\s*:\s*str",
        "POST /analyze-text endpoint": r"@\w+\.post\(\s*['\"]/?analyze-text['\"]",
        "input length": r"\blen\(", "deterministic hash/checksum": r"hashlib|sha(1|256|512)|checksum|digest",
        "empty-input validation": r"strip\(|ValueError|HTTPException|status_code",
    }.items():
        if not re.search(pattern, app, flags=re.IGNORECASE):
            errors.append(f"Python API implementation is missing: {label}.")
    if "test" not in tests.lower() or "analyze-text" not in tests:
        errors.append("Add tests that exercise the /analyze-text endpoint and validation behavior.")
    if "NotImplementedError" in app:
        errors.append("Complete the FastAPI implementation.")
    require_reflection({
        "Copilot/fallback": ("copilot", "fallback", "unavailable"),
        "prompt iteration": ("prompt", "iteration", "refine"),
        "rejected/modified suggestion": ("reject", "modified", "changed"),
        "verification": ("test", "/docs", "http", "verify"),
    }, errors, 140)


def validate(unit: str) -> list[str]:
    module = int(unit[1:3])
    errors: list[str] = []
    validators = {
        1: validate_module1, 2: validate_module2, 4: validate_module4, 5: validate_module5,
        6: validate_module6, 8: validate_module8, 9: validate_module9, 10: validate_module10,
        11: validate_module11, 14: validate_module14, 15: validate_module15, 16: validate_module16,
    }
    validator = validators.get(module)
    if validator:
        validator(unit, errors)
    else:
        errors.append(f"No direct validator is defined for activity module {module}.")
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
