"""Load per-subject exam plans from YAML files under static/subjects/."""

from __future__ import annotations

import os
import random
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

base_path = Path(__file__).parent
SUBJECTS_DIR = base_path / "static" / "subjects"


def get_profile_name() -> str:
    return os.environ.get("APP_PROFILE", "CDS").upper()


def _plan_path(profile: str | None = None) -> Path:
    profile = (profile or get_profile_name()).lower()
    return SUBJECTS_DIR / f"{profile}.exams.yaml"


def plan_exists(profile: str | None = None) -> bool:
    return _plan_path(profile).is_file()


def clear_exam_plan_cache() -> None:
    load_exam_plan.cache_clear()


@lru_cache
def load_exam_plan(profile: str | None = None) -> dict[str, Any] | None:
    path = _plan_path(profile)
    if not path.is_file():
        return None
    with open(path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        return None
    return data


def _format_time(seconds: int) -> str:
    if seconds >= 3600 and seconds % 3600 == 0:
        hours = seconds // 3600
        return f"{hours}時間"
    if seconds >= 60 and seconds % 60 == 0:
        minutes = seconds // 60
        return f"{minutes}分"
    if seconds >= 60:
        minutes = seconds // 60
        remainder = seconds % 60
        if remainder == 15:
            return f"{minutes}分15秒"
        if remainder == 30:
            return f"{minutes}分30秒"
        return f"{minutes}分{remainder}秒"
    return f"{seconds}秒"


def _resolve_area_category(plan: dict[str, Any], area_key: str) -> int:
    topics = plan.get("topics", {})
    topic = topics.get(area_key)
    if topic:
        if "category" in topic:
            return int(topic["category"])
        categories = topic.get("categories")
        if categories:
            return int(categories[0])

    areas = plan.get("areas", {})
    area = areas.get(area_key)
    if area:
        categories = area.get("categories")
        if categories:
            return int(categories[0])
        if "category" in area:
            return int(area["category"])

    raise KeyError(f"Unknown area/topic {area_key!r} in exam plan")


def _weighted_pick(options: list[dict[str, Any]]) -> dict[str, Any]:
    total = sum(int(option.get("weight", 1)) for option in options)
    roll = random.randint(1, total)
    accumulated = 0
    for option in options:
        accumulated += int(option.get("weight", 1))
        if roll <= accumulated:
            return option
    return options[-1]


def _category_pool(plan: dict[str, Any], rule: dict[str, Any]) -> list[int] | None:
    """Return equal-weight category pool from ``from:`` or ``pick:`` shorthand."""
    if "from" in rule:
        pool = rule["from"]
        if not pool:
            raise ValueError(f"Empty from pool in slot rule: {rule}")
        return [int(value) for value in pool]

    if "pick" in rule and all(
        isinstance(option, (int, str)) for option in rule["pick"]
    ):
        # Shorthand: pick: [11, 12]  (equal weight)
        return [int(value) for value in rule["pick"]]

    return None


def _pick_from_pool(pool: list[int]) -> int:
    return int(random.choice(pool))


def _expand_equal_from(rule: dict[str, Any]) -> list[int]:
    """Distribute ``count`` picks evenly across ``equal_from`` categories."""
    pool = [int(value) for value in rule.get("equal_from", [])]
    if not pool:
        raise ValueError(f"equal_from pool is empty: {rule}")
    count = int(rule.get("count") or rule.get("repeat") or 0)
    if count <= 0:
        raise ValueError(f"equal_from requires positive count: {rule}")

    base, remainder = divmod(count, len(pool))
    order = list(pool)
    random.shuffle(order)
    assigned: list[int] = []
    for index, category in enumerate(order):
        n = base + (1 if index < remainder else 0)
        assigned.extend([category] * n)
    random.shuffle(assigned)
    return assigned


def _expand_slot_rule(plan: dict[str, Any], rule: dict[str, Any]) -> list[int]:
    if "use" in rule:
        sequence_name = rule["use"]
        sequences = plan.get("sequences", {})
        sequence = sequences.get(sequence_name)
        if sequence is None:
            raise KeyError(f"Unknown sequence {sequence_name!r} in exam plan")
        categories: list[int] = []
        for item in sequence:
            categories.extend(_expand_slot_rule(plan, item))
        take = rule.get("take")
        if take is not None:
            return categories[: int(take)]
        return categories

    if "equal_from" in rule:
        return _expand_equal_from(rule)

    if "repeat" in rule:
        count = int(rule["repeat"])
        pool = _category_pool(plan, rule)
        if pool is not None:
            return [_pick_from_pool(pool) for _ in range(count)]
        if "area" in rule:
            category = _resolve_area_category(plan, rule["area"])
        elif "category" in rule:
            category = int(rule["category"])
        else:
            raise ValueError(f"repeat rule missing area/category/from: {rule}")
        return [category] * count

    pool = _category_pool(plan, rule)
    if pool is not None:
        return [_pick_from_pool(pool)]

    if "pick" in rule:
        choice = _weighted_pick(rule["pick"])
        if "area" in choice:
            return [_resolve_area_category(plan, choice["area"])]
        if "category" in choice:
            return [int(choice["category"])]
        raise ValueError(f"pick choice missing area/category: {choice}")

    if "area" in rule:
        return [_resolve_area_category(plan, rule["area"])]
    if "category" in rule:
        return [int(rule["category"])]

    raise ValueError(f"Invalid slot rule: {rule}")


def count_exam_slots(plan: dict[str, Any], exam: dict[str, Any]) -> int:
    if "assign_categories" in exam:
        return len(exam["assign_categories"])
    slots = exam.get("slots")
    if not slots:
        return int(exam.get("amount", 1))

    total = 0
    for rule in slots:
        if "use" in rule:
            sequence_name = rule["use"]
            sequence = plan.get("sequences", {}).get(sequence_name, [])
            seq_count = sum(
                count_exam_slots(plan, {"slots": [item]}) for item in sequence
            )
            take = rule.get("take")
            total += min(int(take), seq_count) if take is not None else seq_count
        elif "equal_from" in rule:
            total += int(rule.get("count") or rule.get("repeat") or 0)
        elif "repeat" in rule:
            total += int(rule["repeat"])
        elif "from" in rule or "pick" in rule:
            total += 1
        else:
            total += 1
    return total


def resolve_assign_categories(
    category: int, profile: str | None = None
) -> list[int] | None:
    plan = load_exam_plan(profile)
    if not plan:
        return None

    exam = plan.get("exams", {}).get(str(category))
    if not exam:
        return None

    static = exam.get("assign_categories")
    if static:
        return [int(value) for value in static]

    slots = exam.get("slots")
    if not slots:
        return None

    categories: list[int] = []
    for rule in slots:
        categories.extend(_expand_slot_rule(plan, rule))
    return categories


def get_plan_areas(profile: str | None = None) -> list[dict[str, Any]] | None:
    plan = load_exam_plan(profile)
    if not plan:
        return None

    areas = plan.get("areas")
    if not areas:
        return None

    order = plan.get("area_order", list(areas.keys()))
    result: list[dict[str, Any]] = []
    for key in order:
        area = areas.get(key)
        if not area:
            continue
        entry = dict(area)
        if "categories" not in entry and "category" in entry:
            entry["categories"] = [int(entry["category"])]
        result.append(entry)
    return result


def get_plan_status_rules(profile: str | None = None) -> dict[str, Any] | None:
    plan = load_exam_plan(profile)
    if not plan:
        return None
    rules = plan.get("status_rules")
    if not rules:
        return None
    return dict(rules)


def _build_menu_item(
    exam_id: str, exam: dict[str, Any], plan: dict[str, Any]
) -> dict[str, Any]:
    menu_meta = exam.get("menu", {})
    mode = exam.get("mode", "multi")
    amount = count_exam_slots(plan, exam)
    time_sec = int(exam.get("time_limit_seconds", 0))

    if menu_meta.get("subtitle"):
        subtitle = menu_meta["subtitle"]
    elif mode == "single":
        subtitle = f"時間:{_format_time(time_sec)} / 1問"
    else:
        subtitle = f"時間:{_format_time(time_sec)} / {amount}問"

    return {
        "category": int(exam_id),
        "action": exam.get("action", "makeExam"),
        "label": menu_meta.get("label", exam.get("title", exam_id)),
        "subtitle": subtitle,
        "color": menu_meta.get("color", "#808080"),
    }


def _build_section_items(
    plan: dict[str, Any], item_refs: list[Any]
) -> list[dict[str, Any]]:
    exams = plan.get("exams", {})
    items: list[dict[str, Any]] = []
    for item_ref in item_refs:
        if isinstance(item_ref, dict):
            items.append(dict(item_ref))
            continue
        exam_id = str(item_ref)
        exam = exams.get(exam_id)
        if exam is None:
            raise KeyError(
                f"Exam {exam_id!r} referenced in menu but missing from exams"
            )
        items.append(_build_menu_item(exam_id, exam, plan))
    return items


def _build_hierarchical_menu(
    plan: dict[str, Any], menu_block: dict[str, Any]
) -> dict[str, Any]:
    top_items: list[dict[str, Any]] = []
    for item in menu_block.get("top", []):
        top_items.append(
            {
                "category": int(item.get("category", 0)),
                "action": item.get("action", "openSubmenu"),
                "submenu": item.get("submenu"),
                "label": item["label"],
                "subtitle": item.get("subtitle", ""),
                "color": item.get("color", "#808080"),
                "enabled": item.get("enabled", True),
            }
        )

    submenus: dict[str, Any] = {}
    for key, section in menu_block.get("submenus", {}).items():
        built = {
            "id": key,
            "title": section.get("title", key),
            "items": _build_section_items(plan, section.get("items", [])),
        }
        if "status_rule" in section:
            built["status_rule"] = section["status_rule"]
        submenus[key] = built

    return {
        "title": menu_block.get("title", "メインメニュー"),
        "hierarchy": True,
        "sections": [{"id": "home", "title": "", "items": top_items}],
        "submenus": submenus,
        "actions": list(menu_block.get("actions", [])),
    }


def get_menu_from_plan(profile: str | None = None) -> dict[str, Any] | None:
    plan = load_exam_plan(profile)
    if not plan or "menu" not in plan:
        return None

    menu_block = plan["menu"]
    if menu_block.get("hierarchy"):
        return _build_hierarchical_menu(plan, menu_block)

    sections: list[dict[str, Any]] = []

    for section in menu_block.get("sections", []):
        built_section: dict[str, Any] = {
            "id": section["id"],
            "title": section["title"],
            "items": _build_section_items(plan, section.get("items", [])),
        }
        if "status_rule" in section:
            built_section["status_rule"] = section["status_rule"]
        sections.append(built_section)

    return {
        "title": menu_block.get("title", "メインメニュー"),
        "sections": sections,
        "actions": list(menu_block.get("actions", [])),
    }


def get_exam_plan_entry(
    category: int, profile: str | None = None
) -> dict[str, Any] | None:
    plan = load_exam_plan(profile)
    if not plan:
        return None

    exam = plan.get("exams", {}).get(str(category))
    if not exam:
        return None

    entry = dict(exam)
    entry["amount"] = count_exam_slots(plan, exam)
    return entry
