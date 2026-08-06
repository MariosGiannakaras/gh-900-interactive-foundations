#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "curriculum" / "official-curriculum.yml"
CATALOG = ROOT / "curriculum" / "course-catalog.json"

# Modules without an explicit Microsoft exercise still receive a practical checkpoint.
ACTIVITY_OVERRIDES = {
    "m03-u07",  # metered-usage interpretation scenario
    "m07-u06",  # project insights/automation practice
    "m12-u05",  # enterprise governance scenario
    "m13-u05",  # team-sync identity scenario
}
# Module 16 has two official exercise units. The setup unit is guided/read-only because
# Copilot availability varies; the Python API exercise is the validated practical gate.
READ_OVERRIDES = {"m16-u03"}


@dataclass(frozen=True)
class Unit:
    id: str
    module: int
    number: int
    title: str
    mode: str
    readme: str
    branch: str


def load_units() -> list[Unit]:
    text = CURRICULUM.read_text(encoding="utf-8")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    rows = re.findall(
        r"\{\s*id:\s*(m\d{2}-u\d{2}),\s*title:\s*(.*?),\s*implementation:\s*[^}]+\}",
        text,
    )
    units: list[Unit] = []
    for unit_id, title in rows:
        module = int(unit_id[1:3])
        number = int(unit_id[-2:])
        key = f"{module:02d}"
        if unit_id in READ_OVERRIDES:
            mode = "read"
        elif unit_id in ACTIVITY_OVERRIDES or title.lower().startswith("exercise"):
            mode = "activity"
        elif "assessment" in title.lower() or "knowledge check" in title.lower():
            mode = "assessment"
        elif title.strip().lower() == "summary":
            mode = "summary"
        else:
            mode = "read"
        branch = catalog[key]["branch"]
        units.append(Unit(unit_id, module, number, title.strip(), mode, catalog[key]["readme"], branch))
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
    for index, unit in enumerate(units):
        if unit.id == unit_id:
            return units[index + 1] if index + 1 < len(units) else None
    raise KeyError(unit_id)


def extract_local_section(unit: Unit) -> str:
    text = (ROOT / unit.readme).read_text(encoding="utf-8")
    pattern = rf"(?ms)^## Unit {unit.number}\b[^\n]*\n(.*?)(?=^---\s*$|^## Unit \d+\b|^## Official references\b|\Z)"
    match = re.search(pattern, text)
    if not match:
        raise RuntimeError(f"No local section found for {unit.id} in {unit.readme}")
    return match.group(1).strip()


def learner_instruction(unit: Unit) -> str:
    if unit.mode in {"read", "summary"}:
        return (
            "### Continue\n\n"
            "When you have read and understood this unit, comment exactly **`/next`** on the course Issue. "
            "The course engine will unlock the next official unit."
        )
    if unit.mode == "activity":
        submission = f"labs/module-{unit.module:02d}/submission.md"
        return (
            "### Hands-on checkpoint\n\n"
            f"Work on branch **`{unit.branch}`**. Complete the hands-on instructions/evidence in "
            f"[`{submission}`](../blob/main/{submission}). Leave the knowledge-check answers untouched for now. "
            "Commit and push. The course engine validates the activity state automatically; no Actions button is required."
        )
    assessment = "labs/module-01/assessment.md" if unit.module == 1 else f"labs/module-{unit.module:02d}/submission.md"
    return (
        "### Blind assessment\n\n"
        f"Answer the original course questions in [`{assessment}`](../blob/main/{assessment}) on branch **`{unit.branch}`**, "
        "commit, and push. The validator reports only which questions need review; it does not reveal the answer key."
    )


def render(unit: Unit) -> str:
    section = extract_local_section(unit)
    return (
        f"## {unit.id.upper()} — {unit.title}\n\n"
        f"**Official sequence:** Module {unit.module}, Unit {unit.number} · **Mode:** `{unit.mode}`\n\n"
        f"{section}\n\n---\n\n{learner_instruction(unit)}\n"
    )


def as_dict(unit: Unit) -> dict[str, object]:
    nxt = next_unit(unit.id)
    return {
        "id": unit.id,
        "module": unit.module,
        "number": unit.number,
        "title": unit.title,
        "mode": unit.mode,
        "readme": unit.readme,
        "branch": unit.branch,
        "next": nxt.id if nxt else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit")
    parser.add_argument("--first", action="store_true")
    parser.add_argument("--next", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--list-json", action="store_true")
    args = parser.parse_args()

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
    if args.render:
        print(render(unit))
    else:
        print(json.dumps(as_dict(unit)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
