#!/usr/bin/env python3
"""Validate structured GitHub administration/project scenarios.

The learner supplies explicit decisions instead of an essay that can pass by keyword
stuffing. Validators check required fields and a few relationships between decisions.
"""
from __future__ import annotations

import argparse
import shlex


def fields(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for token in shlex.split(text):
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        result[key.strip().lower()] = value.strip().lower()
    return result


def require(data: dict[str, str], names: tuple[str, ...]) -> list[str]:
    return [f"Missing `{name}=...`." for name in names if not data.get(name)]


def m03(data: dict[str, str]) -> list[str]:
    errors = require(data, ("usage", "cost", "dimension", "decision"))
    if data.get("usage") == data.get("cost") and data.get("usage"):
        errors.append("`usage` and `cost` must describe different report concepts.")
    if data.get("dimension") not in {"product", "sku", "repository", "organization", "period", "date", "runner"}:
        errors.append("Choose a useful report `dimension` such as product, SKU, repository, organization, period, date, or runner.")
    if len(data.get("decision", "")) < 12:
        errors.append("`decision` must state what you would verify/do before a billing decision; use hyphens instead of spaces if needed.")
    return errors


def m07(data: dict[str, str]) -> list[str]:
    errors = require(data, ("trigger", "field", "insight", "reason"))
    if data.get("field") not in {"status", "priority", "iteration", "assignee", "date"}:
        errors.append("Choose a concrete Project `field`, for example status, priority, iteration, assignee, or date.")
    if data.get("insight") not in {"chart", "view", "burnup", "status", "progress", "iteration"}:
        errors.append("Choose a concrete Project `insight`, for example chart, view, burnup, status, progress, or iteration.")
    if len(data.get("reason", "")) < 12:
        errors.append("`reason` must connect the automation trigger to the progress signal.")
    return errors


def m12(data: dict[str, str]) -> list[str]:
    errors = require(data, ("scope", "role", "least_privilege", "reason"))
    if data.get("scope") not in {"repository", "organization", "enterprise"}:
        errors.append("`scope` must be repository, organization, or enterprise.")
    if data.get("least_privilege") not in {"yes", "enforced", "limited", "minimum"}:
        errors.append("Show least privilege with `least_privilege=yes|enforced|limited|minimum`.")
    if len(data.get("role", "")) < 3:
        errors.append("Choose a specific `role` or permission level.")
    if len(data.get("reason", "")) < 12:
        errors.append("`reason` must explain why that scope/role is the minimum appropriate access.")
    return errors


def m13(data: dict[str, str]) -> list[str]:
    errors = require(data, ("idp", "team", "sync", "auth", "provisioning"))
    if data.get("sync") not in {"team-sync", "teamsync", "group-to-team"}:
        errors.append("Use `sync=team-sync` (or group-to-team) for IdP-group to GitHub-team membership.")
    if data.get("auth") not in {"saml", "sso", "saml-sso"}:
        errors.append("Use `auth=saml|sso|saml-sso` for authentication/federation in this scenario.")
    if data.get("provisioning") != "scim":
        errors.append("Use `provisioning=scim` for automated identity lifecycle provisioning/deprovisioning.")
    if len(data.get("idp", "")) < 2 or len(data.get("team", "")) < 2:
        errors.append("Name the IdP/group context and the GitHub team being synchronized.")
    return errors


VALIDATORS = {
    "m03-u07": m03,
    "m07-u06": m07,
    "m12-u05": m12,
    "m13-u05": m13,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", required=True)
    parser.add_argument("--response", required=True)
    args = parser.parse_args()
    validator = VALIDATORS.get(args.unit)
    if not validator:
        print(f"No scenario validator for {args.unit}")
        return 2
    errors = validator(fields(args.response))
    if errors:
        print("Scenario response needs correction:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Scenario response passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
