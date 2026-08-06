#!/usr/bin/env python3
"""Audit independently written learner output against the pinned Microsoft Learn source inventory.

This is not a text-similarity or copying check. It verifies that all 106 locked upstream
units resolve at the pinned commit and that the actual Issue-rendered local lesson is
substantial enough not to be a title/objective-only placeholder.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GH900 = ROOT / ".gh900"
UPSTREAM = ROOT / "_microsoft_learn"
LOCK = GH900 / "data" / "microsoft-source-lock.json"
sys.path.insert(0, str(GH900))

import course_unit_state as state  # noqa: E402


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


def main() -> int:
    if not UPSTREAM.exists():
        print(f"ERROR: pinned upstream checkout missing at {UPSTREAM}")
        return 2

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    units = state.load_units()
    by_module = {n: [u for u in units if u.module == n] for n in range(1, 17)}
    errors: list[str] = []
    total = resolved = depth_passed = 0

    for key, meta in lock["modules"].items():
        module = int(key)
        upstream_root = UPSTREAM / meta["root"]
        local_path = ROOT / meta["local"]
        index = upstream_root / "index.yml"
        if not index.exists():
            errors.append(f"M{key}: upstream index missing: {meta['root']}/index.yml")
            continue
        if not local_path.exists():
            errors.append(f"M{key}: local content missing: {meta['local']}")
            continue

        try:
            uids = parse_index_units(index.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"M{key}: {exc}")
            continue

        expected = int(meta["units"])
        local_units = by_module[module]
        if len(uids) != expected or len(local_units) != expected:
            errors.append(
                f"M{key}: unit count mismatch upstream={len(uids)}, runtime={len(local_units)}, expected={expected}"
            )
            continue

        for unit, uid in zip(local_units, uids):
            total += 1
            try:
                source_path, source_text = resolve_unit_source(upstream_root, uid)
                resolved += 1
            except Exception as exc:
                errors.append(f"{unit.id}: cannot resolve {uid}: {exc}")
                continue

            try:
                local_text = state.render(unit)
            except Exception as exc:
                errors.append(f"{unit.id}: local Issue rendering failed: {exc}")
                continue

            source_n = normalized_len(source_text)
            local_n = normalized_len(local_text)
            lower_uid = uid.lower()

            if "knowledge-check" in lower_uid or "assessment" in lower_uid:
                required = 350
            elif "exercise" in lower_uid:
                required = max(350, int(source_n * 0.20))
            elif "introduction" in lower_uid or "summary" in lower_uid:
                required = max(260, int(source_n * 0.25))
            else:
                required = max(300, int(source_n * 0.40))

            if local_n < required:
                rel = source_path.relative_to(UPSTREAM)
                errors.append(
                    f"{unit.id}: depth gate failed local={local_n}, required>={required}, upstream={source_n} ({rel})"
                )
            else:
                depth_passed += 1

    print(f"Pinned Microsoft source commit: {lock['commit']}")
    print(f"Units resolved from upstream source: {resolved}/{total}")
    print(f"Units passing Issue-rendered depth gate: {depth_passed}/{total}")

    if total != 106:
        errors.append(f"Expected 106 locked units, audited {total}")

    if errors:
        print("Semantic-depth audit failures:")
        for item in errors:
            print(f"- {item}")
        return 1

    print("Microsoft source/depth audit passed: 106/106 units.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
