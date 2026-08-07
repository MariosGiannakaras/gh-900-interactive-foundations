#!/usr/bin/env python3
"""Validate structured GitHub administration/project scenarios.

The learner supplies explicit decisions instead of an essay that can pass by keyword
stuffing. Validators check required fields, bounded vocabularies, and relationships
between decisions so syntactically valid but nonsensical answers do not pass.
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
    usage = data.get("usage", "")
    cost = data.get("cost", "")
    usage_values = {
        "runner-minutes", "actions-minutes", "codespaces-hours", "storage",
        "packages-storage", "copilot-seats", "seat-count",
    }
    cost_values = {
        "billed-amount", "estimated-cost", "spend", "budget-impact",
        "overage", "included-allowance",
    }
    if usage and usage not in usage_values:
        errors.append("Choose a measurable `usage` value such as runner-minutes, actions-minutes, codespaces-hours, storage, packages-storage, copilot-seats, or seat-count.")
    if cost and cost not in cost_values:
        errors.append("Choose a billing `cost` concept such as billed-amount, estimated-cost, spend, budget-impact, overage, or included-allowance.")
    if usage == cost and usage:
        errors.append("`usage` and `cost` must describe different report concepts.")
    if data.get("dimension") not in {"product", "sku", "repository", "organization", "period", "date", "runner"}:
        errors.append("Choose a useful report `dimension` such as product, SKU, repository, organization, period, date, or runner.")
    if len(data.get("decision", "")) < 12:
        errors.append("`decision` must state what you would verify/do before a billing decision; use hyphens instead of spaces if needed.")
    return errors


def m07(data: dict[str, str]) -> list[str]:
    errors = require(data, ("trigger", "field", "insight", "reason"))
    trigger = data.get("trigger", "")
    field = data.get("field", "")
    valid_triggers = {
        "status-change", "iteration-change", "assignee-change", "date-change",
        "item-added", "issue-closed", "pr-merged", "pull-request-merged",
    }
    if trigger and trigger not in valid_triggers:
        errors.append("Choose a concrete automation `trigger`, for example status-change, iteration-change, assignee-change, date-change, item-added, issue-closed, or pull-request-merged.")
    if field not in {"status", "priority", "iteration", "assignee", "date"}:
        errors.append("Choose a concrete Project `field`, for example status, priority, iteration, assignee, or date.")
    if data.get("insight") not in {"chart", "view", "burnup", "status", "progress", "iteration"}:
        errors.append("Choose a concrete Project `insight`, for example chart, view, burnup, status, progress, or iteration.")
    required_field = {
        "status-change": "status",
        "iteration-change": "iteration",
        "assignee-change": "assignee",
        "date-change": "date",
    }.get(trigger)
    if required_field and field and field != required_field:
        errors.append(f"`trigger={trigger}` must be paired with `field={required_field}`.")
    if trigger in {"issue-closed", "pr-merged", "pull-request-merged"} and field and field not in {"status", "date"}:
        errors.append(f"`trigger={trigger}` should update or analyze a status/date field, not `{field}`.")
    if len(data.get("reason", "")) < 12:
        errors.append("`reason` must connect the automation trigger to the progress signal.")
    return errors


def m12(data: dict[str, str]) -> list[str]:
    errors = require(data, ("scope", "role", "least_privilege", "reason"))
    scope = data.get("scope", "")
    role = data.get("role", "")
    valid_scopes = {"repository", "organization", "enterprise"}
    repository_roles = {"read", "triage", "write", "maintain", "admin"}
    organization_roles = {"member", "owner", "billing-manager", "security-manager"}
    enterprise_roles = {"enterprise-owner", "billing-manager", "security-manager"}
    valid_roles = repository_roles | organization_roles | enterprise_roles

    if scope not in valid_scopes:
        errors.append("`scope` must be repository, organization, or enterprise.")
    if role and role not in valid_roles:
        errors.append("Choose a recognized GitHub `role` or permission: read, triage, write, maintain, admin, member, owner, billing-manager, security-manager, or enterprise-owner.")
    if scope == "repository" and role and role not in repository_roles:
        errors.append(f"`role={role}` is not a repository permission level.")
    if scope == "organization" and role and role not in organization_roles:
        errors.append(f"`role={role}` is not an organization-level role for this scenario.")
    if scope == "enterprise" and role and role not in enterprise_roles:
        errors.append(f"`role={role}` is not an enterprise-level role for this scenario.")
    if data.get("least_privilege") not in {"yes", "enforced", "limited", "minimum"}:
        errors.append("Show least privilege with `least_privilege=yes|enforced|limited|minimum`.")
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
    if data.get("idp") and data.get("team") and data["idp"] == data["team"]:
        errors.append("`idp` and `team` represent different identity layers and should not be the same value.")
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
