#!/usr/bin/env python3
"""Pure helpers for GH-900 lesson markers and comment/unit association.

These functions intentionally have no GitHub/network dependency so the same protocol
can be exercised exhaustively in Course Quality and used by runtime validators.
"""
from __future__ import annotations

import re
from typing import Iterable, Mapping, Any

UNIT_RE = re.compile(r"^m\d{2}-u\d{2}$")
MARKER_RE = re.compile(r"<!--\s*gh900-unit:(m\d{2}-u\d{2})\s*-->")


def lesson_marker(unit_id: str) -> str:
    if not UNIT_RE.fullmatch(unit_id):
        raise ValueError(f"Invalid unit id: {unit_id}")
    return f"<!-- gh900-unit:{unit_id} -->"


def extract_lesson_marker(body: str) -> str | None:
    match = MARKER_RE.search(body or "")
    return match.group(1) if match else None


def response_unit(comments: Iterable[Mapping[str, Any]], comment_id: int) -> str | None:
    """Return the lesson marker immediately in force when a comment was created.

    GitHub comment IDs are monotonic for an Issue. Bot acknowledgement comments do not
    change the current lesson; only a rendered lesson carrying gh900-unit does.
    """
    current: str | None = None
    ordered = sorted(
        (c for c in comments if isinstance(c.get("id"), int) and int(c["id"]) < comment_id),
        key=lambda c: int(c["id"]),
    )
    for comment in ordered:
        marker = extract_lesson_marker(str(comment.get("body", "")))
        if marker:
            current = marker
    return current


def response_matches_unit(comments: Iterable[Mapping[str, Any]], comment_id: int, unit_id: str) -> bool:
    return response_unit(comments, comment_id) == unit_id


def bodies_for_unit(
    comments: Iterable[Mapping[str, Any]], prefix: str, unit_id: str
) -> list[str]:
    """Collect learner response bodies whose preceding rendered lesson is unit_id."""
    rows = sorted(
        (c for c in comments if isinstance(c.get("id"), int)),
        key=lambda c: int(c["id"]),
    )
    current: str | None = None
    result: list[str] = []
    prefix_lower = prefix.lower()
    for comment in rows:
        body = str(comment.get("body", "")).strip()
        marker = extract_lesson_marker(body)
        if marker:
            current = marker
            continue
        if current == unit_id and body.lower().startswith(prefix_lower):
            result.append(body)
    return result
