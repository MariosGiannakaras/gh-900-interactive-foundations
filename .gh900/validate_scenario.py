#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re

RULES = {
    "m03-u07": [
        ("usage/quantity", ("usage", "quantity", "consumption")),
        ("cost/charge", ("cost", "charge", "billing", "price")),
        ("report dimension", ("product", "service", "date", "period", "sku")),
    ],
    "m07-u06": [
        ("automation", ("automation", "workflow", "trigger")),
        ("project field/status", ("field", "status", "iteration")),
        ("insight", ("insight", "chart", "view", "progress")),
    ],
    "m12-u05": [
        ("scope", ("repository", "organization", "enterprise")),
        ("permission/role", ("permission", "role", "access")),
        ("least privilege/governance", ("least privilege", "policy", "governance")),
    ],
    "m13-u05": [
        ("identity provider/group", ("identity provider", "idp", "group")),
        ("GitHub team", ("team",)),
        ("synchronization", ("sync", "synchronization", "synchronise", "synchronize")),
        ("auth distinction", ("authentication", "authorization", "saml", "scim")),
    ],
}

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--unit", required=True)
    p.add_argument("--response", required=True)
    args = p.parse_args()
    rules = RULES.get(args.unit)
    if not rules:
        print(f"No scenario validator for {args.unit}")
        return 2

    text = re.sub(r"\s+", " ", args.response.strip().lower())
    if len(text) < 120:
        print("Response is too short. Explain the decision and reasoning, not only keywords.")
        return 1

    missing = []
    for label, alternatives in rules:
        if not any(term in text for term in alternatives):
            missing.append(label)
    if missing:
        print("Needs more detail: " + ", ".join(missing))
        return 1
    print("Scenario response passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
