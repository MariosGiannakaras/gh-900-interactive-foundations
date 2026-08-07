#!/usr/bin/env python3
"""Hardened entrypoint for GH-900 hands-on validation.

The large module-specific implementation lives in validate_activity_core.py. This
entrypoint adds cross-cutting checks for complete Issue-comment pagination, unit-scoped
learner evidence, race-safe/durable merged-PR lookup, and direct behavior validation
of generated Python exercises while preserving the core module logic.
"""
from __future__ import annotations

import argparse
import json
import os
import py_compile
import subprocess
import sys
from pathlib import Path

import runtime_protocol
import validate_activity_core as core

ROOT = Path(__file__).resolve().parents[1]
CURRENT_UNIT = ""


def _course_comments() -> list[dict[str, object]]:
    """Read the complete course transcript across all REST pages."""
    if not os.environ.get("GITHUB_ACTIONS"):
        return []
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo:
        return []
    rows = core.gh_json(["issue", "list", "--state", "all", "--limit", "100", "--json", "number,title"])
    if not isinstance(rows, list):
        return []
    hit = next((row for row in rows if row.get("title") == core.COURSE_TITLE), None)
    if not hit:
        return []

    comments: list[dict[str, object]] = []
    page = 1
    while True:
        result = subprocess.run(
            [
                "gh", "api",
                f"repos/{repo}/issues/{hit['number']}/comments?per_page=100&page={page}",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=60,
        )
        if result.returncode != 0:
            return comments
        try:
            page_rows = json.loads(result.stdout)
        except json.JSONDecodeError:
            return comments
        if not isinstance(page_rows, list) or not page_rows:
            break
        comments.extend(row for row in page_rows if isinstance(row, dict))
        if len(page_rows) < 100:
            break
        page += 1
    return comments


def course_comment_bodies(prefix: str) -> list[str]:
    """Return only responses submitted while CURRENT_UNIT was the visible lesson."""
    if not CURRENT_UNIT:
        return []
    return runtime_protocol.bodies_for_unit(_course_comments(), prefix, CURRENT_UNIT)


def _normalize_rest_pr(row: dict[str, object]) -> dict[str, object]:
    """Convert GitHub REST PR fields to the shape used by existing validators."""
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    number = int(row.get("number", 0) or 0)
    comments_raw = core.gh_api_json(f"repos/{repo}/issues/{number}/comments?per_page=100") if repo and number else []
    commits_raw = core.gh_api_json(f"repos/{repo}/pulls/{number}/commits?per_page=100") if repo and number else []

    comments: list[dict[str, object]] = []
    if isinstance(comments_raw, list):
        for comment in comments_raw:
            if not isinstance(comment, dict):
                continue
            user = comment.get("user") if isinstance(comment.get("user"), dict) else {}
            comments.append(
                {
                    "body": str(comment.get("body", "")),
                    "author": {"login": str(user.get("login", ""))},
                }
            )

    commits: list[dict[str, object]] = []
    if isinstance(commits_raw, list):
        for commit in commits_raw:
            if isinstance(commit, dict) and commit.get("sha"):
                commits.append({"oid": str(commit["sha"])})

    head = row.get("head") if isinstance(row.get("head"), dict) else {}
    base = row.get("base") if isinstance(row.get("base"), dict) else {}
    merge_sha = str(row.get("merge_commit_sha", "") or "")
    return {
        "number": number,
        "title": str(row.get("title", "")),
        "state": "MERGED" if row.get("merged_at") else str(row.get("state", "")).upper(),
        "mergedAt": row.get("merged_at"),
        "headRefName": str(head.get("ref", "")),
        "baseRefName": str(base.get("ref", "")),
        "body": str(row.get("body", "") or ""),
        "comments": comments,
        "commits": commits,
        "mergeCommit": {"oid": merge_sha} if merge_sha else None,
    }


def _rest_merged_pr_for_unit(unit: str) -> dict[str, object] | None:
    """Use the repository REST PR record as durable evidence for manual recovery."""
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo or not os.environ.get("GITHUB_ACTIONS"):
        return None
    rows = core.gh_api_json(f"repos/{repo}/pulls?state=closed&per_page=100")
    if not isinstance(rows, list):
        return None
    head = f"lab/{unit}"
    base = f"sandbox/{unit}"
    for row in rows:
        if not isinstance(row, dict) or not row.get("merged_at"):
            continue
        row_head = row.get("head") if isinstance(row.get("head"), dict) else {}
        row_base = row.get("base") if isinstance(row.get("base"), dict) else {}
        if row_head.get("ref") == head and row_base.get("ref") == base:
            return _normalize_rest_pr(row)
    return None


def merged_pr_for_unit(unit: str) -> dict[str, object] | None:
    """Resolve a merged training PR without relying on one eventually-consistent view.

    During ``pull_request.closed`` the exact event PR is authoritative. For `/check`
    and later events, the repository REST pull-request record is the durable fallback.
    The legacy merged-list lookup remains only as a final compatibility fallback.
    """
    head = f"lab/{unit}"
    base = f"sandbox/{unit}"
    pr_number = os.environ.get("PR_NUMBER", "").strip()

    if pr_number:
        data = core.gh_json(
            [
                "pr", "view", pr_number,
                "--json",
                "number,title,state,mergedAt,headRefName,baseRefName,body,comments,commits,mergeCommit",
            ]
        )
        if (
            isinstance(data, dict)
            and data.get("headRefName") == head
            and data.get("baseRefName") == base
            and (data.get("mergedAt") or str(data.get("state", "")).upper() == "MERGED")
        ):
            return data

    durable = _rest_merged_pr_for_unit(unit)
    if durable:
        return durable
    return core._merged_pr_for_unit_original(unit)


def _run_python(code: str, cwd: Path) -> tuple[bool, str]:
    if not cwd.exists():
        return False, f"Exercise directory is missing: {cwd.relative_to(ROOT)}"
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
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
core._merged_pr_for_unit_original = core.merged_pr_for_unit
core._validate_module5_original = core.validate_module5
core._validate_module8_original = core.validate_module8
core._validate_module14_original = core.validate_module14
core._validate_module16_original = core.validate_module16
core.course_comment_bodies = course_comment_bodies
core.merged_pr_for_unit = merged_pr_for_unit
core.validate_module5 = validate_module5
core.validate_module8 = validate_module8
core.validate_module14 = validate_module14
core.validate_module16 = validate_module16


def main() -> int:
    global CURRENT_UNIT
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", required=True)
    args = parser.parse_args()
    CURRENT_UNIT = args.unit
    errors = core.validate(args.unit)
    if errors:
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print(f"{args.unit} hands-on checkpoint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
