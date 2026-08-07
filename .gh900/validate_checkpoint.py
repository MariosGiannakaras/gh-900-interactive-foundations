#!/usr/bin/env python3
"""Validate structured external/account-aware checkpoints without pretending UI telemetry exists."""
from __future__ import annotations

import argparse
import re
import shlex


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for token in shlex.split(text):
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        fields[key.strip().lower()] = value.strip().lower()
    return fields


def validate_m16_u03(response: str) -> list[str]:
    fields = parse_fields(response)
    errors: list[str] = []
    access = fields.get("access", "")
    if access not in {"available", "unavailable"}:
        errors.append("Set `access=available` or `access=unavailable`.")

    editor = fields.get("editor", "")
    if editor not in {"vscode", "codespace", "codespaces"}:
        errors.append("Set `editor=vscode` or `editor=codespace`.")

    if fields.get("signin") not in {"confirmed", "understood"}:
        errors.append("Set `signin=confirmed` after checking sign-in, or `signin=understood` on the fallback path.")

    if fields.get("interface") not in {"chat", "inline", "both", "located", "understood"}:
        errors.append("Record the Copilot surface with `interface=chat|inline|both|located|understood`.")

    if fields.get("suggestion") not in {"reviewed", "rejected", "cycled", "understood"}:
        errors.append("Record suggestion review with `suggestion=reviewed|rejected|cycled|understood`.")

    if fields.get("python") not in {"ready", "verified", "understood"}:
        errors.append("Record the Python environment with `python=ready|verified|understood`.")

    if access == "available":
        if fields.get("copilot") not in {"located", "enabled", "ready"}:
            errors.append("With Copilot available, record `copilot=located|enabled|ready`.")
    elif access == "unavailable":
        if fields.get("official") not in {"opened", "reviewed"}:
            errors.append("Without Copilot access, review the official exercise and record `official=opened|reviewed`.")
        fallback = fields.get("fallback", "")
        if fallback not in {"reviewed", "completed", "understood"}:
            errors.append("Complete the guided fallback and record `fallback=reviewed|completed|understood`.")

    note = fields.get("note", "")
    if note and not re.fullmatch(r"[a-z0-9._/-]+", note):
        errors.append("Keep optional `note=` compact; use hyphens instead of spaces.")
    return errors


VALIDATORS = {"m16-u03": validate_m16_u03}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", required=True)
    parser.add_argument("--response", required=True)
    args = parser.parse_args()
    validator = VALIDATORS.get(args.unit)
    if not validator:
        print(f"No checkpoint validator for {args.unit}")
        return 2
    errors = validator(args.response)
    if errors:
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{args.unit} setup checkpoint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
