#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / ".gh900" / "templates"

VISIBLE_CLEANUP = [
    ROOT / "exercise",
    ROOT / ".devcontainer",
    ROOT / "SECURITY.md",
    ROOT / ".gitignore",
    ROOT / "package.json",
    ROOT / ".github" / "CODEOWNERS",
    ROOT / ".github" / "dependabot.yml",
    ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
    ROOT / ".github" / "ISSUE_TEMPLATE",
    ROOT / ".github" / "workflows" / "module-04-codeql.yml",
]


def clean_visible() -> None:
    for path in VISIBLE_CLEANUP:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists() or path.is_symlink():
            path.unlink()


def copy_template(module: int, name: str, dest: str) -> None:
    src = TEMPLATES / "labs" / f"module-{module:02d}" / name
    dst = ROOT / dest
    if not src.exists():
        raise FileNotFoundError(f"Missing internal template: {src.relative_to(ROOT)}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write(path: str, content: str) -> None:
    dst = ROOT / path
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content, encoding="utf-8")


def prepare(unit: str) -> None:
    clean_visible()
    module = int(unit[1:3])

    if module == 1:
        copy_template(1, "version-control-notes.md", "exercise/version-control-notes.md")
        copy_template(1, "diff-practice.txt", "exercise/diff-practice.txt")
        copy_template(1, "vscode-branch.txt", "exercise/vscode-branch.txt")

    elif module == 2:
        write(
            "exercise/github-flow.md",
            "# GitHub Flow guided tour\n\n"
            "TODO: make one meaningful repository change here. Use the Issue and Pull Request workflow "
            "described in the course Issue, then update this file if review feedback requires it.\n",
        )

    elif module == 4:
        copy_template(4, "code-scanning-simulation.yml", "exercise/code-scanning-simulation.yml")
        write(
            ".github/workflows/module-04-codeql.yml",
            "# Temporary training workflow: customize the TODO values as instructed in the course.\n"
            "name: Module 04 CodeQL practice\n\n"
            "on:\n"
            "  push:\n"
            "    branches: ['lab/**']\n"
            "  pull_request:\n"
            "    branches: ['sandbox/**']\n"
            "  schedule:\n"
            "    - cron: '30 5 * * 1'\n\n"
            "permissions:\n"
            "  contents: read\n"
            "  security-events: write\n\n"
            "jobs:\n"
            "  analyze:\n"
            "    runs-on: ubuntu-24.04\n"
            "    steps:\n"
            "      # TODO: describe/select the CodeQL init, analyze, and language/build strategy.\n"
            "      - run: echo 'Training-only advanced CodeQL workflow scaffold'\n",
        )
        write(
            "exercise/sample.sarif.json",
            json.dumps(
                {
                    "version": "2.1.0",
                    "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
                    "runs": [
                        {
                            "tool": {"driver": {"name": "GH-900 sample external scanner", "rules": []}},
                            "results": [],
                        }
                    ],
                },
                indent=2,
            )
            + "\n",
        )
        write(
            "exercise/codeql-notes.md",
            "# Code scanning observations\n\n"
            "TODO: compare default setup, advanced setup, and an external SARIF-producing scanner.\n\n"
            "TODO: note what you observed in the Security and Actions interfaces, or what would be expected "
            "if your account/repository policy prevents the temporary workflow from running.\n",
        )

    elif module == 5:
        write(
            "exercise/copilot-practice.py",
            '"""Small implementation target for the GitHub Copilot exercise."""\n\n'
            "def summarize_items(items: list[str]) -> str:\n"
            "    # TODO: validate input and return a deterministic, readable summary.\n"
            "    raise NotImplementedError\n",
        )
        write(
            "exercise/test_copilot_practice.py",
            "from copilot_practice import summarize_items\n\n"
            "def test_summary_is_deterministic():\n"
            "    assert summarize_items(['beta', 'alpha']) == '2 items: alpha, beta'\n\n"
            "def test_empty_input_is_rejected():\n"
            "    try:\n"
            "        summarize_items([])\n"
            "    except ValueError:\n"
            "        return\n"
            "    raise AssertionError('empty input should raise ValueError')\n",
        )

    elif module == 6:
        src = TEMPLATES / "devcontainer"
        dst = ROOT / ".devcontainer"
        if not src.exists():
            raise FileNotFoundError("Missing internal devcontainer template")
        shutil.copytree(src, dst)
        write(
            "exercise/codespaces-observations.md",
            "# Codespaces observations\n\n"
            "TODO: record the sample command/test you ran in the Codespace terminal.\n\n"
            "TODO: explain one thing possible in Codespaces that is not possible in github.dev.\n\n"
            "TODO: distinguish stopping a Codespace from deleting it.\n",
        )

    elif module == 8:
        copy_template(8, "markdown-practice.md", "exercise/markdown-showcase.md")

    elif module == 9:
        write(
            "exercise/open-source-pr.md",
            "# Open-source contribution practice\n\n"
            "TODO: make the documentation improvement requested by the temporary Module 9 Issue.\n\n"
            "Keep the change focused, explain why it helps, and update it after the automated training review.\n",
        )

    elif module == 10:
        write(
            "exercise/README-sample.md",
            "# Sample InnerSource project\n\n"
            "TODO: document purpose, intended consumers, prerequisites/setup, usage, support, and contribution entry points.\n",
        )
        write(
            "exercise/CONTRIBUTING.md",
            "# Contributing\n\n"
            "TODO: document setup, branch/PR workflow, tests, review expectations, and how to request help.\n",
        )
        write(
            "exercise/CODEOWNERS",
            "# TODO: add path ownership examples for maintainers/teams.\n",
        )
        write(
            "exercise/ISSUE_TEMPLATE/feature.yml",
            "name: InnerSource feature request\n"
            "description: TODO describe what contributors should provide\n"
            "title: '[Feature]: '\n"
            "body:\n"
            "  - type: textarea\n"
            "    id: need\n"
            "    attributes:\n"
            "      label: Need\n"
            "      description: TODO explain the problem and expected outcome\n",
        )
        write(
            "exercise/PULL_REQUEST_TEMPLATE.md",
            "## What changed\nTODO\n\n## Validation\nTODO\n\n## Review/ownership\nTODO\n",
        )
        write(
            "exercise/discoverability-plan.md",
            "# Discoverability plan\n\nTODO: cover repository name/description, topics, README, catalog or internal links, and support ownership.\n",
        )
        write(
            "exercise/access-visibility-matrix.md",
            "# Access and visibility matrix\n\n"
            "TODO: compare relevant visibility/permission choices and apply least privilege for consumers, contributors, maintainers, and admins.\n",
        )
        write(
            "exercise/success-metrics.md",
            "# InnerSource success metrics\n\n"
            "TODO: define useful contribution, response-time, reuse/adoption, and qualitative onboarding measures.\n",
        )

    elif module == 11:
        write(
            "package.json",
            json.dumps(
                {
                    "name": "gh900-security-fixture",
                    "private": True,
                    "version": "1.0.0",
                    "dependencies": {"lodash": "4.17.20"},
                },
                indent=2,
            )
            + "\n",
        )
        write("exercise/sensitive/config.yml", "# Sensitive-path ownership practice\nmode: training\n")
        write(
            "exercise/rules-design.md",
            "# Repository rules design\n\nTODO: design rules that require pull requests, appropriate status checks, and meaningful review.\n",
        )
        write(
            "exercise/secret-remediation.md",
            "# Secret remediation scenario\n\n"
            "TODO: explain what to do if a real credential is committed, including revocation/rotation and history handling.\n",
        )
        write(
            "exercise/local-secret.example",
            "# Fake training example only. Never place a real secret here.\nEXAMPLE_TOKEN=not-a-real-credential\n",
        )

    elif module == 14:
        write(
            "exercise/review_fixture.py",
            '"""Pull-request review fixture with an intentional defect."""\n\n'
            "def normalized_name(name: str) -> str:\n"
            "    # Intentional defect: whitespace-only input currently returns an empty string.\n"
            "    return name.strip().lower()\n",
        )
        write(
            "exercise/test_review_fixture.py",
            "from review_fixture import normalized_name\n\n"
            "def test_normalizes_name():\n"
            "    assert normalized_name('  Ada Lovelace ') == 'ada lovelace'\n\n"
            "def test_rejects_blank_name():\n"
            "    try:\n"
            "        normalized_name('   ')\n"
            "    except ValueError:\n"
            "        return\n"
            "    raise AssertionError('blank names should raise ValueError')\n",
        )

    elif module == 15:
        write(
            "exercise/history-fixture.txt",
            "GH-900 history investigation fixture\n"
            "Stable behavior: cache keys are normalized before lookup.\n",
        )

    elif module == 16:
        copy_template(16, "app.py", "exercise/app.py")
        copy_template(16, "test_app.py", "exercise/test_app.py")
        copy_template(16, "requirements.txt", "exercise/requirements.txt")

    else:
        write(
            "exercise/task.md",
            f"# {unit} practice\n\nTODO: complete the repository/GitHub task described in the course Issue.\n",
        )


def bootstrap() -> None:
    for rel in [
        "docs",
        "modules",
        "unit-details",
        "curriculum",
        "labs",
        "scripts",
        "course",
        "course-content",
        ".devcontainer",
        ".github/CONTRIBUTING.md",
        ".github/CODE_OF_CONDUCT.md",
        ".github/SECURITY.md",
        ".github/ARCHITECTURE.md",
        ".github/MAINTAINING.md",
        ".github/workflows/quality.yml",
    ]:
        path = ROOT / rel
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists() or path.is_symlink():
            path.unlink()

    clean_visible()
    (ROOT / "README.md").write_text(
        "# GH-900 Interactive Foundations — Learner Workspace\n\n"
        "This repository is an interactive course workspace. The lesson itself lives in the "
        "**GH-900 Interactive Foundations — Course** Issue.\n\n"
        "- Follow the latest instruction in the course Issue.\n"
        "- Exercise files appear only when the current lesson needs them.\n"
        "- Temporary exercise branches/files are cleaned after validation.\n"
        "- Do not edit `.gh900/` or the course workflows; they are the internal course engine.\n\n"
        "Open **Issues** to continue the course.\n",
        encoding="utf-8",
    )


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("bootstrap")
    prep = sub.add_parser("prepare")
    prep.add_argument("--unit", required=True)
    sub.add_parser("clean")
    args = p.parse_args()
    if args.command == "bootstrap":
        bootstrap()
    elif args.command == "prepare":
        prepare(args.unit)
    else:
        clean_visible()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
