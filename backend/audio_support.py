"""Listening audio: NUMBER.mp3, NUMBER-Q.mp3, or choice NUMBER-A..D.mp3."""

from __future__ import annotations

import os
import re
from typing import Any

import constant

# Spanish shared listening stem uses FLAG in this range (optional).
LISTENING_FLAG_MIN = 201
LISTENING_FLAG_MAX = 299
# TOEIC Part3/4 set audio: FLAG = set-head NUMBER → {FLAG}.mp3 (301-399 / 401-499).
SET_AUDIO_FLAG_MIN = 301
SET_AUDIO_FLAG_MAX = 499

SET_HEAD_NOTE = (
    "この会話音声は続く問題でも使います。再生は1回のみです。ここで再生してください。"
)
SET_FOLLOW_NOTE = "このセットの音声は先頭の問題で再生してください。"
SET_FOLLOW_NOTE_WITH_Q = "このセットの音声は問題{head_q_no}で再生してください。"
SET_FOLLOW_PLAYED_SUFFIX = "（再生済みです）"

_SAFE_STEM = re.compile(r"^[0-9]+$")
_SAFE_CHOICE_STEM = re.compile(r"^[0-9]+-[A-D]$")
_SAFE_QUESTION_STEM = re.compile(r"^[0-9]+-Q$")
_CHOICE_LETTERS = ("A", "B", "C", "D")


def resolve_audio_dir() -> str:
    """Directory for mp3 files. Override with EXAM_AUDIO_DIR."""
    override = os.environ.get("EXAM_AUDIO_DIR", "").strip()
    if override:
        return override if os.path.isabs(override) else os.path.join(constant.base_path, override)
    return os.path.join(constant.base_path, "audio")


def _media_search_dirs() -> list[str]:
    """Dirs to search for mp3: audio/, then image/ and image/TOEIC-* packs."""
    dirs = [resolve_audio_dir()]
    try:
        from image_support import media_pack_dirs

        for directory in media_pack_dirs():
            if directory not in dirs:
                dirs.append(directory)
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


def is_set_audio_flag(flag) -> bool:
    """True when FLAG is a TOEIC set-head id used as shared conversation audio."""
    if flag is None or flag == "":
        return False
    try:
        value = int(flag)
    except (TypeError, ValueError):
        return False
    return SET_AUDIO_FLAG_MIN <= value <= SET_AUDIO_FLAG_MAX


def uses_flag_audio_stem(flag) -> bool:
    return is_listening_share_flag(flag) or is_set_audio_flag(flag)


def resolve_audio_stem(number, flag=0) -> str:
    """Return filename stem: shared/set FLAG when applicable, else question NUMBER."""
    if uses_flag_audio_stem(flag):
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
            settings: dict[str, Any] = {
                "max_audio_plays": int(area.get("max_audio_plays", 2)),
            }
            if area.get("set_size"):
                settings["set_size"] = int(area["set_size"])
            return settings
    except Exception as exc:
        print(f"listening settings lookup failed for category={category}: {exc}")
        return None


def get_set_listening_role(question) -> str | None:
    """Return 'head' / 'follow_up' for set listening, else None."""
    category = getattr(question, "category", None)
    settings = get_listening_settings_for_category(category)
    if not settings or not settings.get("set_size"):
        return None
    try:
        number = int(getattr(question, "number"))
        flag = int(getattr(question, "flag", 0) or 0)
    except (TypeError, ValueError):
        return None
    if not is_set_audio_flag(flag):
        return None
    if number == flag:
        return "head"
    return "follow_up"


def get_set_listening_note(question, *, head_q_no: int | None = None) -> str:
    """Exam navigation note for set listening. Analysis screens omit this."""
    role = get_set_listening_role(question)
    if role == "head":
        return SET_HEAD_NOTE
    if role == "follow_up":
        if head_q_no is not None and int(head_q_no) > 0:
            return SET_FOLLOW_NOTE_WITH_Q.format(head_q_no=int(head_q_no))
        return SET_FOLLOW_NOTE
    return ""


def audio_filename_for_question(number, flag=0) -> str:
    return f"{resolve_audio_stem(number, flag)}.mp3"


def resolve_audio_path(number, flag=0) -> str | None:
    """Return absolute path for a stem mp3 if it exists.

    Order: shared/set FLAG file, then ``{NUMBER}-Q.mp3`` (Part2),
    then ``{NUMBER}.mp3``. Searches audio/ and image/TOEIC-* packs.
    """
    candidates: list[str] = []
    if uses_flag_audio_stem(flag):
        candidates.append(audio_filename_for_question(number, flag))
    try:
        stem = str(int(number))
    except (TypeError, ValueError):
        return None
    candidates.append(f"{stem}-Q.mp3")
    candidates.append(f"{stem}.mp3")

    # Keep unique order
    seen: set[str] = set()
    ordered: list[str] = []
    for name in candidates:
        if name not in seen:
            seen.add(name)
            ordered.append(name)

    for directory in _media_search_dirs():
        for name in ordered:
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
    """Map original A1..A4 files onto display slots A..D via permutation."""
    slots = parse_permutation(permutation)
    mapped: dict[str, str] = {}
    for i, display_letter in enumerate(_CHOICE_LETTERS):
        orig = slots[i]
        if orig <= 0 or orig > 4:
            continue
        orig_letter = _CHOICE_LETTERS[orig - 1]
        path = original_paths.get(orig_letter)
        if path:
            # Normalize separators so Windows-style paths still yield a basename on Linux.
            mapped[display_letter] = os.path.basename(path.replace("\\", "/"))
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
    """Per-choice clips ({NUMBER}-A.mp3 .. D), remapped by permutation."""
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


def get_audio_play_info(
    question,
    *,
    hide_set_follow_up: bool = False,
) -> dict[str, Any] | None:
    """Stem / question mp3 ({NUMBER}-Q.mp3 or {NUMBER}.mp3), or None.

    May coexist with choice clips (Part2: Q + A/B/C).
    Multi-exam set listening can hide the player on follow-up questions;
    一問一答 keeps audio available on every question.
    """
    category = getattr(question, "category", None)
    settings = get_listening_settings_for_category(category)
    if not settings:
        return None

    number = getattr(question, "number", None)
    if number is None:
        return None
    flag = getattr(question, "flag", 0)
    role = get_set_listening_role(question)
    if hide_set_follow_up and role == "follow_up":
        return None

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
    stem = filename[:-4] if filename.endswith(".mp3") else ""
    if not (_SAFE_STEM.match(stem) or _SAFE_QUESTION_STEM.match(stem)):
        return None

    info: dict[str, Any] = {
        "filename": filename,
        "max_audio_plays": settings["max_audio_plays"],
        "path": path,
    }
    if role:
        info["set_role"] = role
    return info


def is_safe_audio_filename(filename: str) -> bool:
    if not filename or "/" in filename or "\\" in filename or ".." in filename:
        return False
    if not filename.endswith(".mp3"):
        return False
    stem = filename[:-4]
    return bool(
        _SAFE_STEM.match(stem)
        or _SAFE_CHOICE_STEM.match(stem)
        or _SAFE_QUESTION_STEM.match(stem)
    )
