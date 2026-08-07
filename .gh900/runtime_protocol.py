#!/usr/bin/env python3
"""Pure helpers for GH-900 lesson markers and comment/unit association.

These functions intentionally have no GitHub/network dependency so the same protocol
can be exercised exhaustively in Course Quality and used by runtime validators.
"""
from __future__ import annotations

import re
from typing import Any, Iterable, Mapping

UNIT_RE = re.compile(r"^m\d{2}-u\d{2}$")
MARKER_RE = re.compile(r"<!--\s*gh900-unit:(m\d{2}-u\d{2})\s*-->")
AUTOMATION_LOGIN = "github-actions[bot]"


def lesson_marker(unit_id: str) -> str:
    if not UNIT_RE.fullmatch(unit_id):
        raise ValueError(f"Invalid unit id: {unit_id}")
    return f"<!-- gh900-unit:{unit_id} -->"


def extract_lesson_marker(body: str) -> str | None:
    match = MARKER_RE.search(body or "")
    return match.group(1) if match else None


def is_authoritative_lesson_comment(comment: Mapping[str, Any]) -> bool:
    """Return True only for lesson comments posted by the course automation actor."""
    user = comment.get("user")
    return isinstance(user, Mapping) and user.get("login") == AUTOMATION_LOGIN


def authoritative_lesson_marker(comment: Mapping[str, Any]) -> str | None:
    """Extract a lesson marker only from a trusted automation-authored comment."""
    if not is_authoritative_lesson_comment(comment):
        return None
    return extract_lesson_marker(str(comment.get("body", "")))


def response_unit(comments: Iterable[Mapping[str, Any]], comment_id: int) -> str | None:
    """Return the authoritative lesson marker in force when a comment was created.

    GitHub comment IDs are monotonic for an Issue. Learner-authored marker lookalikes
    are protocol data, not authority, and must never change the current lesson.
    """
    current: str | None = None
    ordered = sorted(
        (c for c in comments if isinstance(c.get("id"), int) and int(c["id"]) < comment_id),
        key=lambda c: int(c["id"]),
    )
    for comment in ordered:
        marker = authoritative_lesson_marker(comment)
        if marker:
            current = marker
    return current


def response_matches_unit(comments: Iterable[Mapping[str, Any]], comment_id: int, unit_id: str) -> bool:
    return response_unit(comments, comment_id) == unit_id


def bodies_for_unit(
    comments: Iterable[Mapping[str, Any]], prefix: str, unit_id: str
) -> list[str]:
    """Collect learner response bodies scoped by authoritative rendered lessons."""
    rows = sorted(
        (c for c in comments if isinstance(c.get("id"), int)),
        key=lambda c: int(c["id"]),
    )
    current: str | None = None
    result: list[str] = []
    prefix_lower = prefix.lower()
    for comment in rows:
        body = str(comment.get("body", "")).strip()
        marker = authoritative_lesson_marker(comment)
        if marker:
            current = marker
            continue
        if current == unit_id and body.lower().startswith(prefix_lower):
            result.append(body)
    return result
