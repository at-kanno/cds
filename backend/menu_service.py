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


def _item_enabled(category: int, status: int, default_enabled: bool, section_enabled: bool | None) -> bool:
    if section_enabled is not None:
        return section_enabled

    entry = get_exam_entry(category)
    if entry is None:
        return default_enabled

    required = entry.get("requires_status_min")
    if required is None:
        return default_enabled
    return status >= required


def build_main_menu(user_id: int) -> dict[str, Any]:
    status = getStatus(user_id)
    if status is False:
        status = 0

    email = getLoginName(user_id)
    if email is False:
        email = ""

    menu = get_menu_template()
    sections: list[dict[str, Any]] = []

    for section in menu.get("sections", []):
        rule_key = section.get("status_rule")
        section_message = None
        section_enabled = None
        if rule_key:
            section_message, section_enabled = _section_message_and_enabled(rule_key, status)

        items: list[dict[str, Any]] = []
        for item in section.get("items", []):
            items.append(
                {
                    "category": item["category"],
                    "action": item["action"],
                    "label": item["label"],
                    "subtitle": item["subtitle"],
                    "color": item["color"],
                    "enabled": _item_enabled(
                        item["category"],
                        status,
                        item.get("enabled", True),
                        section_enabled,
                    ),
                }
            )

        built: dict[str, Any] = {
            "id": section["id"],
            "title": section["title"],
            "items": items,
        }
        if section_message:
            built["message"] = section_message
        sections.append(built)

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

    return {
        "user_id": user_id,
        "email": email,
        "status": status,
        "title": menu.get("title", "メインメニュー"),
        "sections": sections,
        "actions": actions,
    }
