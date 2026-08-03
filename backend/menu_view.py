from typing import Any

from flask import render_template

from menu_service import build_main_menu


def render_main_menu_page(user_id: int) -> Any:
    """Render HTML main menu from config-driven menu_service output."""
    menu = build_main_menu(int(user_id))
    return render_template(
        "main-menu.html",
        user_id=int(user_id),
        status=menu.get("status", 0),
        menu=menu,
    )
