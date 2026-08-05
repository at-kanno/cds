"""Question image helpers: backend/image/{NUMBER}.png"""

from __future__ import annotations

import os
import re
from typing import Any

import constant

_SAFE_STEM = re.compile(r"^[0-9]+$")
_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


def resolve_image_dir() -> str:
    """Directory for question images (and optional colocated Part1 mp3)."""
    override = os.environ.get("EXAM_IMAGE_DIR", "").strip()
    if override:
        return override if os.path.isabs(override) else os.path.join(constant.base_path, override)
    return os.path.join(constant.base_path, "image")


def is_safe_image_filename(filename: str) -> bool:
    if not filename or "/" in filename or "\\" in filename or ".." in filename:
        return False
    lower = filename.lower()
    if not any(lower.endswith(ext) for ext in _IMAGE_EXTENSIONS):
        return False
    stem = filename.rsplit(".", 1)[0]
    return bool(_SAFE_STEM.match(stem))


def resolve_image_path(number) -> str | None:
    """Return absolute path for {NUMBER}.png/.jpg if present."""
    try:
        stem = str(int(number))
    except (TypeError, ValueError):
        return None
    image_dir = resolve_image_dir()
    for ext in _IMAGE_EXTENSIONS:
        path = os.path.join(image_dir, f"{stem}{ext}")
        if os.path.isfile(path):
            return path
    return None


def get_image_info(question) -> dict[str, Any] | None:
    number = getattr(question, "number", None)
    if number is None:
        return None
    path = resolve_image_path(number)
    if not path:
        return None
    filename = os.path.basename(path)
    if not is_safe_image_filename(filename):
        return None
    return {"filename": filename, "path": path}
