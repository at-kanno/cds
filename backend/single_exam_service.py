import sqlite3
from types import SimpleNamespace
from typing import Any

from audio_support import get_audio_play_info, get_choice_audio_info
from config_loader import get_areas, get_exam_entry
from constant import db_path
from examDB import getQuestionFromCategory, getQuestionFromNum
from image_support import get_image_info
from users import getStage, setStage


def _media_payloads(num, db_category: int, permutation) -> dict[str, Any]:
    stub = SimpleNamespace(
        number=int(num),
        category=int(db_category),
        permutation=permutation,
        flag=0,
    )
    choice = get_choice_audio_info(stub)
    audio = get_audio_play_info(stub)
    image = get_image_info(stub)
    payload: dict[str, Any] = {
        "audio": None,
        "choice_audio": None,
        "image": None,
    }
    if audio:
        payload["audio"] = {
            "filename": audio["filename"],
            "url": f"/audio/{audio['filename']}",
            "max_audio_plays": audio["max_audio_plays"],
        }
    if choice:
        payload["choice_audio"] = {
            "choices": {
                letter: {"filename": filename, "url": f"/audio/{filename}"}
                for letter, filename in choice["choices"].items()
            },
            "max_audio_plays": choice["max_audio_plays"],
        }
    if image:
        payload["image"] = {
            "filename": image["filename"],
            "url": f"/image/{image['filename']}",
        }
    return payload


def _question_response(
    *,
    user_id: int,
    category: int,
    area: str,
    question: str,
    selection1: str,
    selection2: str,
    selection3: str,
    selection4: str,
    crct: int,
    cid: int,
    num: str,
    permutation: str,
    time_limit_seconds: int,
    choice_count: int = 4,
    db_category: int | None = None,
) -> dict[str, Any]:
    media = _media_payloads(num, db_category if db_category is not None else category, permutation)
    if media.get("choice_audio"):
        selection1 = selection2 = selection3 = selection4 = ""
    return {
        "mode": "single",
        "user_id": user_id,
        "category": category,
        "area": area,
        "title": f"{area}：一問一答（問題）",
        "question": question,
        "selection1": selection1,
        "selection2": selection2,
        "selection3": selection3,
        "selection4": selection4,
        "choice_count": choice_count,
        "crct": crct,
        "cid": cid,
        "num": str(num),
        "permutation": str(permutation),
        "time_limit_seconds": time_limit_seconds,
        **media,
    }


def start_single_exam(user_id: int, category: int) -> dict[str, Any]:
    entry = get_exam_entry(category)
    if entry is None or entry.get("mode") != "single":
        raise ValueError("Unsupported single-question category.")

    category_range = entry.get("category_range")
    if not category_range or len(category_range) != 2:
        raise ValueError("Single-question category is missing category_range.")

    area_index = entry.get("area_index", 0)
    areas = get_areas()
    if area_index >= len(areas):
        raise ValueError("Single-question category has invalid area_index.")

    area = areas[area_index]["abbrev"]
    time_limit = int(entry.get("time_limit_seconds", 135))

    stage = getStage(user_id)
    if stage == 1:
        setStage(user_id, 2)

    start, end = int(category_range[0]), int(category_range[1])
    result = getQuestionFromCategory(start, end)
    if result is False or not isinstance(result, tuple):
        raise ValueError("No questions available for this category.")

    question, a1, a2, a3, a4, crct, cid, num, permutation, choice_count, _prompt = result
    return _question_response(
        user_id=user_id,
        category=category,
        area=area,
        question=question,
        selection1=a1,
        selection2=a2,
        selection3=a3,
        selection4=a4,
        crct=crct,
        cid=cid,
        num=num,
        permutation=permutation,
        time_limit_seconds=time_limit,
        choice_count=choice_count,
        db_category=start,
    )


def check_single_answer(
    *,
    user_id: int,
    category: int,
    area: str,
    crct: int,
    num: str,
    permutation: str,
    cid: int,
    answer: int,
) -> dict[str, Any]:
    if answer == 9:
        result_message = "選択がなされませんでした。"
    elif answer - 1 == crct:
        result_message = "正解です。"
    else:
        result_message = "誤りです。"

    fetched = getQuestionFromNum(num, permutation)
    if fetched is False:
        raise ValueError("Question not found.")

    question, a1, a2, a3, a4, cid0, cid1, cid2, cid3, prompt_text, conn, _cursor = fetched
    if answer != 9 and 1 <= answer <= 4:
        comment_id = [cid0, cid1, cid2, cid3][answer - 1]
    else:
        comment_id = cid

    db_conn = sqlite3.connect(db_path)
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT COMMENT FROM COMMENTS_TABLE WHERE COMMENT_ID = ?",
        (comment_id,),
    )
    row = cursor.fetchone()
    db_conn.close()
    conn.close()
    comment = row[0] if row else ""

    entry = get_exam_entry(int(category))
    db_category = int(entry["category_range"][0]) if entry and entry.get("category_range") else int(category)
    media = _media_payloads(num, db_category, permutation)

    return {
        "mode": "single_result",
        "user_id": user_id,
        "category": category,
        "area": area,
        "title": f"{area}：一問一答（解説）",
        "result_message": result_message,
        "correct_answer": "ABCD"[crct],
        "question": question,
        "selection1": a1,
        "selection2": a2,
        "selection3": a3,
        "selection4": a4,
        "prompt_text": prompt_text,
        "choice_count": sum(1 for text in (a1, a2, a3, a4) if text),
        "comment": comment,
        **media,
    }
