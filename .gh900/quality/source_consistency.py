#!/usr/bin/env python3
"""Keep canonical lesson source aligned with the current on-demand runtime.

The Issue renderer should not need to hide/translate an abandoned implementation model.
This gate rejects old branch/path names and obsolete post-unit implementation sections in
`.gh900/content` while leaving ordinary conceptual references untouched.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / ".gh900" / "content"

FORBIDDEN = {
    "lab/module-": "legacy module-named learner branch",
    "labs/module-": "legacy top-level lab artifact path",
    "## Interactive course flow": "obsolete post-unit runtime description",
    "## Interactive lab": "obsolete post-unit lab description",
    "## Interactive identity simulation": "obsolete identity simulation block",
    "## Hands-on/simulation layer": "obsolete simulation block",
    "account-plan-decisions.md": "obsolete billing worksheet",
    "project-report.md": "obsolete Projects worksheet",
    "history-investigation.md": "obsolete history worksheet",
    "then asks the learner to use the same Markdown in an Issue comment": "obsolete duplicate Markdown submission step",
}


def main() -> int:
    errors: list[str] = []
    files = sorted(CONTENT.glob("**/README.md"))
    for path in files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for needle, description in FORBIDDEN.items():
            if needle in text:
                errors.append(f"{rel}: {description}: {needle}")

    if len(files) != 16:
        errors.append(f"Expected 16 canonical module README files, found {len(files)}")

    if errors:
        print("Canonical source/runtime consistency failures:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Canonical lesson source matches the current runtime model: no legacy lab paths/blocks remain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
