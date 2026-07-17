from typing import Any, List

from resultDB import getUserResultList, getUserResultList1, getUserResultList2
from users import (
    deleteUser,
    getLoginName,
    getLoginPassword,
    getStatus,
    getUserList,
    password_verify,
    rankUp,
    setPassword,
    setStage,
)


def _grade_label(status: int) -> str:
    if status < 10:
        return "グレード１：基本機能だけ利用できます。"
    if status < 24:
        return "グレード２：模擬試験が利用できます。"
    if status < 31:
        return "グレード３：模擬試験と修了試験が利用できます。"
    if status == 31:
        return "グレード３+：次の修了試験でもう一度70点以上を獲得すると修了です。"
    return "グレード４：修了しました。"


def enter_admin(user_id: int) -> dict[str, Any]:
    setStage(user_id, 9)
    return build_admin_home(user_id)


def build_admin_home(user_id: int) -> dict[str, Any]:
    is_admin = user_id < 4
    is_staff = user_id <= 5

    actions: List[dict[str, Any]] = [
        {"id": "history", "label": "演習履歴", "enabled": True},
        {"id": "reset_password", "label": "パスワード再設定", "enabled": True},
    ]

    if is_admin:
        actions.extend([
            {"id": "registration", "label": "ユーザ登録", "enabled": False, "message": "Coming soon in Flutter."},
            {"id": "user_list", "label": "ユーザリストの表示", "enabled": True},
        ])
    else:
        actions.append({"id": "status", "label": "ステータスの表示", "enabled": True})

    if is_staff:
        actions.extend([
            {"id": "db_questions", "label": "演習問題データ更新", "enabled": False, "message": "Web admin only."},
            {"id": "db_comments", "label": "コメントデータ更新", "enabled": False, "message": "Web admin only."},
            {"id": "db_manual", "label": "問題データメンテナンス", "enabled": False, "message": "Web admin only."},
            {"id": "db_download", "label": "演習問題ダウンロード", "enabled": False, "message": "Web admin only."},
        ])

    return {
        "user_id": user_id,
        "title": "管理画面",
        "is_admin": is_admin,
        "is_staff": is_staff,
        "actions": actions,
    }


def build_exercise_history(user_id: int) -> dict[str, Any]:
    result_list, count = getUserResultList(user_id)
    if result_list is False:
        result_list = []
        count = 0

    items = []
    for row in result_list:
        lastname, total, score, rate, start_time, exam_type, mail_adr = row
        items.append({
            "lastname": lastname,
            "email": mail_adr,
            "start_time": start_time,
            "exam_type": exam_type,
            "score": score,
            "total": total,
            "rate": rate,
            "passed": float(rate) >= 70 if rate not in ("", None) else False,
            "label": f"{lastname}({mail_adr})：{start_time}【{exam_type}】{score}/{total}[{rate}%]",
        })

    return {
        "user_id": user_id,
        "title": "演習履歴",
        "count": count,
        "items": items,
    }


def build_user_status(user_id: int, target_user_id: int) -> dict[str, Any]:
    status = getStatus(target_user_id)
    if status is False:
        status = 0

    mock_results, mock_count = getUserResultList1(target_user_id)
    final_results, final_count = getUserResultList2(target_user_id)
    if mock_results is False:
        mock_results, mock_count = [], 0
    if final_results is False:
        final_results, final_count = [], 0

    def _mock_item(row: tuple[Any, ...]) -> dict[str, Any]:
        lastname, _, total, score, rate, start_time, exam_type, mail_adr = row
        return {
            "lastname": lastname,
            "email": mail_adr,
            "start_time": start_time,
            "exam_type": exam_type,
            "score": score,
            "total": total,
            "rate": rate,
            "passed": float(rate) >= 70 if rate not in ("", None) else False,
            "label": f"{lastname}({mail_adr})：{start_time}【{exam_type}】{score}/{total}[{rate}%]",
        }

    def _final_item(row: tuple[Any, ...]) -> dict[str, Any]:
        lastname, _, rate, start_time, exam_type, mail_adr = row
        return {
            "lastname": lastname,
            "email": mail_adr,
            "start_time": start_time,
            "exam_type": exam_type,
            "rate": rate,
            "passed": float(rate) >= 75 if rate not in ("", None) else False,
            "label": f"{lastname}({mail_adr})：{start_time}【{exam_type}】",
        }

    return {
        "user_id": user_id,
        "target_user_id": target_user_id,
        "title": "現在のステータス",
        "grade": _grade_label(status),
        "status": status,
        "mock_exam_history": {
            "count": mock_count,
            "items": [_mock_item(row) for row in mock_results],
        },
        "final_exam_history": {
            "count": final_count,
            "items": [_final_item(row) for row in final_results],
        },
    }


def build_user_list(actor_user_id: int) -> dict[str, Any]:
    if actor_user_id >= 4:
        raise PermissionError("Admin access required.")

    users = getUserList()
    if users is False:
        users = []

    return {
        "user_id": actor_user_id,
        "title": "ユーザ・リスト",
        "users": [
            {
                "id": row[0],
                "lastname": row[1],
                "email": row[2],
                "label": f"{row[0]}:{row[1]}({row[2]})",
            }
            for row in users
        ],
    }


def delete_target_user(actor_user_id: int, target_user_id: int) -> dict[str, Any]:
    if actor_user_id >= 4:
        raise PermissionError("Admin access required.")
    deleteUser(target_user_id)
    return {"message": "User deleted.", "target_user_id": target_user_id}


def build_password_reset_form(user_id: int) -> dict[str, Any]:
    name = getLoginName(user_id)
    if name is False:
        raise ValueError("User not found.")

    return {
        "user_id": user_id,
        "title": "パスワード設定画面",
        "name": name,
        "is_staff": user_id <= 5,
    }


def change_password(user_id: int, old_password: str, new_password: str) -> dict[str, Any]:
    if not old_password:
        return {
            "success": False,
            "message": "現在のパスワードが入力されていない。もしくは、正しくありません。",
        }
    if not new_password:
        return {"success": False, "message": "新しいパスワードを入力してください。"}

    hashed_password = getLoginPassword(user_id)
    if not hashed_password:
        return {"success": False, "message": "エラーが発生しました。"}

    if not password_verify(old_password, hashed_password):
        return {
            "success": False,
            "message": "現在のパスワードが入力されていない。もしくは、正しくありません。",
        }

    if not setPassword(user_id, new_password):
        return {"success": False, "message": "エラーが発生しました。"}

    return {"success": True, "message": "成功しました。"}


def promote_mock_exam(actor_user_id: int, target_user_id: int) -> dict[str, Any]:
    if actor_user_id >= 4:
        raise PermissionError("Admin access required.")
    rankUp(target_user_id, 0, 0)
    return {
        "message": "模擬試験が受けられるように設定しました。",
        "target_user_id": target_user_id,
    }
