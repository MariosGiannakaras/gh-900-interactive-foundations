#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PUBLIC_FILES = [
    "README.md",
    "LICENSE",
    ".github/CONTRIBUTING.md",
    ".github/CODE_OF_CONDUCT.md",
    ".github/SECURITY.md",
    "docs/ARCHITECTURE.md",
    "docs/MAINTAINING.md",
]

# These are intentional learner deliverables. Seeding them in the template would
# pre-complete part of Module 11, so the maintained source must leave them absent.
LEARNER_OWNED_BASELINE_ARTIFACTS = [
    "SECURITY.md",
    ".github/CODEOWNERS",
]

PINNED_ACTION = re.compile(r"(?m)^\s*uses:\s*([^\s#]+)")
FULL_SHA_REF = re.compile(r"^[^@\s]+@[0-9a-fA-F]{40}$")


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_PUBLIC_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"required public-repository file missing: {rel}")

    for rel in LEARNER_OWNED_BASELINE_ARTIFACTS:
        if (ROOT / rel).exists():
            errors.append(f"template baseline must not pre-create learner-owned artifact: {rel}")

    readme_path = ROOT / "README.md"
    if readme_path.exists():
        readme = readme_path.read_text(encoding="utf-8")
        for required in [
            "Copy Exercise",
            "16 / 16",
            "106 / 106",
            "## Security model",
            "## Contributing",
            "## License and attribution",
            "docs/ARCHITECTURE.md",
            "docs/MAINTAINING.md",
        ]:
            if required not in readme:
                errors.append(f"README public-facing contract missing: {required}")

    workflows = sorted((ROOT / ".github" / "workflows").glob("*.y*ml"))
    if not workflows:
        errors.append("no GitHub Actions workflows found")

    for path in workflows:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if "pull_request_target" in text:
            errors.append(f"{rel} must not use privileged pull_request_target")
        if not re.search(r"(?m)^permissions:\s*$", text):
            errors.append(f"{rel} must declare explicit GITHUB_TOKEN permissions")
        for action_ref in PINNED_ACTION.findall(text):
            if action_ref.startswith("./"):
                continue
            if not FULL_SHA_REF.fullmatch(action_ref):
                errors.append(f"{rel} action must use a full 40-character commit SHA: {action_ref}")

    start = ROOT / ".github/workflows/00-start-course.yml"
    engine = ROOT / ".github/workflows/01-course-engine.yml"
    quality = ROOT / ".github/workflows/quality.yml"

    if start.exists() and "!github.event.repository.is_template" not in start.read_text(encoding="utf-8"):
        errors.append("Step 0 must remain disabled in the upstream template")

    if engine.exists():
        text = engine.read_text(encoding="utf-8")
        for required in [
            "!github.event.repository.is_template",
            "github.event.pull_request.author_association",
            "github.event.comment.author_association",
            "github.event.comment.user.type",
            "timeout-minutes:",
        ]:
            if required not in text:
                errors.append(f"course engine hardening requirement missing: {required}")

    if quality.exists():
        text = quality.read_text(encoding="utf-8")
        for required in [
            "if: github.event.repository.is_template",
            "cancel-in-progress: true",
            "scripts/audit_public_repository.py",
            "timeout-minutes:",
        ]:
            if required not in text:
                errors.append(f"source quality hardening requirement missing: {required}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Public repository audit passed.")
    print(f"Community/security files: {len(REQUIRED_PUBLIC_FILES)}/{len(REQUIRED_PUBLIC_FILES)}")
    print("External Actions: immutable full-SHA references only")
    print("Template baseline: learner-owned Module 11 artifacts remain unseeded")
    print("Runtime isolation: source quality and learner course jobs are separated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
