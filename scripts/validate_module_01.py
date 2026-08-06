#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ASSESSMENT = Path("labs/module-01/assessment.md")
EXPECTED_HASHES = {
    "Q1": "e03a69c76f96143bcf7b4201d0a4cc6b8d7759cbc74ff08aa6bb15068e96ee3d",
    "Q2": "37360f1fbeb07882c89a009532110f5fdc227b84acf3f06640fbe753f56478c4",
    "Q3": "f9f003ccdefd764a152af94c8335ec292b4a91cf402c17c88b3e9240abc9b61d",
    "Q4": "6eda2a848d37516a3c34dda208d38585b145f1a1ba6a6294c82e64313907e7bb",
    "Q5": "2b5d4b1bb78beea18d02e9fb6da5079b9368577589b40857fe37e49cb5210554",
    "Q6": "15362d98bee1b5ce53045f9d37dd1a45a8f08051e7854fedd65a91a533d6bc68",
}


def digest(question: str, answer: str) -> str:
    return hashlib.sha256(f"{question}:{answer}".encode("utf-8")).hexdigest()


def main() -> int:
    text = ASSESSMENT.read_text(encoding="utf-8")
    sections = re.split(r"(?=^## Q\d+\s*$)", text, flags=re.MULTILINE)
    parsed: dict[str, str] = {}
    malformed: list[str] = []

    for section in sections:
        header = re.match(r"^## (Q\d+)\s*$", section, flags=re.MULTILINE)
        if not header:
            continue
        question = header.group(1)
        checked = re.findall(r"^- \[[xX]\] ([A-C])\.", section, flags=re.MULTILINE)
        if len(checked) != 1:
            malformed.append(question)
            continue
        parsed[question] = checked[0]

    if malformed or set(parsed) != set(EXPECTED_HASHES):
        problems = sorted(set(malformed) | (set(EXPECTED_HASHES) - set(parsed)))
        print("Assessment format is incomplete. Check exactly one option for each question.")
        print("Needs attention: " + ", ".join(problems))
        return 2

    wrong = [
        question
        for question, answer in parsed.items()
        if digest(question, answer) != EXPECTED_HASHES[question]
    ]

    score = len(EXPECTED_HASHES) - len(wrong)
    print(f"Score: {score}/{len(EXPECTED_HASHES)}")
    if wrong:
        print("Review these questions: " + ", ".join(sorted(wrong)))
        return 1

    print("Module 1 assessment passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
