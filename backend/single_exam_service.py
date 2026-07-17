import sqlite3
from typing import Any, Optional, Tuple

from constant import abbreviation, db_path
from examDB import getQuestionFromCategory, getQuestionFromNum
from users import getStage, setStage


def _category_range(category: int) -> Optional[Tuple[int, int, str]]:
    mapping = {
        91: (11, 19, abbreviation[0]),
        92: (21, 29, abbreviation[1]),
        93: (31, 39, abbreviation[2]),
        94: (41, 49, abbreviation[3]),
    }
    return mapping.get(category)


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
) -> dict[str, Any]:
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
        "crct": crct,
        "cid": cid,
        "num": str(num),
        "permutation": str(permutation),
        "time_limit_seconds": 135,
    }


def start_single_exam(user_id: int, category: int) -> dict[str, Any]:
    config = _category_range(category)
    if config is None:
        raise ValueError("Unsupported single-question category.")

    stage = getStage(user_id)
    if stage == 1:
        setStage(user_id, 2)

    start, end, area = config
    result = getQuestionFromCategory(start, end)
    if result is False:
        raise ValueError("No questions available for this category.")

    question, a1, a2, a3, a4, crct, cid, num, permutation = result
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

    question, a1, a2, a3, a4, comment_id = getQuestionFromNum(num, permutation)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COMMENT FROM COMMENTS_TABLE WHERE COMMENT_ID = ?",
        (comment_id if comment_id else cid,),
    )
    row = cursor.fetchone()
    conn.close()
    comment = row[0] if row else ""

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
        "comment": comment,
    }
