#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".gh900"
SOURCE_CATALOG = ROOT / "curriculum" / "course-catalog.json"
RUNTIME_CATALOG = RUNTIME / "data" / "course-catalog.json"


def catalogs() -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    return (
        json.loads(SOURCE_CATALOG.read_text(encoding="utf-8")),
        json.loads(RUNTIME_CATALOG.read_text(encoding="utf-8")),
    )


def source_detail(key: str) -> Path | None:
    path = ROOT / "unit-details" / f"m{key}.md"
    return path if path.exists() else None


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def sync_write() -> None:
    source, runtime = catalogs()

    for key in source:
        src_item = source[key]
        run_item = runtime[key]
        copy_file(ROOT / str(src_item["readme"]), ROOT / str(run_item["readme"]))
        src_detail = source_detail(key)
        run_detail = run_item.get("detail")
        if src_detail and run_detail:
            copy_file(src_detail, ROOT / str(run_detail))

    for name in ["official-curriculum.yml", "assessment-hashes.json", "microsoft-source-lock.json"]:
        copy_file(ROOT / "curriculum" / name, RUNTIME / "data" / name)

    runtime_labs = RUNTIME / "templates" / "labs"
    if runtime_labs.exists():
        shutil.rmtree(runtime_labs)
    shutil.copytree(ROOT / "labs", runtime_labs)
    unused = runtime_labs / "module-01" / "submission.md"
    if unused.exists():
        unused.unlink()

    runtime_dev = RUNTIME / "templates" / "devcontainer"
    if runtime_dev.exists():
        shutil.rmtree(runtime_dev)
    shutil.copytree(ROOT / ".devcontainer", runtime_dev)


def same_file(a: Path, b: Path) -> bool:
    return a.exists() and b.exists() and a.read_bytes() == b.read_bytes()


def check() -> list[str]:
    errors: list[str] = []
    source, runtime = catalogs()

    if set(source) != set(runtime):
        errors.append("source and runtime catalogs must contain the same 16 module keys")
        return errors

    for key in source:
        src_item = source[key]
        run_item = runtime[key]
        if src_item.get("title") != run_item.get("title"):
            errors.append(f"Module {key} title differs between source and runtime catalog")
        expected_part = 1 if int(key) <= 8 else 2
        if int(run_item.get("part", 0)) != expected_part:
            errors.append(f"Module {key} runtime catalog has wrong Part value")

        src_readme = ROOT / str(src_item["readme"])
        run_readme = ROOT / str(run_item["readme"])
        if not same_file(src_readme, run_readme):
            errors.append(f"Module {key} packaged lesson is out of sync with {src_readme.relative_to(ROOT)}")

        src_detail = source_detail(key)
        run_detail_raw = run_item.get("detail")
        run_detail = ROOT / str(run_detail_raw) if run_detail_raw else None
        if bool(src_detail) != bool(run_detail):
            errors.append(f"Module {key} source/runtime detail mapping differs")
        elif src_detail and run_detail and not same_file(src_detail, run_detail):
            errors.append(f"Module {key} packaged detail is out of sync with {src_detail.relative_to(ROOT)}")

    for name in ["official-curriculum.yml", "assessment-hashes.json", "microsoft-source-lock.json"]:
        if not same_file(ROOT / "curriculum" / name, RUNTIME / "data" / name):
            errors.append(f"runtime data is out of sync: {name}")

    source_labs = ROOT / "labs"
    runtime_labs = RUNTIME / "templates" / "labs"
    expected_source = {
        path.relative_to(source_labs)
        for path in source_labs.rglob("*")
        if path.is_file() and path.relative_to(source_labs).as_posix() != "module-01/submission.md"
    }
    actual_runtime = {path.relative_to(runtime_labs) for path in runtime_labs.rglob("*") if path.is_file()}
    if expected_source != actual_runtime:
        missing = sorted(str(x) for x in expected_source - actual_runtime)
        extra = sorted(str(x) for x in actual_runtime - expected_source)
        if missing:
            errors.append("runtime lab templates missing: " + ", ".join(missing))
        if extra:
            errors.append("unexpected runtime lab templates: " + ", ".join(extra))
    for rel in expected_source & actual_runtime:
        if not same_file(source_labs / rel, runtime_labs / rel):
            errors.append(f"runtime lab template out of sync: {rel}")

    source_dev = ROOT / ".devcontainer"
    runtime_dev = RUNTIME / "templates" / "devcontainer"
    source_files = {p.relative_to(source_dev) for p in source_dev.rglob("*") if p.is_file()}
    runtime_files = {p.relative_to(runtime_dev) for p in runtime_dev.rglob("*") if p.is_file()}
    if source_files != runtime_files:
        errors.append("runtime devcontainer template file set is out of sync")
    for rel in source_files & runtime_files:
        if not same_file(source_dev / rel, runtime_dev / rel):
            errors.append(f"runtime devcontainer template out of sync: {rel}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Synchronize packaged learner content from canonical source")
    args = parser.parse_args()

    if args.write:
        sync_write()

    errors = check()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        if not args.write:
            print("Run: python3 scripts/sync_learner_runtime.py --write")
        return 1

    print("Learner runtime package is synchronized with canonical source.")
    print("Modules/details: 16/16")
    print("Curriculum/source-lock/assessment data: synchronized")
    print("Exercise templates: synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
