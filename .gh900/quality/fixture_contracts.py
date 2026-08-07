#!/usr/bin/env python3
"""Verify on-demand workspace, assessment, and runtime resilience contracts."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GH900 = ROOT / ".gh900"
TEMPLATES = GH900 / "templates"
sys.path.insert(0, str(GH900))

import course_unit_state as state  # noqa: E402
import validate_activity as activity_validator  # noqa: E402
import validate_assessment as assessment_validator  # noqa: E402
import workspace as workspace_manager  # noqa: E402

EXPECTED_ACTIVITY_MODULES = {1, 2, 4, 5, 6, 8, 9, 10, 11, 14, 15, 16}
LEGACY_ASSESSMENT_MARKERS = (
    "ACTIVITY_STATUS",
    "REPLACE_ME",
    "EVIDENCE_",
    "Read `modules/",
    "Work on branch `lab/module-",
)


def check_merged_pr_event_lookup(errors: list[str]) -> None:
    """Closed+merged PR events must not depend on another PR index."""
    original_gh_json = activity_validator.core.gh_json
    original_gh_api_json = activity_validator.core.gh_api_json
    original_pr_number = os.environ.get("PR_NUMBER")
    original_actions = os.environ.get("GITHUB_ACTIONS")
    original_repo = os.environ.get("GITHUB_REPOSITORY")
    calls: list[list[str]] = []

    def fake_gh_json(args: list[str]) -> object | None:
        calls.append(args)
        if args[:3] == ["pr", "view", "42"]:
            return {
                "number": 42,
                "state": "MERGED",
                "mergedAt": "2026-08-07T10:04:49Z",
                "headRefName": "lab/m02-u06",
                "baseRefName": "sandbox/m02-u06",
                "body": "Closes #3",
                "comments": [],
                "commits": [],
                "mergeCommit": {"oid": "deadbeef"},
            }
        if args[:2] == ["pr", "list"]:
            return []
        return None

    try:
        os.environ["GITHUB_ACTIONS"] = "true"
        os.environ["GITHUB_REPOSITORY"] = "example/course"
        os.environ["PR_NUMBER"] = "42"
        activity_validator.core.gh_json = fake_gh_json
        activity_validator.core.gh_api_json = lambda endpoint: []
        result = activity_validator.merged_pr_for_unit("m02-u06")
        if not isinstance(result, dict) or result.get("number") != 42:
            errors.append("Merged PR closed-event lookup did not resolve the exact event PR")
        if not calls or calls[0][:3] != ["pr", "view", "42"]:
            errors.append("Merged PR lookup must query the exact event PR first")
        if any(call[:2] == ["pr", "list"] for call in calls):
            errors.append("Merged PR lookup unnecessarily fell back after an exact event match")
    finally:
        activity_validator.core.gh_json = original_gh_json
        activity_validator.core.gh_api_json = original_gh_api_json
        if original_pr_number is None:
            os.environ.pop("PR_NUMBER", None)
        else:
            os.environ["PR_NUMBER"] = original_pr_number
        if original_actions is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = original_actions
        if original_repo is None:
            os.environ.pop("GITHUB_REPOSITORY", None)
        else:
            os.environ["GITHUB_REPOSITORY"] = original_repo


def check_merged_pr_recovery_lookup(errors: list[str]) -> None:
    """Manual /check recovery must accept durable REST merged-PR evidence."""
    original_gh_json = activity_validator.core.gh_json
    original_gh_api_json = activity_validator.core.gh_api_json
    original_pr_number = os.environ.get("PR_NUMBER")
    original_actions = os.environ.get("GITHUB_ACTIONS")
    original_repo = os.environ.get("GITHUB_REPOSITORY")
    api_calls: list[str] = []
    legacy_calls: list[list[str]] = []

    def fake_api(endpoint: str) -> object | None:
        api_calls.append(endpoint)
        if endpoint.endswith("/pulls?state=closed&per_page=100"):
            return [
                {
                    "number": 4,
                    "title": "Complete M02-U06 GitHub Flow exercise",
                    "state": "closed",
                    "merged_at": "2026-08-07T10:04:46Z",
                    "merge_commit_sha": "8fa22ce",
                    "head": {"ref": "lab/m02-u06"},
                    "base": {"ref": "sandbox/m02-u06"},
                    "body": "Closes #3",
                }
            ]
        if endpoint.endswith("/issues/4/comments?per_page=100"):
            return [{"body": "review addressed", "user": {"login": "learner"}}]
        if endpoint.endswith("/pulls/4/commits?per_page=100"):
            return [{"sha": "abc123"}]
        return None

    def fake_gh_json(args: list[str]) -> object | None:
        legacy_calls.append(args)
        return []

    try:
        os.environ["GITHUB_ACTIONS"] = "true"
        os.environ["GITHUB_REPOSITORY"] = "example/course"
        os.environ.pop("PR_NUMBER", None)
        activity_validator.core.gh_api_json = fake_api
        activity_validator.core.gh_json = fake_gh_json
        result = activity_validator.merged_pr_for_unit("m02-u06")
        if not isinstance(result, dict) or result.get("number") != 4:
            errors.append("Manual recovery did not resolve durable REST merged-PR evidence")
        if isinstance(result, dict):
            if result.get("headRefName") != "lab/m02-u06" or result.get("baseRefName") != "sandbox/m02-u06":
                errors.append("Durable REST merged-PR normalization lost head/base refs")
            comments = result.get("comments", [])
            if not isinstance(comments, list) or not comments or comments[0].get("author", {}).get("login") != "learner":
                errors.append("Durable REST merged-PR normalization lost conversation authors")
        if any(call[:2] == ["pr", "list"] for call in legacy_calls):
            errors.append("Manual recovery unnecessarily used the legacy merged PR list after a REST match")
        if not any(endpoint.endswith("/pulls?state=closed&per_page=100") for endpoint in api_calls):
            errors.append("Manual recovery did not query the durable REST pull-request endpoint")
    finally:
        activity_validator.core.gh_json = original_gh_json
        activity_validator.core.gh_api_json = original_gh_api_json
        if original_pr_number is None:
            os.environ.pop("PR_NUMBER", None)
        else:
            os.environ["PR_NUMBER"] = original_pr_number
        if original_actions is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = original_actions
        if original_repo is None:
            os.environ.pop("GITHUB_REPOSITORY", None)
        else:
            os.environ["GITHUB_REPOSITORY"] = original_repo


def check_runtime_cache_cleanup(errors: list[str]) -> None:
    """Generated learner branches must never capture interpreter bytecode."""
    cache_dir = GH900 / "__pycache__"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cached = cache_dir / "gh900-fixture.cpython-312.pyc"
    loose = GH900 / "gh900-fixture.pyc"
    cached.write_bytes(b"test-bytecode")
    loose.write_bytes(b"test-bytecode")
    try:
        workspace_manager.clean_runtime_caches()
    except Exception as exc:
        errors.append(f"Runtime cache cleanup raised unexpectedly: {exc}")
        return
    finally:
        cached.unlink(missing_ok=True)
        loose.unlink(missing_ok=True)
        if cache_dir.exists() and not any(cache_dir.iterdir()):
            cache_dir.rmdir()
    if cached.exists() or loose.exists() or cache_dir.exists():
        errors.append("workspace runtime cache cleanup left .pyc/__pycache__ artifacts behind")


def main() -> int:
    errors: list[str] = []
    workspace = (GH900 / "workspace.py").read_text(encoding="utf-8")

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

    for module in sorted(EXPECTED_ACTIVITY_MODULES):
        marker = "if module == 1:" if module == 1 else f"elif module == {module}:"
        if marker not in workspace:
            errors.append(f"workspace.py has no provisioning branch for activity Module {module}")

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
            errors.append(f"Module {module} assessment hashes do not match its {expected} question IDs")
        for question, value in module_hashes.items():
            if not re.fullmatch(r"[0-9a-f]{64}", str(value)):
                errors.append(f"Module {module} {question} has an invalid SHA-256 answer hash")
                continue
            matches = [answer for answer in "ABC" if assessment_validator.digest(module, question, answer) == value]
            if len(matches) != 1:
                errors.append(
                    f"Module {module} {question} hash must resolve to exactly one valid A/B/C answer; got {matches}"
                )

    for name in ("app.py", "test_app.py", "requirements.txt"):
        path = TEMPLATES / "labs" / "module-16" / name
        if not path.exists():
            errors.append(f"Module 16 FastAPI fixture is missing {path.relative_to(ROOT)}")

    check_merged_pr_event_lookup(errors)
    check_merged_pr_recovery_lookup(errors)
    check_runtime_cache_cleanup(errors)

    start = (ROOT / ".github" / "workflows" / "00-start-course.yml").read_text(encoding="utf-8")
    engine = (ROOT / ".github" / "workflows" / "01-course-engine.yml").read_text(encoding="utf-8")
    for marker in ("concurrency:", "gh900-start-${{ github.repository }}", "cancel-in-progress: false"):
        if marker not in start:
            errors.append(f"Step 0 startup serialization contract is missing: {marker}")
    for marker in (
        "COMMENT_ID:",
        "comment_matches_current_unit()",
        "Ignoring a stale/ambiguous course response",
        "reconcile_current_lesson()",
        "gh900-unit:${state}",
        "validate_checkpoint.py",
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
        "16 clean assessments with complete/decodable hash coverage, serialized/self-healing runtime, "
        "race-safe/durable merged-PR validation, bytecode-clean learner provisioning."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())