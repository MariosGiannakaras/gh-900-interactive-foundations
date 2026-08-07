#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HASH_FILE = ROOT / ".gh900" / "data" / "assessment-hashes.json"


def digest(module: int, question: str, answer: str) -> str:
    # Module 1 predates the module-prefixed digest namespace. Keep its digest input
    # stable while storing every module's expected hashes in the same data file.
    raw = f"{question}:{answer}" if module == 1 else f"m{module:02d}:{question}:{answer}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--module", required=True, type=int)
    p.add_argument("--answers", required=True)
    args = p.parse_args()

    answers = [x.upper() for x in re.findall(r"\b[A-C]\b", args.answers.upper())]
    all_hashes = json.loads(HASH_FILE.read_text(encoding="utf-8"))
    expected = all_hashes.get(f"{args.module:02d}")
    if expected is None:
        print(f"Unsupported module: {args.module}")
        return 2

    if len(answers) != len(expected):
        print(f"Expected {len(expected)} answers, received {len(answers)}.")
        return 2

    wrong = []
    for i, answer in enumerate(answers, start=1):
        q = f"Q{i}"
        if digest(args.module, q, answer) != expected[q]:
            wrong.append(q)

    if wrong:
        print("Needs review: " + ", ".join(wrong))
        return 1
    print(f"Assessment passed: {len(expected)}/{len(expected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
