from typing import Any, List

import constant
from examDB import getCommentId, getExamlist, getQuestion
from resultDB import getComment, getResult, getStartTime, makeComments
from users import getStage, setStage


def _area_offsets() -> List[int]:
    return [
        0,
        constant.NumOfCategory1,
        constant.NumOfCategory2,
        constant.NumOfCategory3,
        constant.NumOfCategory4,
        constant.NumOfCategory5,
        constant.NumOfCategory6,
        constant.NumOfCategory7,
    ]


def _parse_question_refs(raw: str) -> List[dict[str, Any]]:
    if not raw:
        return []

    items: List[dict[str, Any]] = []
    for part in raw.split(","):
        token = part.strip()
        if not token:
            continue
        correct = not token.startswith("-")
        q_no = int(token.lstrip("-"))
        items.append({"q_no": q_no, "correct": correct})
    return items


def _build_practice2(arealist: str, resultlist: str) -> List[List[List[str]]]:
    practice2 = [
        [["", "", ""] for _ in range(constant.NumOfCategory)]
        for _ in range(constant.NumOfArea)
    ]

    for index, category_code in enumerate(arealist):
        position = constant.categoryCode.find(category_code)
        if position == -1:
            continue

        question_no = str(index + 1)
        token = question_no if resultlist[index] == "1" else f"-{question_no}"

        if position < constant.NumOfCategory1:
            area_idx, cat_idx = 0, position
        elif position < constant.NumOfCategory2:
            area_idx, cat_idx = 1, position - constant.NumOfCategory1
        elif position < constant.NumOfCategory3:
            area_idx, cat_idx = 2, position - constant.NumOfCategory2
        elif position < constant.NumOfCategory4:
            area_idx, cat_idx = 3, position - constant.NumOfCategory3
        elif position < constant.NumOfCategory5:
            area_idx, cat_idx = 4, position - constant.NumOfCategory4
        elif position < constant.NumOfCategory6:
            area_idx, cat_idx = 5, position - constant.NumOfCategory5
        elif position < constant.NumOfCategory7:
            area_idx, cat_idx = 6, position - constant.NumOfCategory6
        elif position < constant.NumOfCategory8:
            area_idx, cat_idx = 7, position - constant.NumOfCategory7
        else:
            continue

        current = practice2[area_idx][cat_idx][2]
        practice2[area_idx][cat_idx][2] = (
            f"{current},{token}" if current else token
        )

    return practice2


def _prepare_summary(
    *,
    user_id: int,
    exam_id: int,
    total: int,
    arealist: str,
    resultlist: str,
    correct: int,
    title: str,
) -> dict[str, Any]:
    stage = getStage(user_id)
    if stage < 4:
        raise PermissionError("Exam has not finished yet.")

    setStage(user_id, 5)
    stime = getStartTime(exam_id)
    rate = correct / total * 100 if total else 0
    passed = rate >= constant.PassScore1
    practice2 = _build_practice2(arealist, resultlist)
    category_number, category_score, category_percent, area_number, area_score, area_percent = \
        getResult(exam_id)

    return {
        "user_id": user_id,
        "exam_id": exam_id,
        "title": title,
        "total": total,
        "correct": correct,
        "rate": round(rate, 2),
        "passed": passed,
        "result": "合格" if passed else "不合格",
        "stime": stime,
        "arealist": arealist,
        "resultlist": resultlist,
        "practice2": practice2,
        "category_number": category_number,
        "category_score": category_score,
        "category_percent": category_percent,
        "area_number": area_number,
        "area_score": area_score,
        "area_percent": area_percent,
    }


def _format_score(score: int, total: int) -> str:
    return f"{score}/{total}"


def _format_percent(value: float, total: int) -> str:
    if total == 0:
        return "-"
    return f"{value:.1f}%"


def build_area_results(data: dict[str, Any]) -> dict[str, Any]:
    summary = _prepare_summary(
        user_id=int(data["user_id"]),
        exam_id=int(data["exam_id"]),
        total=int(data["total"]),
        arealist=str(data.get("arealist", "")),
        resultlist=str(data.get("resultlist", "")),
        correct=int(data["correct"]),
        title=str(data.get("title", "")),
    )

    offsets = _area_offsets()
    areas: List[dict[str, Any]] = []

    for area_idx in range(constant.NumOfArea):
        chapter_count = int(constant.areaname[area_idx][1])
        chapters: List[dict[str, Any]] = []

        for chapter_idx in range(chapter_count):
            global_idx = offsets[area_idx] + chapter_idx
            chapters.append({
                "label": constant.practice[area_idx][chapter_idx],
                "score_label": _format_score(
                    summary["category_score"][global_idx],
                    summary["category_number"][global_idx],
                ),
                "percent_label": _format_percent(
                    summary["category_percent"][global_idx],
                    summary["category_number"][global_idx],
                ),
                "questions": _parse_question_refs(
                    summary["practice2"][area_idx][chapter_idx][2]
                ),
            })

        areas.append({
            "label": constant.areaname[area_idx][0],
            "score_label": _format_score(
                summary["area_score"][area_idx],
                summary["area_number"][area_idx],
            ),
            "percent_label": _format_percent(
                summary["area_percent"][area_idx],
                summary["area_number"][area_idx],
            ),
            "chapters": chapters,
        })

    return {
        "view": "area_results",
        "title": f"{summary['title']}（領域ごとの結果）",
        **summary,
        "areas": areas,
    }


def build_comments_analysis(data: dict[str, Any]) -> dict[str, Any]:
    summary = _prepare_summary(
        user_id=int(data["user_id"]),
        exam_id=int(data["exam_id"]),
        total=int(data["total"]),
        arealist=str(data.get("arealist", "")),
        resultlist=str(data.get("resultlist", "")),
        correct=int(data["correct"]),
        title=str(data.get("title", "")),
    )
    comments = makeComments(int(data["exam_id"]))

    return {
        "view": "comments",
        "title": f"{summary['title']}（分析結果）",
        **summary,
        "comments_html": comments,
    }


def build_question_analysis(data: dict[str, Any]) -> dict[str, Any]:
    user_id = int(data["user_id"])
    exam_id = int(data["exam_id"])
    total = int(data["total"])
    correct = int(data["correct"])
    title = str(data.get("title", ""))
    q_no = int(data["q_no"])
    stime = data.get("stime") or getStartTime(exam_id)
    arealist = str(data.get("arealist", ""))
    resultlist = str(data.get("resultlist", ""))

    stage = getStage(user_id)
    if stage < 4:
        raise PermissionError("Exam has not finished yet.")
    if stage < 5:
        setStage(user_id, 5)

    examlist, _, answerlist = getExamlist(exam_id)
    question, _, _ = getQuestion(examlist, q_no)
    answers = "ABCD"
    correct_answer = answers[question.crct]
    user_answer = int(answerlist[q_no - 1]) if answerlist[q_no - 1].isdigit() else 0
    comment_id = getCommentId(examlist, q_no, question.crct + 1, user_answer)
    comment = getComment(comment_id)
    rate = correct / total * 100 if total else 0
    passed = rate >= constant.PassScore1

    return {
        "view": "question_analysis",
        "title": f"{title}（問題解説）",
        "user_id": user_id,
        "exam_id": exam_id,
        "total": total,
        "correct": correct,
        "rate": round(rate, 2),
        "result": "合格" if passed else "不合格",
        "stime": stime,
        "arealist": arealist,
        "resultlist": resultlist,
        "q_no": q_no,
        "question": question.q,
        "selection1": question.a1,
        "selection2": question.a2,
        "selection3": question.a3,
        "selection4": question.a4,
        "correct_answer": correct_answer,
        "comment_html": comment,
    }


def return_to_main_menu(user_id: int) -> dict[str, Any]:
    setStage(user_id, 1)
    return {"message": "Returned to main menu.", "user_id": user_id}
