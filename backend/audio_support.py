"""Listening audio helpers: NUMBER.mp3 (optional shared FLAG 201-299)."""

from __future__ import annotations

import os
import re
from typing import Any

import constant

# Shared conversation audio uses FLAG in this range (optional).
# Normal questions use {NUMBER}.mp3 with FLAG outside this range (0, etc.).
LISTENING_FLAG_MIN = 201
LISTENING_FLAG_MAX = 299

_SAFE_STEM = re.compile(r"^[0-9]+$")


def resolve_audio_dir() -> str:
    """Directory for mp3 files (not in git). Override with EXAM_AUDIO_DIR."""
    override = os.environ.get("EXAM_AUDIO_DIR", "").strip()
    if override:
        return override if os.path.isabs(override) else os.path.join(constant.base_path, override)
    return os.path.join(constant.base_path, "audio")


def is_listening_share_flag(flag) -> bool:
    if flag is None or flag == "":
        return False
    try:
        value = int(flag)
    except (TypeError, ValueError):
        return False
    return LISTENING_FLAG_MIN <= value <= LISTENING_FLAG_MAX


def resolve_audio_stem(number, flag=0) -> str:
    """Return filename stem: shared FLAG when 201-299, else question NUMBER."""
    if is_listening_share_flag(flag):
        return str(int(flag))
    return str(int(number))


def get_listening_settings_for_category(category: int | None) -> dict[str, Any] | None:
    if category is None:
        return None
    try:
        from config_loader import get_areas

        for area in get_areas():
            if int(category) not in [int(c) for c in area.get("categories", [])]:
                continue
            if not area.get("listening"):
                return None
            return {
                "max_audio_plays": int(area.get("max_audio_plays", 2)),
            }
    except Exception as exc:
        print(f"listening settings lookup failed for category={category}: {exc}")
    return None


def audio_filename_for_question(number, flag=0) -> str:
    return f"{resolve_audio_stem(number, flag)}.mp3"


def resolve_audio_path(number, flag=0) -> str | None:
    """Return absolute path if the mp3 exists.

    Prefer shared FLAG file when FLAG is 201-299; fall back to NUMBER.mp3.
    """
    audio_dir = resolve_audio_dir()
    candidates = [audio_filename_for_question(number, flag)]
    number_name = f"{int(number)}.mp3"
    if candidates[0] != number_name:
        candidates.append(number_name)

    for name in candidates:
        path = os.path.join(audio_dir, name)
        if os.path.isfile(path):
            return path
    return None


def get_audio_play_info(question) -> dict[str, Any] | None:
    """Build listening playback info for a Question-like object, or None."""
    category = getattr(question, "category", None)
    settings = get_listening_settings_for_category(category)
    if not settings:
        return None

    number = getattr(question, "number", None)
    if number is None:
        return None
    flag = getattr(question, "flag", 0)
    path = resolve_audio_path(number, flag)
    if not path:
        print(
            f"listening audio missing: number={number}, flag={flag}, "
            f"dir={resolve_audio_dir()}"
        )
        return None

    filename = os.path.basename(path)
    if not _SAFE_STEM.match(filename[:-4]) or not filename.endswith(".mp3"):
        return None

    return {
        "filename": filename,
        "max_audio_plays": settings["max_audio_plays"],
        "path": path,
    }


def is_safe_audio_filename(filename: str) -> bool:
    if not filename or "/" in filename or "\\" in filename or ".." in filename:
        return False
    if not filename.endswith(".mp3"):
        return False
    return bool(_SAFE_STEM.match(filename[:-4]))
