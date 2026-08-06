#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HASH_FILE = ROOT / ".gh900" / "data" / "assessment-hashes.json"

MODULE1 = {
    "Q1": "e03a69c76f96143bcf7b4201d0a4cc6b8d7759cbc74ff08aa6bb15068e96ee3d",
    "Q2": "37360f1fbeb07882c89a009532110f5fdc227b84acf3f06640fbe753f56478c4",
    "Q3": "f9f003ccdefd764a152af94c8335ec292b4a91cf402c17c88b3e9240abc9b61d",
    "Q4": "6eda2a848d37516a3c34dda208d38585b145f1a1ba6a6294c82e64313907e7bb",
    "Q5": "2b5d4b1bb78beea18d02e9fb6da5079b9368577589b40857fe37e49cb5210554",
    "Q6": "15362d98bee1b5ce53045f9d37dd1a45a8f08051e7854fedd65a91a533d6bc68",
    "Q7": "d23f9052dc22f4d281fa3eb266a91aea0cdcf6daa06c6e29bd46fe816a9736a7",
    "Q8": "b0d2f1585a10fb8225f257b7ba1e090fd276815728120ae05d5c04cc182ccb25",
    "Q9": "c60b831f2441d3fb18d5483e5c13576d97d593aba691401e552fc7c85151fc94",
    "Q10": "77a4018a9dbce5a7e92c5ca36b0a12f190abf2aa15813deacf47a9607b7be1cc",
    "Q11": "754a5728fe202eb8a9f1598528322cb119891cf9ff1c95386d51c944fd052ee5",
    "Q12": "e29dad8e4008e304881f092cf6ff7d16ff350e87bdfb79ac6f69e860304f1268",
}

def digest(module: int, question: str, answer: str) -> str:
    raw = f"{question}:{answer}" if module == 1 else f"m{module:02d}:{question}:{answer}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--module", required=True, type=int)
    p.add_argument("--answers", required=True)
    args = p.parse_args()

    answers = [x.upper() for x in re.findall(r"\b[A-C]\b", args.answers.upper())]
    if args.module == 1:
        expected = MODULE1
    else:
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
