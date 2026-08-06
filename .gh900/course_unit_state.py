#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / ".gh900" / "data"
TEMPLATES = ROOT / ".gh900" / "templates"

ACTIVITY_OVERRIDES = set()
SCENARIO_OVERRIDES = {"m03-u07", "m07-u06", "m12-u05", "m13-u05"}
READ_OVERRIDES = {"m16-u03"}
PR_ACTIVITY_MODULES = {2, 9, 14}

@dataclass(frozen=True)
class Unit:
    id: str
    part: int
    module: int
    number: int
    title: str
    mode: str
    branch: str | None
    sandbox: str | None
    content_path: str
    detail_path: str | None
    module_units: int
    ordinal: int

def _catalog() -> dict[str, dict[str, object]]:
    return json.loads((DATA / "course-catalog.json").read_text(encoding="utf-8"))

def load_units() -> list[Unit]:
    manifest = (DATA / "official-curriculum.yml").read_text(encoding="utf-8")
    catalog = _catalog()
    rows = re.findall(
        r"\{\s*id:\s*(m\d{2}-u\d{2}),\s*title:\s*(.*?),\s*implementation:\s*[^}]+\}",
        manifest,
    )
    counts = {
        int(m): int(c)
        for m, c in re.findall(
            r"(?ms)^      - id: m(\d{2})\n.*?^        unit_count: (\d+)",
            manifest,
        )
    }
    units: list[Unit] = []
    for ordinal, (unit_id, title) in enumerate(rows, start=1):
        module = int(unit_id[1:3])
        number = int(unit_id[-2:])
        part = 1 if module <= 8 else 2
        lower = title.strip().lower()
        if unit_id in READ_OVERRIDES:
            mode = "read"
        elif unit_id in SCENARIO_OVERRIDES:
            mode = "scenario"
        elif unit_id in ACTIVITY_OVERRIDES or "exercise" in lower:
            mode = "activity"
        elif "assessment" in lower or "knowledge check" in lower:
            mode = "assessment"
        elif lower == "summary":
            mode = "summary"
        else:
            mode = "read"
        branch = f"lab/{unit_id}" if mode == "activity" else None
        sandbox = f"sandbox/{unit_id}" if mode == "activity" else None
        item = catalog[f"{module:02d}"]
        units.append(
            Unit(
                unit_id,
                part,
                module,
                number,
                title.strip(),
                mode,
                branch,
                sandbox,
                str(item["readme"]),
                str(item["detail"]) if item.get("detail") else None,
                counts[module],
                ordinal,
            )
        )
    if len(units) != 106:
        raise RuntimeError(f"Expected 106 units, parsed {len(units)}")
    return units

def find(unit_id: str) -> Unit:
    for unit in load_units():
        if unit.id == unit_id:
            return unit
    raise KeyError(unit_id)

def next_unit(unit_id: str) -> Unit | None:
    units = load_units()
    for i, unit in enumerate(units):
        if unit.id == unit_id:
            return units[i + 1] if i + 1 < len(units) else None
    raise KeyError(unit_id)

def extract_local_section(unit: Unit) -> str:
    text = (ROOT / unit.content_path).read_text(encoding="utf-8")
    pattern = rf"(?ms)^## Unit {unit.number}\b[^\n]*\n(.*?)(?=^---\s*$|^## Unit \d+\b|^## Official references\b|\Z)"
    match = re.search(pattern, text)
    if not match:
        raise RuntimeError(f"No learner content found for {unit.id}")
    return match.group(1).strip()

def extract_detail_section(unit: Unit) -> str:
    if not unit.detail_path:
        return ""
    path = ROOT / unit.detail_path
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    pattern = rf"(?ms)^## {re.escape(unit.id)}\s*$\n(.*?)(?=^## m\d{{2}}-u\d{{2}}\s*$|\Z)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""

def _assessment_file(module: int) -> Path:
    if module == 1:
        return TEMPLATES / "labs" / "module-01" / "assessment.md"
    return TEMPLATES / "labs" / f"module-{module:02d}" / "submission.md"

def assessment_questions(module: int) -> tuple[str, int]:
    text = _assessment_file(module).read_text(encoding="utf-8")
    if module != 1 and "## Knowledge check" in text:
        text = text.split("## Knowledge check", 1)[1]
    sections = re.split(r"(?=^#{2,3} Q\d+\s*$)", text, flags=re.MULTILINE)
    rendered: list[str] = []
    count = 0
    for section in sections:
        header = re.match(r"^#{2,3} Q(\d+)\s*$", section, flags=re.MULTILINE)
        if not header:
            continue
        count += 1
        qnum = header.group(1)
        body = re.sub(r"^#{2,3} Q\d+\s*$", "", section, count=1, flags=re.MULTILINE).strip()
        body = re.sub(r"(?m)^- \[[ xX]\] ([A-C])\.\s*", r"- **\1.** ", body)
        rendered.append(f"### Question {qnum}\n\n{body}")
    if not rendered:
        raise RuntimeError(f"No assessment questions found for Module {module}")
    return "\n\n".join(rendered), count

def scenario_instruction(unit: Unit) -> str:
    prompts = {
        "m03-u07": (
            "Apply the metered-usage concepts from this unit to a short administration scenario. "
            "Explain what you would inspect in a usage report, how you would distinguish quantity/usage from cost, "
            "and what you would verify before making a billing decision."
        ),
        "m07-u06": (
            "Describe a small GitHub Projects automation and insight setup: name a field/status change that should "
            "trigger automation and explain what view/chart/insight you would use to monitor progress."
        ),
        "m12-u05": (
            "Given repository, organization, and enterprise scopes, explain where you would apply an access or "
            "governance policy and how least privilege affects the role/permission you choose."
        ),
        "m13-u05": (
            "Explain how team synchronization connects an identity provider/group to a GitHub team, and distinguish "
            "that synchronization from authentication and authorization."
        ),
    }
    return prompts[unit.id]

def activity_instruction(unit: Unit) -> str:
    tasks = {
        1: "Complete the Git practice in `exercise/`: make the requested edits and commits, create a temporary practice branch, and merge it back into the learner branch.",
        2: f"Edit `exercise/github-flow.md`. Create an Issue whose title includes `[GH-900 {unit.id}]`, then complete GitHub Flow with a PR.",
        4: "Complete `exercise/code-scanning-simulation.yml` using the code-scanning concepts taught above.",
        5: "Complete `exercise/copilot-practice.py`. Use Copilot if available, but the validator checks the resulting code rather than requiring a paid feature.",
        6: "Customize `.devcontainer/devcontainer.json` as described above.",
        8: "Complete `exercise/markdown-practice.md` and demonstrate the GitHub-flavored Markdown features taught in this module.",
        9: "Edit `exercise/open-source-pr.md` and complete the temporary PR workflow as your safe contribution practice.",
        10: "Complete `exercise/innersource-program.md` with a realistic InnerSource program design.",
        11: "Create a real `SECURITY.md` and `.github/CODEOWNERS` on the learner branch. They exist only for this exercise and are removed with the temporary branch afterward.",
        14: f"Improve `exercise/review_fixture.py`, create an Issue whose title includes `[GH-900 {unit.id}]`, link it from the PR body, review the diff, and merge the PR.",
        15: f"Edit `exercise/history-practice.txt` in at least two learner commits, inspect the history, then create and push tag `gh900-{unit.id}`. Comment `/check` after the tag is pushed.",
        16: "Complete `exercise/app.py` until `exercise/test_app.py` passes.",
    }
    task = tasks.get(unit.module, "Complete the GitHub/repository task described above.")
    pr_note = ""
    if unit.module in PR_ACTIVITY_MODULES:
        pr_note = (
            f"\n\n> [!IMPORTANT]\n> This exercise uses a temporary sandbox. Open the Pull Request from "
            f"`{unit.branch}` into `{unit.sandbox}` — **not** into `main`. Merge the PR when the exercise is complete. "
            "The course cleans both temporary branches afterward."
        )
    return (
        "### Hands-on\n\n"
        "The course engine has prepared only what this unit needs. "
        f"Work on **`{unit.branch}`**. {task}\n\n"
        "The instructions on this Issue are the source of truth; you do not need to read internal course files. "
        "Commit and push your work. Validation runs automatically."
        f"{pr_note}\n\n"
        "> [!TIP]\n> If an automatic check was missed, comment `/check` in this Issue."
    )

def continuation(unit: Unit) -> str:
    if unit.mode in {"read", "summary"}:
        extra = ""
        if unit.id == "m08-u05":
            extra = "\n\n> [!IMPORTANT]\n> Completing this step finishes **GitHub Foundations Part 1 of 2**."
        return (
            f"{extra}\n\n### Continue\n\n"
            "When ready, comment exactly **`/next`**."
        ).strip()
    if unit.mode == "activity":
        return activity_instruction(unit)
    if unit.mode == "scenario":
        return (
            "### Apply it\n\n"
            f"{scenario_instruction(unit)}\n\n"
            "Reply with **`/scenario `** followed by your answer. The response is checked for the required concepts; "
            "no worksheet file is created."
        )
    questions, count = assessment_questions(unit.module)
    return (
        "## Check your understanding\n\n"
        f"{questions}\n\n"
        "### Submit\n\n"
        f"Reply with **`/answer `** followed by {count} letters in question order, separated by spaces. "
        "Example: `/answer A C B ...`. The validator reports only the question numbers that need review."
    )

def _modernize_section(unit: Unit, section: str) -> str:
    if unit.mode == "activity" and unit.branch:
        section = re.sub(r"`lab/module-[^`]+`", f"`{unit.branch}`", section)
        section = re.sub(r"create the module branch\s+`[^`]+`", f"use the temporary learner branch `{unit.branch}` created by the course engine", section, flags=re.IGNORECASE)
        section = section.replace("create/edit the module lab file", "edit the temporary exercise file created for this unit")
        section = section.replace("module lab file", "temporary exercise file")
    return section

def render(unit: Unit) -> str:
    section = _modernize_section(unit, extract_local_section(unit))
    detail = extract_detail_section(unit)
    merged = section + (f"\n\n### Additional source-audited detail\n\n{detail}" if detail else "")
    progress = round(unit.ordinal / 106 * 100)
    intro = ""
    if unit.id == "m01-u01":
        intro = "> [!NOTE]\n> **Part 1 of 2 starts here.**\n\n"
    elif unit.id == "m09-u01":
        intro = "> [!IMPORTANT]\n> **Part 1 complete. GitHub Foundations Part 2 of 2 starts here.**\n\n"
    return (
        f"{intro}"
        f"# {unit.title}\n\n"
        f"| Course position | Progress |\n"
        f"|---|---:|\n"
        f"| Part **{unit.part} / 2** · Module **{unit.module} / 16** · Unit **{unit.number} / {unit.module_units}** | "
        f"**{unit.ordinal} / 106** ({progress}%) |\n\n"
        f"{merged}\n\n---\n\n{continuation(unit)}\n"
    )

def as_dict(unit: Unit) -> dict[str, object]:
    nxt = next_unit(unit.id)
    return {
        "id": unit.id,
        "part": unit.part,
        "module": unit.module,
        "number": unit.number,
        "ordinal": unit.ordinal,
        "module_units": unit.module_units,
        "title": unit.title,
        "mode": unit.mode,
        "branch": unit.branch,
        "sandbox": unit.sandbox,
        "requires_pr": unit.module in PR_ACTIVITY_MODULES if unit.mode == "activity" else False,
        "next": nxt.id if nxt else None,
    }

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--unit")
    p.add_argument("--first", action="store_true")
    p.add_argument("--next", action="store_true")
    p.add_argument("--render", action="store_true")
    p.add_argument("--list-json", action="store_true")
    args = p.parse_args()
    units = load_units()
    if args.list_json:
        print(json.dumps([as_dict(u) for u in units], indent=2))
        return 0
    unit = units[0] if args.first else find(args.unit)
    if args.next:
        nxt = next_unit(unit.id)
        if nxt is None:
            return 3
        unit = nxt
    print(render(unit) if args.render else json.dumps(as_dict(unit)))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
