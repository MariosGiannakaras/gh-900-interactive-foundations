#!/usr/bin/env python3
"""Audit local unit depth against the pinned Microsoft Learn source snapshot.

This is deliberately not a copyright/similarity checker. It verifies that every unit
can be resolved at the locked upstream commit and that the local, independently worded
coverage presented to the learner is substantial enough not to be a title/objective-only placeholder.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "curriculum" / "microsoft-source-lock.json"
UPSTREAM = ROOT / "_microsoft_learn"
DETAILS = ROOT / "unit-details"


def normalized_len(text: str) -> int:
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r":::image.*?:::", " ", text, flags=re.DOTALL)
    text = re.sub(r"[`#>*_\[\]()|:-]", " ", text)
    return len(re.sub(r"\s+", " ", text).strip())


def parse_index_units(text: str) -> list[str]:
    match = re.search(r"(?ms)^units:\s*\n(.*?)(?=^[A-Za-z_][\w-]*:\s*(?:\n|$))", text)
    if not match:
        raise ValueError("index.yml has no parseable units block")
    return [m.group(1).strip() for m in re.finditer(r"(?m)^\s*-\s+([^\s#]+)", match.group(1))]


def resolve_unit_source(module_root: Path, uid: str) -> tuple[Path, str]:
    for yml in module_root.glob("*.yml"):
        text = yml.read_text(encoding="utf-8")
        if re.search(rf"(?m)^uid:\s*{re.escape(uid)}\s*$", text):
            include = re.search(r"\[!include\[\]\(([^)]+)\)\]", text)
            if include:
                path = (yml.parent / include.group(1)).resolve()
                return path, path.read_text(encoding="utf-8")
            return yml, text
    raise FileNotFoundError(f"No unit source YAML found for {uid}")


def extract_local_unit(readme: str, number: int) -> str:
    pattern = rf"(?ms)^## Unit {number}\b[^\n]*\n(.*?)(?=^---\s*$|^## Unit \d+\b|^## Official references\b|\Z)"
    match = re.search(pattern, readme)
    return match.group(1).strip() if match else ""


def extract_detail(key: str, number: int) -> str:
    path = DETAILS / f"m{key}.md"
    if not path.exists():
        return ""
    unit_id = f"m{key}-u{number:02d}"
    text = path.read_text(encoding="utf-8")
    pattern = rf"(?ms)^## {re.escape(unit_id)}\s*$\n(.*?)(?=^## m\d{{2}}-u\d{{2}}\s*$|\Z)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def main() -> int:
    if not UPSTREAM.exists():
        print(f"ERROR: pinned upstream checkout missing at {UPSTREAM}")
        return 2

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    errors: list[str] = []
    total = 0
    resolved = 0
    depth_passed = 0

    for key, meta in lock["modules"].items():
        upstream_root = UPSTREAM / meta["root"]
        local_readme = ROOT / meta["local"]
        index = upstream_root / "index.yml"
        if not index.exists():
            errors.append(f"M{key}: upstream index missing: {meta['root']}/index.yml")
            continue
        if not local_readme.exists():
            errors.append(f"M{key}: local README missing: {meta['local']}")
            continue

        try:
            uids = parse_index_units(index.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"M{key}: {exc}")
            continue

        expected = int(meta["units"])
        if len(uids) != expected:
            errors.append(f"M{key}: pinned Microsoft index has {len(uids)} units, lock expects {expected}")
            continue

        local_text = local_readme.read_text(encoding="utf-8")
        lab = ROOT / f"labs/module-{key}/submission.md"
        lab_text = lab.read_text(encoding="utf-8") if lab.exists() else ""

        for number, uid in enumerate(uids, 1):
            total += 1
            try:
                source_path, source_text = resolve_unit_source(upstream_root, uid)
                resolved += 1
            except Exception as exc:
                errors.append(f"M{key} U{number}: cannot resolve {uid}: {exc}")
                continue

            local_unit = extract_local_unit(local_text, number)
            if not local_unit:
                errors.append(f"M{key} U{number}: local Unit heading/content missing for {uid}")
                continue

            detail = extract_detail(key, number)
            source_n = normalized_len(source_text)
            local_n = normalized_len(local_unit) + normalized_len(detail)
            lower_uid = uid.lower()

            if "knowledge-check" in lower_uid or "assessment" in lower_uid:
                if local_n < 220:
                    errors.append(f"M{key} U{number}: assessment coverage is too thin ({local_n} chars)")
                else:
                    depth_passed += 1
                continue

            if "exercise" in lower_uid:
                local_n += normalized_len(lab_text)
                ratio = 0.20
            elif "introduction" in lower_uid or "summary" in lower_uid:
                ratio = 0.25
            else:
                ratio = 0.40

            required = max(240, int(source_n * ratio))
            if local_n < required:
                rel = source_path.relative_to(UPSTREAM)
                errors.append(
                    f"M{key} U{number}: semantic-depth gate failed: local={local_n}, "
                    f"required>={required}, upstream={source_n} ({rel})"
                )
            else:
                depth_passed += 1

    print(f"Pinned Microsoft source commit: {lock['commit']}")
    print(f"Units resolved from upstream source: {resolved}/{total}")
    print(f"Units passing depth gate: {depth_passed}/{total}")
    if errors:
        print("\nSemantic-depth audit failures:")
        for item in errors:
            print(f"- {item}")
        return 1

    if total != 106:
        print(f"ERROR: expected 106 units in locked curriculum, audited {total}")
        return 1

    print("Microsoft semantic-depth audit passed: 106/106 units.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
