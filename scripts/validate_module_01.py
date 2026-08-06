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
    "Q7": "d23f9052dc22f4d281fa3eb266a91aea0cdcf6daa06c6e29bd46fe816a9736a7",
    "Q8": "b0d2f1585a10fb8225f257b7ba1e090fd276815728120ae05d5c04cc182ccb25",
    "Q9": "c60b831f2441d3fb18d5483e5c13576d97d593aba691401e552fc7c85151fc94",
    "Q10": "77a4018a9dbce5a7e92c5ca36b0a12f190abf2aa15813deacf47a9607b7be1cc",
    "Q11": "754a5728fe202eb8a9f1598528322cb119891cf9ff1c95386d51c944fd052ee5",
    "Q12": "e29dad8e4008e304881f092cf6ff7d16ff350e87bdfb79ac6f69e860304f1268",
}


def digest(question: str, answer: str) -> str:
    return hashlib.sha256(f"{question}:{answer}".encode("utf-8")).hexdigest()


def question_sort_key(question: str) -> int:
    return int(question.removeprefix("Q"))


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

    expected = set(EXPECTED_HASHES)
    actual = set(parsed)
    if malformed or actual != expected:
        problems = set(malformed) | (expected - actual) | (actual - expected)
        ordered = sorted(problems, key=question_sort_key)
        print("Assessment format is incomplete or changed. Check exactly one option for every expected question.")
        print("Needs attention: " + ", ".join(ordered))
        return 2

    wrong = [
        question
        for question, answer in parsed.items()
        if digest(question, answer) != EXPECTED_HASHES[question]
    ]
    wrong.sort(key=question_sort_key)

    score = len(EXPECTED_HASHES) - len(wrong)
    print(f"Score: {score}/{len(EXPECTED_HASHES)}")
    if wrong:
        print("Review these questions: " + ", ".join(wrong))
        return 1

    print("Module 1 assessment passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
