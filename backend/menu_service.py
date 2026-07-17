from typing import Any

from users import getStatus, getLoginName


def _mock_exam_message(status: int) -> str:
    if status < 10:
        return "模擬試験には、まだ挑戦できません。"
    if status >= 30:
        return "模擬試験で５回以上、合格することができました。修了試験に挑戦することができます。"
    return "模擬試験に挑戦できるようになりました。"


def _final_exam_message(status: int) -> str:
    if status < 30:
        return "修了試験には、まだ挑戦できません。模擬試験に少なくとも5回合格が必要です。"
    if status == 30:
        return "修了試験に挑戦できるようになりました。２回連続で合格すると修了です。"
    if status == 31:
        return "合格することができました。連続してもう一度、合格すると修了です。"
    return "おめでとうございます。修了しました。"


def build_main_menu(user_id: int) -> dict[str, Any]:
    status = getStatus(user_id)
    if status is False:
        status = 0

    email = getLoginName(user_id)
    if email is False:
        email = ""

    return {
        "user_id": user_id,
        "email": email,
        "status": status,
        "title": "メインメニュー",
        "sections": [
            {
                "id": "single_question",
                "title": "一問一答",
                "items": [
                    _item(91, "makeExam3", "組織と人材", "時間:2分15秒 / 1問", "#A46892"),
                    _item(92, "makeExam3", "情報と技術", "時間:2分15秒 / 1問", "#7DA7D3"),
                    _item(93, "makeExam3", "サービスバリュー・ストリーム", "時間:2分15秒 / 1問", "#51CBCA"),
                    _item(94, "makeExam3", "活動調整と調達", "時間:2分15秒 / 1問", "#D065A2"),
                ],
            },
            {
                "id": "area_quiz",
                "title": "分野別確認問題",
                "items": [
                    _item(10, "makeExam", "組織と人材【5問】", "時間:11分15秒", "#642852"),
                    _item(20, "makeExam", "情報と技術【5問】", "時間:11分15秒", "#3D6793"),
                    _item(30, "makeExam", "サービスバリュー・ストリーム【5問】", "時間:11分15秒", "#219B9A"),
                    _item(40, "makeExam", "活動調整と調達【5問】", "時間:11分15秒", "#902562"),
                    _item(60, "makeExam", "全領域から【10問】", "時間:22分30秒", "#60B719"),
                ],
            },
            {
                "id": "mock_exam",
                "title": "模擬試験",
                "message": _mock_exam_message(status),
                "items": [
                    _item(
                        70,
                        "makeExam",
                        "模擬試験【40問】",
                        "時間：1時間30分",
                        "#A0A0A0",
                        enabled=status >= 10,
                    ),
                ],
            },
            {
                "id": "final_exam",
                "title": "修了試験",
                "message": _final_exam_message(status),
                "items": [
                    _item(
                        80,
                        "makeExam",
                        "修了試験【40問】",
                        "時間：1時間30分",
                        "#D4AF37",
                        enabled=status >= 30,
                    ),
                ],
            },
        ],
        "actions": [
            {
                "id": "admin",
                "label": "管理画面",
                "action": "makeExam",
                "category": 99,
                "enabled": True,
            },
            {
                "id": "logout",
                "label": "ログアウト",
                "action": "logout",
                "enabled": True,
            },
        ],
    }


def _item(
    category: int,
    action: str,
    label: str,
    subtitle: str,
    color: str,
    *,
    enabled: bool = True,
) -> dict[str, Any]:
    return {
        "category": category,
        "action": action,
        "label": label,
        "subtitle": subtitle,
        "color": color,
        "enabled": enabled,
    }
