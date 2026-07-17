import datetime
import sqlite3
from typing import Any, Optional, Tuple

from constant import (
    DIFF_JST_FROM_UTC,
    FAIL_MESSAGE,
    PASS1_MASSAGE,
    PASS2_MASSAGE,
    PassScore1,
    PassScore2,
    db_path,
    examTitle1,
    examTitle10,
    examTitle11,
    examTitle12,
    examTitle2,
    examTitle3,
    examTitle4,
)
from examDB import getCorrectList, getQuestion, makeExam2, saveExam
from mail import sendMail
from resultDB import putResult
from users import getMailadress, getStage, getStatus, rankDown, rankUp, setStage


def _category_config(category: int) -> Optional[Tuple[int, str]]:
    mapping = {
        10: (5, examTitle1),
        20: (5, examTitle2),
        30: (5, examTitle3),
        40: (5, examTitle4),
        60: (10, examTitle10),
        70: (40, examTitle11),
        80: (40, examTitle12),
    }
    return mapping.get(category)


def _init_lists(total: int) -> tuple[str, str]:
    return "0" * total, "0" * total


def _question_payload(
    *,
    user_id: int,
    exam_id: int,
    title: str,
    total: int,
    examlist: str,
    arealist: str,
    q_no: int,
    marklist: str,
    answerlist: str,
    time_min: int,
    time_sec: int,
) -> dict[str, Any]:
    question = getQuestion(examlist, q_no)
    selected = int(answerlist[q_no - 1]) if answerlist[q_no - 1].isdigit() else 0

    return {
        "finished": False,
        "user_id": user_id,
        "exam_id": exam_id,
        "title": title,
        "total": total,
        "q_no": q_no,
        "examlist": examlist,
        "arealist": arealist,
        "question": question.q,
        "selection1": question.a1,
        "selection2": question.a2,
        "selection3": question.a3,
        "selection4": question.a4,
        "marklist": marklist,
        "answerlist": answerlist,
        "selected_answer": selected,
        "time_min": time_min,
        "time_sec": time_sec,
        "can_go_back": q_no > 1,
        "can_go_forward": q_no < total,
        "time_limit_seconds": total * 135,
    }


def start_exam(user_id: int, category: int) -> dict[str, Any]:
    config = _category_config(category)
    if config is None:
        raise ValueError("Unsupported exam category.")

    amount, title = config
    stage = getStage(user_id)
    if stage == 1:
        setStage(user_id, 2)

    examlist, arealist = makeExam2(user_id, amount, category, 1, 900, "")
    exam_id = saveExam(user_id, str(category), 1, amount, examlist, arealist)
    marklist, answerlist = _init_lists(amount)

    return _begin_exercise(
        user_id=user_id,
        exam_id=exam_id,
        title=title,
        total=amount,
        examlist=examlist,
        arealist=arealist,
        marklist=marklist,
        answerlist=answerlist,
    )


def _begin_exercise(
    *,
    user_id: int,
    exam_id: int,
    title: str,
    total: int,
    examlist: str,
    arealist: str,
    marklist: str,
    answerlist: str,
) -> dict[str, Any]:
    stage = getStage(user_id)
    if stage not in (2, 3, 4):
        raise PermissionError("Invalid exam stage.")
    if stage == 2:
        setStage(user_id, 3)
    if stage == 4:
        raise PermissionError("Exam already finished. Please log in again.")

    if datetime.datetime.now().tzinfo is None and __import__("os").name != "nt":
        now = datetime.datetime.now() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
    else:
        now = datetime.datetime.now()

    stime = now.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE EXAM_TABLE SET START_TIME = ? WHERE EXAM_ID = ?',
        (stime, exam_id),
    )
    conn.commit()
    conn.close()

    return _question_payload(
        user_id=user_id,
        exam_id=exam_id,
        title=title,
        total=total,
        examlist=examlist,
        arealist=arealist,
        q_no=1,
        marklist=marklist,
        answerlist=answerlist,
        time_min=0,
        time_sec=0,
    )


def _apply_selection(answerlist: str, q_no: int, selection: Optional[int]) -> str:
    if selection is None or selection < 1 or selection > 4:
        return answerlist
    index = q_no - 1
    return answerlist[:index] + str(selection) + answerlist[index + 1:]


def _toggle_mark(marklist: str, q_no: int) -> str:
    index = q_no - 1
    current = marklist[index]
    new_value = "0" if current == "1" else "1"
    return marklist[:index] + new_value + marklist[index + 1:]


def process_exercise(data: dict[str, Any]) -> dict[str, Any]:
    command = data.get("command", "")
    user_id = int(data["user_id"])
    exam_id = int(data["exam_id"])
    title = data.get("title", "")
    total = int(data["total"])
    examlist = data.get("examlist", "")
    arealist = data.get("arealist", "")
    q_no = int(data.get("q_no", 1))
    marklist = data.get("marklist", "0" * total)
    answerlist = data.get("answerlist", "0" * total)
    time_min = int(data.get("time_min", 0))
    time_sec = int(data.get("time_sec", 0))
    selection = data.get("selected_answer")

    stage = getStage(user_id)
    if stage not in (2, 3, 4):
        raise PermissionError("Invalid exam stage.")
    if stage == 4 and command != "finish":
        raise PermissionError("Exam already finished. Please log in again.")

    if command == "mark":
        mark_q = int(data.get("target_q_no", q_no))
        marklist = _toggle_mark(marklist, mark_q)
        return _question_payload(
            user_id=user_id,
            exam_id=exam_id,
            title=title,
            total=total,
            examlist=examlist,
            arealist=arealist,
            q_no=q_no,
            marklist=marklist,
            answerlist=answerlist,
            time_min=time_min,
            time_sec=time_sec,
        )

    if command in {"next", "previous", "move", "finish", "timeout"}:
        answerlist = _apply_selection(answerlist, q_no, selection)

    if command == "next":
        q_no = min(q_no + 1, total)
    elif command == "previous":
        q_no = max(q_no - 1, 1)
    elif command == "move":
        q_no = int(data.get("target_q_no", q_no))
        q_no = max(1, min(q_no, total))
    elif command in {"finish", "timeout"}:
        return _finish_exercise(
            user_id=user_id,
            exam_id=exam_id,
            title=title,
            total=total,
            examlist=examlist,
            arealist=arealist,
            answerlist=answerlist,
            time_min=time_min,
            time_sec=time_sec,
        )

    return _question_payload(
        user_id=user_id,
        exam_id=exam_id,
        title=title,
        total=total,
        examlist=examlist,
        arealist=arealist,
        q_no=q_no,
        marklist=marklist,
        answerlist=answerlist,
        time_min=time_min,
        time_sec=time_sec,
    )


def _finish_exercise(
    *,
    user_id: int,
    exam_id: int,
    title: str,
    total: int,
    examlist: str,
    arealist: str,
    answerlist: str,
    time_min: int,
    time_sec: int,
) -> dict[str, Any]:
    setStage(user_id, 4)
    correctlist = getCorrectList(examlist)
    correct = 0
    resultlist = ""
    for index, answer in enumerate(answerlist):
        if answer == correctlist[index]:
            correct += 1
            resultlist += "1"
        else:
            resultlist += "0"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    rate = round((correct / total * 100), 1)
    used_time = int(time_sec) + int(time_min) * 60
    total_time = total * 90
    cursor.execute(
        "UPDATE EXAM_TABLE SET RESULTLIST = ?, SCORE = ?, USED_TIME = ?, "
        "TOTAL_TIME = ?, RATE = ? WHERE EXAM_ID = ?",
        (resultlist, correct, used_time, total_time, rate, exam_id),
    )
    cursor.execute(
        "SELECT START_TIME, EXAM_TYPE FROM EXAM_TABLE WHERE EXAM_ID = ?",
        (exam_id,),
    )
    row = cursor.fetchone()
    exam_type = row[1] if row else ""
    conn.commit()
    conn.close()

    putResult(user_id, exam_id, total, arealist, answerlist, resultlist, correct, rate, used_time)

    old_status = getStatus(user_id)
    flag = 0
    if rate >= PassScore2 and total == 40:
        _, flag = rankUp(user_id, 2, exam_type)
    elif rate >= PassScore1 and total == 40:
        _, flag = rankUp(user_id, 1, exam_type)

    if old_status == 31 and exam_type == "修了試験(40問)" and rate < PassScore2:
        rankDown(user_id)
        flag = 4

    message = f"Correct: {correct}/{total} ({rate}%)"
    if old_status >= 30 and exam_type == "修了試験(40問)":
        if rate < PassScore2:
            message = FAIL_MESSAGE if old_status < 40 else "不合格でした。"
        elif old_status == 30:
            message = PASS1_MASSAGE
        elif old_status == 31:
            message = PASS2_MASSAGE
            user_info = getMailadress(user_id)
            if user_info:
                username = f"{user_info[0][0]} {user_info[0][1]}"
                sendMail(username, str(user_info[0][2]), "合格です。")
        else:
            message = "合格です。おめでとうございます。"

    return {
        "finished": True,
        "user_id": user_id,
        "exam_id": exam_id,
        "title": title,
        "total": total,
        "correct": correct,
        "rate": rate,
        "resultlist": resultlist,
        "answerlist": answerlist,
        "message": message,
        "flag": flag,
    }
