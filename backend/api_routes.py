import os
import secrets
from typing import Any

from flask import Blueprint, jsonify, request

from admin_service import (
    build_admin_home,
    build_exercise_history,
    build_password_reset_form,
    build_user_list,
    build_user_status,
    change_password,
    delete_target_user,
    enter_admin,
    promote_mock_exam,
)
from exercise_service import process_exercise, start_exam
from menu_service import build_main_menu
from single_exam_service import check_single_answer, start_single_exam
from users import check_login, checkPeriod, getStatus, setStage

api_module = Blueprint("api", __name__)


@api_module.get("/api/health")
def health() -> tuple[Any, int]:
    return jsonify({"status": "ok"}), 200


@api_module.post("/api/login")
def login() -> tuple[Any, int]:
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email:
        return jsonify({"message": "Email is required."}), 400
    if not password:
        return jsonify({"message": "Password is required."}), 400

    user_id = check_login(email, password)
    if user_id is False:
        return jsonify({"message": "Invalid email or password."}), 401

    period = checkPeriod(user_id)
    if period == 99:
        return jsonify({"message": "Your access period has not started yet."}), 403
    if period == 101:
        return jsonify({"message": "Your access period has expired."}), 403

    setStage(user_id, 1)
    status = getStatus(user_id)
    token = secrets.token_urlsafe(32)

    return jsonify({
        "token": token,
        "user_id": user_id,
        "status": status,
        "message": "Login successful.",
    }), 200


@api_module.get("/api/main-menu")
def main_menu() -> tuple[Any, int]:
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"message": "user_id is required."}), 400

    status = getStatus(user_id)
    if status is False:
        return jsonify({"message": "User not found."}), 404

    return jsonify(build_main_menu(user_id)), 200


@api_module.post("/api/logout")
def logout() -> tuple[Any, int]:
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"message": "user_id is required."}), 400

    setStage(int(user_id), 0)
    return jsonify({"message": "Logged out."}), 200


@api_module.post("/api/exam/start")
def exam_start() -> tuple[Any, int]:
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    category = data.get("category")

    if not user_id or category is None:
        return jsonify({"message": "user_id and category are required."}), 400

    try:
        payload = start_exam(int(user_id), int(category))
    except PermissionError as exc:
        return jsonify({"message": str(exc)}), 403
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400
    except Exception:
        return jsonify({"message": "Failed to start exam."}), 500

    return jsonify(payload), 200


@api_module.post("/api/exam/action")
def exam_action() -> tuple[Any, int]:
    data = request.get_json(silent=True) or {}
    if not data.get("user_id") or not data.get("exam_id"):
        return jsonify({"message": "user_id and exam_id are required."}), 400

    try:
        payload = process_exercise(data)
    except PermissionError as exc:
        return jsonify({"message": str(exc)}), 403
    except Exception:
        return jsonify({"message": "Failed to process exam action."}), 500

    return jsonify(payload), 200


@api_module.post("/api/single-exam/start")
def single_exam_start() -> tuple[Any, int]:
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    category = data.get("category")

    if not user_id or category is None:
        return jsonify({"message": "user_id and category are required."}), 400

    try:
        payload = start_single_exam(int(user_id), int(category))
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400
    except Exception:
        return jsonify({"message": "Failed to start single-question exam."}), 500

    return jsonify(payload), 200


@api_module.post("/api/single-exam/check")
def single_exam_check() -> tuple[Any, int]:
    data = request.get_json(silent=True) or {}
    required = ("user_id", "category", "area", "crct", "num", "permutation", "cid", "answer")
    if any(data.get(field) is None for field in required):
        return jsonify({"message": "Missing required fields for answer check."}), 400

    try:
        payload = check_single_answer(
            user_id=int(data["user_id"]),
            category=int(data["category"]),
            area=str(data["area"]),
            crct=int(data["crct"]),
            num=str(data["num"]),
            permutation=str(data["permutation"]),
            cid=int(data["cid"]),
            answer=int(data["answer"]),
        )
    except Exception:
        return jsonify({"message": "Failed to check answer."}), 500

    return jsonify(payload), 200


@api_module.post("/api/admin/enter")
def admin_enter() -> tuple[Any, int]:
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"message": "user_id is required."}), 400
    return jsonify(enter_admin(int(user_id))), 200


@api_module.get("/api/admin/home")
def admin_home() -> tuple[Any, int]:
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"message": "user_id is required."}), 400
    return jsonify(build_admin_home(user_id)), 200


@api_module.get("/api/admin/history")
def admin_history() -> tuple[Any, int]:
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"message": "user_id is required."}), 400
    return jsonify(build_exercise_history(user_id)), 200


@api_module.get("/api/admin/status")
def admin_status() -> tuple[Any, int]:
    user_id = request.args.get("user_id", type=int)
    target_user_id = request.args.get("target_user_id", type=int)
    if not user_id:
        return jsonify({"message": "user_id is required."}), 400
    return jsonify(build_user_status(user_id, target_user_id or user_id)), 200


@api_module.get("/api/admin/users")
def admin_users() -> tuple[Any, int]:
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"message": "user_id is required."}), 400
    try:
        return jsonify(build_user_list(user_id)), 200
    except PermissionError as exc:
        return jsonify({"message": str(exc)}), 403


@api_module.post("/api/admin/users/delete")
def admin_delete_user() -> tuple[Any, int]:
    data = request.get_json(silent=True) or {}
    actor_user_id = data.get("actor_user_id")
    target_user_id = data.get("target_user_id")
    if not actor_user_id or not target_user_id:
        return jsonify({"message": "actor_user_id and target_user_id are required."}), 400
    try:
        return jsonify(delete_target_user(int(actor_user_id), int(target_user_id))), 200
    except PermissionError as exc:
        return jsonify({"message": str(exc)}), 403


@api_module.get("/api/admin/password-reset")
def admin_password_reset_form() -> tuple[Any, int]:
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"message": "user_id is required."}), 400
    try:
        return jsonify(build_password_reset_form(user_id)), 200
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 404


@api_module.post("/api/admin/password-reset")
def admin_password_reset_submit() -> tuple[Any, int]:
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    old_password = data.get("old_password") or ""
    new_password = data.get("new_password") or ""
    if not user_id:
        return jsonify({"message": "user_id is required."}), 400
    return jsonify(change_password(int(user_id), old_password, new_password)), 200


@api_module.post("/api/admin/users/rankup")
def admin_rankup_user() -> tuple[Any, int]:
    data = request.get_json(silent=True) or {}
    actor_user_id = data.get("actor_user_id")
    target_user_id = data.get("target_user_id")
    if not actor_user_id or not target_user_id:
        return jsonify({"message": "actor_user_id and target_user_id are required."}), 400
    try:
        return jsonify(promote_mock_exam(int(actor_user_id), int(target_user_id))), 200
    except PermissionError as exc:
        return jsonify({"message": str(exc)}), 403
