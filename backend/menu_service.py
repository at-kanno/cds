from __future__ import annotations

from typing import Any

from config_loader import get_exam_entry, get_menu_template, get_status_rules
from users import getLoginName, getStatus


def _section_message_and_enabled(rule_key: str, status: int) -> tuple[str | None, bool]:
    rules = get_status_rules().get(rule_key)
    if rules is None:
        return None, True

    messages = rules.get("messages", {})
    min_status = rules.get("min_status", 0)

    if rule_key == "mock_exam":
        completed_min = rules.get("completed_min_status", min_status)
        if status < min_status:
            return messages.get("locked"), False
        if status >= completed_min:
            return messages.get("completed"), True
        return messages.get("unlocked"), True

    if rule_key == "final_exam":
        passed_once_status = rules.get("passed_once_status", min_status + 1)
        if status < min_status:
            return messages.get("locked"), False
        if status == passed_once_status:
            return messages.get("passed_once"), True
        if status > passed_once_status:
            return messages.get("completed"), True
        return messages.get("unlocked"), True

    if status < min_status:
        return messages.get("locked"), False
    return messages.get("unlocked"), True


def _item_enabled(
    category: int | None, status: int, default_enabled: bool, section_enabled: bool | None
) -> bool:
    if section_enabled is not None:
        return section_enabled

    if category is None or int(category) == 0:
        return default_enabled

    entry = get_exam_entry(int(category))
    if entry is None:
        return default_enabled

    required = entry.get("requires_status_min")
    if required is None:
        return default_enabled
    return status >= required


def _build_items(
    raw_items: list[dict[str, Any]], status: int, section_enabled: bool | None
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for item in raw_items:
        category = item.get("category", 0)
        payload: dict[str, Any] = {
            "category": int(category) if category is not None else 0,
            "action": item["action"],
            "label": item["label"],
            "subtitle": item.get("subtitle", ""),
            "color": item.get("color", "#808080"),
            "enabled": _item_enabled(
                category,
                status,
                item.get("enabled", True),
                section_enabled,
            ),
        }
        if item.get("submenu"):
            payload["submenu"] = item["submenu"]
        items.append(payload)
    return items


def _build_section(
    section: dict[str, Any], status: int
) -> dict[str, Any]:
    rule_key = section.get("status_rule")
    section_message = None
    section_enabled = None
    if rule_key:
        section_message, section_enabled = _section_message_and_enabled(rule_key, status)

    built: dict[str, Any] = {
        "id": section["id"],
        "title": section.get("title", ""),
        "items": _build_items(section.get("items", []), status, section_enabled),
    }
    if section_message:
        built["message"] = section_message
    return built


def build_main_menu(user_id: int) -> dict[str, Any]:
    status = getStatus(user_id)
    if status is False:
        status = 0

    email = getLoginName(user_id)
    if email is False:
        email = ""

    menu = get_menu_template()
    sections = [_build_section(section, status) for section in menu.get("sections", [])]

    actions = []
    for action in menu.get("actions", []):
        payload: dict[str, Any] = {
            "id": action["id"],
            "label": action["label"],
            "action": action["action"],
            "enabled": action.get("enabled", True),
        }
        if "category" in action:
            payload["category"] = action["category"]
        actions.append(payload)

    result: dict[str, Any] = {
        "user_id": user_id,
        "email": email,
        "status": status,
        "title": menu.get("title", "メインメニュー"),
        "sections": sections,
        "actions": actions,
    }

    if menu.get("hierarchy"):
        result["hierarchy"] = True
        submenus: dict[str, Any] = {}
        for key, section in menu.get("submenus", {}).items():
            submenus[key] = _build_section(section, status)
        result["submenus"] = submenus

    return result
