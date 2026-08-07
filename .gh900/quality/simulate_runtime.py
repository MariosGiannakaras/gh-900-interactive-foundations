#!/usr/bin/env python3
"""Deterministic simulation of the complete 106-unit course state/protocol.

This does not claim to replace a GitHub-hosted learner E2E. It exhaustively exercises
all local states, modes, render markers, transitions, branch contracts, stale-response
scoping, structured scenario validators, and entitlement-aware setup checkpoints.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GH900 = ROOT / ".gh900"
sys.path.insert(0, str(GH900))

import course_unit_state as state  # noqa: E402
import runtime_protocol  # noqa: E402


def run_validator(script: str, *args: str) -> int:
    return subprocess.run(
        [sys.executable, str(GH900 / script), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=10,
    ).returncode


def main() -> int:
    units = state.load_units()
    errors: list[str] = []
    if len(units) != 106:
        errors.append(f"Expected 106 units, found {len(units)}")

    # Walk the exact transition chain from first to final state.
    cursor = units[0]
    visited: list[str] = []
    while cursor:
        visited.append(cursor.id)
        nxt = state.next_unit(cursor.id)
        cursor = nxt
    expected = [u.id for u in units]
    if visited != expected:
        errors.append("next_unit() does not traverse the 106-unit manifest exactly once in order")

    for ordinal, unit in enumerate(units, start=1):
        if unit.ordinal != ordinal:
            errors.append(f"{unit.id}: ordinal {unit.ordinal} != {ordinal}")
        rendered = state.render(unit)
        marker = runtime_protocol.lesson_marker(unit.id)
        if not rendered.startswith(marker):
            errors.append(f"{unit.id}: rendering does not start with the stable lesson marker")
        if f"**{unit.ordinal} / 106**" not in rendered:
            errors.append(f"{unit.id}: global progress is missing")
        if unit.mode == "activity":
            if unit.branch != f"lab/{unit.id}" or unit.sandbox != f"sandbox/{unit.id}":
                errors.append(f"{unit.id}: activity branch/sandbox contract is invalid")
            if "Hands-on checklist" not in rendered:
                errors.append(f"{unit.id}: activity checklist is missing")
        else:
            if unit.branch is not None or unit.sandbox is not None:
                errors.append(f"{unit.id}: non-activity unit unexpectedly owns exercise branches")
        if unit.mode in {"read", "summary"} and "/next" not in rendered:
            errors.append(f"{unit.id}: reading/summary continuation is missing /next")
        if unit.mode == "assessment" and "/answer" not in rendered:
            errors.append(f"{unit.id}: assessment continuation is missing /answer")
        if unit.mode == "scenario" and "/scenario" not in rendered:
            errors.append(f"{unit.id}: scenario continuation is missing /scenario")
        if unit.mode == "checkpoint" and "/checkpoint" not in rendered:
            errors.append(f"{unit.id}: checkpoint continuation is missing /checkpoint")

    # Every official unit whose title says Exercise must be interactive, never a read unit.
    for unit in units:
        if "exercise" in unit.title.lower() and unit.mode == "read":
            errors.append(f"{unit.id}: official exercise was downgraded to read mode")
    if state.find("m16-u03").mode != "checkpoint":
        errors.append("m16-u03 must be an account-aware checkpoint")

    # Simulate duplicate/stale comments and unit-scoped evidence.
    comments = [
        {"id": 10, "body": runtime_protocol.lesson_marker("m01-u01") + "\nlesson"},
        {"id": 11, "body": "/next"},
        {"id": 12, "body": runtime_protocol.lesson_marker("m01-u02") + "\nlesson"},
        {"id": 13, "body": "/next"},
        {"id": 14, "body": "/reflection old evidence"},
        {"id": 15, "body": runtime_protocol.lesson_marker("m04-u05") + "\nlesson"},
        {"id": 16, "body": "/reflection default advanced SARIF Security workflow observation"},
        {"id": 17, "body": "acknowledgement without marker"},
        {"id": 18, "body": "/check"},
    ]
    if runtime_protocol.response_matches_unit(comments, 13, "m01-u01"):
        errors.append("stale duplicate command incorrectly matches a previous unit")
    if not runtime_protocol.response_matches_unit(comments, 13, "m01-u02"):
        errors.append("current-unit command association failed")
    scoped = runtime_protocol.bodies_for_unit(comments, "/reflection ", "m04-u05")
    if scoped != ["/reflection default advanced SARIF Security workflow observation"]:
        errors.append("unit-scoped reflection selection is incorrect")

    # Structured scenarios must accept a coherent decision and reject keyword essays.
    valid_scenarios = {
        "m03-u07": "usage=runner-minutes cost=billed-amount dimension=repository decision=verify-budget-and-allowance",
        "m07-u06": "trigger=status-change field=status insight=chart reason=show-progress-after-status-change",
        "m12-u05": "scope=organization role=maintain least_privilege=yes reason=limit-access-to-required-org-scope",
        "m13-u05": "idp=entra-engineering team=platform sync=team-sync auth=saml provisioning=scim",
    }
    for uid, response in valid_scenarios.items():
        if run_validator("validate_scenario.py", "--unit", uid, "--response", response) != 0:
            errors.append(f"{uid}: valid structured scenario did not pass")
        if run_validator("validate_scenario.py", "--unit", uid, "--response", "authentication authorization policy team usage cost " * 20) == 0:
            errors.append(f"{uid}: unstructured keyword stuffing unexpectedly passed")

    available = "access=available editor=vscode signin=confirmed interface=both suggestion=reviewed python=ready copilot=located"
    unavailable = "access=unavailable editor=vscode signin=understood interface=understood suggestion=understood python=understood official=reviewed fallback=completed"
    for response in (available, unavailable):
        if run_validator("validate_checkpoint.py", "--unit", "m16-u03", "--response", response) != 0:
            errors.append("m16-u03: valid account-aware checkpoint did not pass")
    if run_validator("validate_checkpoint.py", "--unit", "m16-u03", "--response", "access=unavailable") == 0:
        errors.append("m16-u03: incomplete checkpoint unexpectedly passed")

    print(f"Runtime states simulated: {len(visited)}/106")
    print(f"Interactive official exercises checked: {sum('exercise' in u.title.lower() for u in units)}")
    if errors:
        print("Runtime simulation failures:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("106-unit runtime protocol simulation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
