"""Listening audio helpers: NUMBER.mp3 or Part1 NUMBER-A..D.mp3 (FLAG 201-299)."""

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
_SAFE_CHOICE_STEM = re.compile(r"^[0-9]+-[A-D]$")
_CHOICE_LETTERS = ("A", "B", "C", "D")


def resolve_audio_dir() -> str:
    """Directory for mp3 files (not in git). Override with EXAM_AUDIO_DIR."""
    override = os.environ.get("EXAM_AUDIO_DIR", "").strip()
    if override:
        return override if os.path.isabs(override) else os.path.join(constant.base_path, override)
    return os.path.join(constant.base_path, "audio")


def _media_search_dirs() -> list[str]:
    """Dirs to search for mp3: audio/ first, then image/ (TOEIC Part1 colocated)."""
    dirs = [resolve_audio_dir()]
    try:
        from image_support import resolve_image_dir

        image_dir = resolve_image_dir()
        if image_dir not in dirs:
            dirs.append(image_dir)
    except Exception:
        pass
    return dirs


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
    """Return absolute path if a single mp3 exists.

    Prefer shared FLAG file when FLAG is 201-299; fall back to NUMBER.mp3.
    Searches backend/audio/ then backend/image/.
    """
    candidates = [audio_filename_for_question(number, flag)]
    number_name = f"{int(number)}.mp3"
    if candidates[0] != number_name:
        candidates.append(number_name)

    for directory in _media_search_dirs():
        for name in candidates:
            path = os.path.join(directory, name)
            if os.path.isfile(path):
                return path
    return None


def resolve_choice_audio_paths(number) -> dict[str, str]:
    """Return {A: path, ...} for existing {NUMBER}-A.mp3 .. {NUMBER}-D.mp3."""
    try:
        stem = str(int(number))
    except (TypeError, ValueError):
        return {}
    found: dict[str, str] = {}
    for letter in _CHOICE_LETTERS:
        name = f"{stem}-{letter}.mp3"
        for directory in _media_search_dirs():
            path = os.path.join(directory, name)
            if os.path.isfile(path):
                found[letter] = path
                break
    return found


def parse_permutation(value) -> list[int]:
    """Normalize examlist / form permutation to four slots (1..4, unused=0)."""
    if value is None:
        return [1, 2, 3, 4]
    if isinstance(value, str):
        slots = [int(ch) for ch in value[:4] if ch.isdigit()]
    else:
        try:
            slots = [int(x) for x in list(value)[:4]]
        except (TypeError, ValueError):
            return [1, 2, 3, 4]
    while len(slots) < 4:
        slots.append(0)
    return slots[:4]


def map_choice_audio_to_display(
    original_paths: dict[str, str],
    permutation,
) -> dict[str, str]:
    """Map original A1..A4 files onto display slots A..D via permutation.

    Example: permutation [2,1,3,4] → display A plays *-B.mp3, B plays *-A.mp3.
    """
    slots = parse_permutation(permutation)
    mapped: dict[str, str] = {}
    for i, display_letter in enumerate(_CHOICE_LETTERS):
        orig = slots[i]
        if orig <= 0 or orig > 4:
            continue
        orig_letter = _CHOICE_LETTERS[orig - 1]
        path = original_paths.get(orig_letter)
        if path:
            mapped[display_letter] = os.path.basename(path)
    return mapped


def locate_audio_file(filename: str) -> str | None:
    """Return absolute path for a safe audio filename, or None."""
    if not is_safe_audio_filename(filename):
        return None
    for directory in _media_search_dirs():
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            return path
    return None


def get_choice_audio_info(question) -> dict[str, Any] | None:
    """Part1-style per-choice clips ({NUMBER}-A.mp3 .. D), or None.

    Filenames are stored for original A1..A4; ``question.permutation`` remaps
    them onto the shuffled display order (same rule as answer text).
    """
    category = getattr(question, "category", None)
    settings = get_listening_settings_for_category(category)
    if not settings:
        return None

    number = getattr(question, "number", None)
    if number is None:
        return None

    paths = resolve_choice_audio_paths(number)
    if not paths:
        return None

    choices = map_choice_audio_to_display(
        paths,
        getattr(question, "permutation", None),
    )
    if not choices:
        return None

    return {
        "choices": choices,
        "max_audio_plays": settings["max_audio_plays"],
    }


def get_audio_play_info(question) -> dict[str, Any] | None:
    """Build single-file listening info, or None.

    Prefer a single {NUMBER}.mp3. If only Part1 choice clips exist, return None
    (use get_choice_audio_info instead).
    """
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
        if resolve_choice_audio_paths(number):
            return None
        print(
            f"listening audio missing: number={number}, flag={flag}, "
            f"dirs={_media_search_dirs()}"
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
    stem = filename[:-4]
    return bool(_SAFE_STEM.match(stem) or _SAFE_CHOICE_STEM.match(stem))
