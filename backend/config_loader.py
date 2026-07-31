from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any

base_path = os.path.dirname(__file__)
DEFAULT_CONFIG_PATH = os.path.join(base_path, "static", "config.json")


def get_profile_name() -> str:
    return os.environ.get("APP_PROFILE", "CDS").upper()


def get_config_path() -> str:
    return os.environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH)


def clear_config_cache() -> None:
    load_raw_config.cache_clear()


@lru_cache
def load_raw_config() -> dict[str, Any]:
    with open(get_config_path(), encoding="utf-8") as handle:
        return json.load(handle)


def get_profile_section() -> dict[str, Any]:
    config = load_raw_config()
    profile_name = get_profile_name()
    if profile_name not in config:
        raise KeyError(
            f"APP_PROFILE={profile_name!r} not found in {get_config_path()}"
        )
    return config[profile_name]


def get_default_section() -> dict[str, Any]:
    return load_raw_config().get("DEFAULT", {})


def get_exam_entry(category: int) -> dict[str, Any] | None:
    catalog = get_profile_section().get("exam_catalog", {})
    entry = catalog.get(str(category))
    if entry is None:
        return None
    return dict(entry)


def get_menu_template() -> dict[str, Any]:
    menu = get_profile_section().get("menu")
    if menu is None:
        raise KeyError(
            f"menu block missing for APP_PROFILE={get_profile_name()!r}"
        )
    return menu


def get_status_rules() -> dict[str, Any]:
    return get_profile_section().get("status_rules", {})


def get_areas() -> list[dict[str, Any]]:
    return get_profile_section().get("areas", [])


def build_area_globals(
    areas: list[dict[str, Any]],
) -> tuple[list[str], list[list[Any]], list[list[str]], list[str], list[int]]:
    abbreviation: list[str] = []
    areaname: list[list[Any]] = []
    practice: list[list[str]] = []
    practice2: list[str] = []
    category_number: list[int] = []

    for area in areas:
        name = area["name"]
        abbrev = area["abbrev"]
        categories = area.get("categories", [])
        practices = area.get("practices", [])

        abbreviation.append(abbrev)
        areaname.append([name, len(categories), "", "", ""])
        practice.append(list(practices))
        practice2.extend(practices)
        category_number.extend(categories)

    return abbreviation, areaname, practice, practice2, category_number
