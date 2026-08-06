#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / ".gh900" / "templates"

VISIBLE_CLEANUP = [
    ROOT / "exercise",
    ROOT / ".devcontainer",
    ROOT / "SECURITY.md",
    ROOT / ".github" / "CODEOWNERS",
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
        write("exercise/github-flow.md", "# GitHub Flow practice\n\nTODO: describe and implement one small repository improvement for this exercise.\n")
    elif module == 4:
        copy_template(4, "code-scanning-simulation.yml", "exercise/code-scanning-simulation.yml")
    elif module == 5:
        write(
            "exercise/copilot-practice.py",
            '"""Small practice target for the GitHub Copilot unit."""\n\n'
            "def summarize_items(items: list[str]) -> str:\n"
            "    # TODO: implement a useful summary with validation and clear output.\n"
            "    raise NotImplementedError\n",
        )
    elif module == 6:
        src = TEMPLATES / "devcontainer"
        dst = ROOT / ".devcontainer"
        if not src.exists():
            raise FileNotFoundError("Missing internal devcontainer template")
        shutil.copytree(src, dst)
    elif module == 8:
        copy_template(8, "markdown-practice.md", "exercise/markdown-practice.md")
    elif module == 9:
        write(
            "exercise/open-source-pr.md",
            "# Pull request practice\n\nTODO: make a meaningful contribution here, then use the Issue/PR workflow described in the course.\n",
        )
    elif module == 10:
        copy_template(10, "innersource-program.md", "exercise/innersource-program.md")
    elif module == 11:
        pass
    elif module == 14:
        write(
            "exercise/review_fixture.py",
            '"""Review-practice fixture."""\n\n'
            "def normalized_name(name: str) -> str:\n"
            "    # TODO: make the implementation robust and document the behavior in the PR.\n"
            "    return name\n",
        )
    elif module == 15:
        write(
            "exercise/history-practice.txt",
            "GH-900 history practice\nTODO: make multiple meaningful commits, then create the tag requested in the course.\n",
        )
    elif module == 16:
        copy_template(16, "app.py", "exercise/app.py")
        copy_template(16, "test_app.py", "exercise/test_app.py")
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
        "LICENSE",
        ".github/CONTRIBUTING.md",
        ".github/CODE_OF_CONDUCT.md",
        ".github/SECURITY.md",
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
