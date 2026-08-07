from constant import db_path, abbreviation
import constant
from flask import Flask, session, render_template, request, Blueprint
import sqlite3, os
from types import SimpleNamespace
from users import getStage, setStage, getStatus, getPrivilege
from examDB import makeExam2, getQuestionFromCategory, getQuestionFromNum, saveExam, getCorrectList
from config_loader import get_exam_entry
from exercise import _media_template_kwargs


def _single_question_media(num, category, permutation, *, enforce_play_limit: bool = True) -> dict:
    """Build image / choice-audio kwargs for 一問一答 (permutation-aware)."""
    db_category = None
    flag = 0
    try:
        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT CATEGORY, FLAG FROM knowledge_base WHERE NUMBER = ?",
            (int(num),),
        ).fetchone()
        conn.close()
        if row:
            db_category = int(row[0])
            try:
                flag = int(row[1] or 0)
            except (TypeError, ValueError):
                flag = 0
    except Exception:
        pass
    if db_category is None:
        entry = get_exam_entry(int(category)) if str(category).isdigit() else None
        if entry and entry.get("category_range"):
            db_category = int(entry["category_range"][0])
        else:
            db_category = int(category) if str(category).isdigit() else 0
    stub = SimpleNamespace(
        number=int(num),
        category=db_category,
        permutation=permutation,
        flag=flag,
    )
    # 一問一答: every question can play set audio; no multi-exam set navigation notes.
    return _media_template_kwargs(
        stub,
        enforce_play_limit=enforce_play_limit,
        hide_set_follow_up=False,
        show_set_note=False,
    )


def _multi_exam_settings(
    category: str,
    default_amount: int,
    default_title: str,
    default_time: int,
) -> tuple[int, str, int]:
    entry = get_exam_entry(int(category))
    if entry is None:
        return default_amount, default_title, default_time
    amount = int(entry.get("amount", default_amount))
    title = entry.get("title", default_title)
    time_limit = int(entry.get("time_limit_seconds", default_time))
    return amount, title, time_limit


def _run_make_exam(
    user_id,
    category: str,
    level: int,
    default_amount: int,
    default_title: str,
    default_time: int,
):
    amount, title, time_limit = _multi_exam_settings(
        category, default_amount, default_title, default_time
    )
    result = makeExam2(user_id, amount, int(category), level, time_limit, "")
    if result is None:
        return None
    examlist, arealist = result
    return amount, title, examlist, arealist


def _login_path() -> str:
    prefix = request.script_root.rstrip("/")
    return f"{prefix}/" if prefix else "/"


exam_module = Blueprint("exam", __name__, static_folder='./static')


@exam_module.route("/submenu", methods=["POST"])
def open_submenu():
    """HTML 2-level menu: show a submenu section with the same admin/logout actions."""
    from menu_service import build_main_menu

    user_id = request.form.get("user_id")
    submenu_key = request.form.get("submenu") or ""
    menu = build_main_menu(int(user_id))
    section = (menu.get("submenus") or {}).get(submenu_key)
    if not section:
        return render_template(
            "error.html",
            user_id=user_id,
            error_message=f"サブメニューが見つかりません: {submenu_key}",
        )

    sub_menu = {
        "title": section.get("title") or submenu_key,
        "sections": [section],
        "actions": menu.get("actions", []),
        "hierarchy": False,
    }
    return render_template(
        "main-menu.html",
        user_id=int(user_id),
        status=menu.get("status", 0),
        menu=sub_menu,
        show_back_to_main=True,
    )


@exam_module.route("/mainMenu", methods=["POST"])
def main_menu_page():
    from menu_view import render_main_menu_page

    user_id = request.form.get("user_id")
    return render_main_menu_page(user_id)


# 基本概念を選択
@exam_module.route('/makeExam', methods=['POST'])
def makeExam():
    user_id = request.form.get('user_id')
    stage = getStage(user_id)
    #    if(stage != 1 and stage !=2):
    #        return """
    #        <h1>異常を検出しました。<br>
    #        ログインし直してください。</h1>
    #        <p><a href="{_login_path()}">→ログインする</a></p>
    #        """
    if (stage == 1):
        setStage(user_id, 2)

    if not is_login():
        return f"""
        <h1>ログインしてください</h1>
        <p><a href="{_login_path()}">→ログインする</a></p>
        """
    if request.method == 'POST':
        category = request.form['category']
        print('category=' + str(category))

        level = 1
        if (category == constant.examEntry):
            from menu_view import render_main_menu_page
            return render_main_menu_page(user_id)
        elif (category == constant.examEntry10):
            exam_data = _run_make_exam(
                user_id, category, level, 10, constant.examTitle10,
                constant.NumOfQuestions2 * constant.TimePerQuestion,
            )
        elif (category == constant.examEntry11):
            exam_data = _run_make_exam(
                user_id, category, level, constant.MaxQuestions, constant.examTitle11,
                constant.MaxQuestions * constant.TimePerQuestion,
            )
        elif (category == constant.examEntry12):
            exam_data = _run_make_exam(
                user_id, category, level, constant.MaxQuestions, constant.examTitle12,
                constant.MaxQuestions * constant.TimePerQuestion,
            )
        elif (category == constant.examEntry1):
            exam_data = _run_make_exam(
                user_id, category, level, 5, constant.examTitle1,
                constant.NumOfQuestions1 * constant.TimePerQuestion,
            )
        elif (category == constant.examEntry2):
            exam_data = _run_make_exam(
                user_id, category, level, 5, constant.examTitle2,
                constant.NumOfQuestions1 * constant.TimePerQuestion,
            )
        elif (category == constant.examEntry3):
            exam_data = _run_make_exam(
                user_id, category, level, 5, constant.examTitle3,
                constant.NumOfQuestions1 * constant.TimePerQuestion,
            )
        elif (category == constant.examEntry4):
            exam_data = _run_make_exam(
                user_id, category, level, 5, constant.examTitle4,
                constant.NumOfQuestions1 * constant.TimePerQuestion,
            )
        elif (category == constant.examEntry5):
            exam_data = _run_make_exam(
                user_id, category, level, 5, constant.examTitle5,
                constant.NumOfQuestions1 * constant.TimePerQuestion,
            )
        elif category == constant.examEntry1s or category == constant.examEntry2s or \
            category == constant.examEntry3s or category == constant.examEntry4s or \
            category == constant.examEntry5s:
            exam_data = _run_make_exam(
                user_id, category, level, 5, "", constant.TimePerQuestion,
            )
        else:
            entry = get_exam_entry(int(category))
            if entry and entry.get("mode") == "multi":
                default_amount = int(entry.get("amount", 5))
                default_title = entry.get("title", "")
                default_time = int(
                    entry.get(
                        "time_limit_seconds",
                        default_amount * constant.TimePerQuestion,
                    )
                )
                exam_data = _run_make_exam(
                    user_id, category, level, default_amount, default_title, default_time,
                )
            else:
                setStage(user_id, 9)
                priv = getPrivilege(user_id)
                return render_template('admin.html',
                                       user_id=int(user_id),
                                       priv=priv,
                                       )
        if exam_data is None:
            return render_template(
                'error3.html',
                error_message='問題データを作成できませんでした。設定または問題DBを確認してください。',
            )
        amount, title, examlist, arealist = exam_data
        try:
            exam_id = saveExam(user_id, category, level, amount, examlist, arealist)
            # for debug
            correctlist = getCorrectList(examlist)
            return render_template('startExam.html',
                                   user_id=user_id,
                                   exam_id=exam_id,
                                   total=amount,
                                   examlist=examlist,
                                   arealist=arealist,
                                   title=title,
                                   correctlist=correctlist,
                                   )
        except:
            return "Error...."
    else:
        return 'Fail'


# 基本概念を選択
@exam_module.route('/makeExam3', methods=['POST'])
def makeExam3():

    user_id = request.form.get('user_id')
    command = request.form.get('command')

    if command == 'exit':
        from menu_view import render_main_menu_page
        return render_main_menu_page(user_id)

    category = request.form['category']
    cidx = ['' for i in range(4)]

    if command == 'check' or command == 'timeout':
        crct = int(request.form.get('crct'))
        num = request.form.get('num')
        ans = int(request.form.get('answer'))
        cid = request.form.get('cid')
        permutation = request.form.get('permutation')
        if ans == 9:
            correct = '選択がなされませんでした。'
        elif ans - 1 == crct:
            correct = '正解です。'
        else:
            correct = '誤りです。'

        q, a1, a2, a3, a4, cidx[0], cidx[1], cidx[2], cidx[3], prompt_text, conn, c = (
            getQuestionFromNum(num, permutation)
        )

        if ans != 9:
            cid = cidx[ans-1]

        sql = "SELECT  COMMENT FROM COMMENTS_TABLE" \
              + " WHERE COMMENT_ID = " + str(cid) + ";"
        try:
            if c.execute(sql):
                print("Success!")
            else:
                print("Error!")
        except:
            print("Error!")
        items = c.fetchall()
        try:
            comment = items[0][0]
        except:
            return render_template('error3.html',
                                   error_message='該当するコメントがありませんでした'
                                   )

        area = request.form.get('area')
        media = _single_question_media(
            num, category, permutation, enforce_play_limit=False
        )
        return render_template('analysis2.html',
                               user_id=user_id,
                               q=q,
                               a1=a1,
                               a2=a2,
                               a3=a3,
                               a4=a4,
                               prompt_text=prompt_text,
                               choice_count=sum(1 for text in (a1, a2, a3, a4) if text),
                               correct=correct,
                               comment=comment,
                               answer="ABCD"[crct],
                               category=category,
                               area=area,
                               subject=constant.SUBJECT,
                               **media,
                               )
    else:
        stage = getStage(user_id)
        if (stage == 1):
            setStage(user_id, 2)

        if not is_login():
            return f"""
            <h1>ログインしてください</h1>
            <p><a href="{_login_path()}">→ログインする</a></p>
            """

        #        category = request.form['category']
        print('category=' + str(category))

# １問１答の処理（91:FND,92:CDS,93:DSV,94:HVIT,95:DPI）
        entry = get_exam_entry(int(category))
        if entry and entry.get("category_range"):
            start, end = entry["category_range"]
            q, a1, a2, a3, a4, crct, cid, num, permutation, choice_count, _prompt = \
                getQuestionFromCategory(int(start), int(end))
        elif (category == '91'):
            q, a1, a2, a3, a4, crct, cid, num, permutation, choice_count, _prompt = \
                getQuestionFromCategory(11, 19)
        elif (category == '92'):
            q, a1, a2, a3, a4, crct, cid, num, permutation, choice_count, _prompt = \
                getQuestionFromCategory(21, 29)
        elif (category == '93'):
            q, a1, a2, a3, a4, crct, cid, num, permutation, choice_count, _prompt = \
                getQuestionFromCategory(31, 39)
        elif (category == '94'):
            q, a1, a2, a3, a4, crct, cid, num, permutation, choice_count, _prompt = \
                getQuestionFromCategory(41, 49)
        else:
            setStage(user_id, 1)
            from menu_view import render_main_menu_page
            return render_main_menu_page(user_id)

    n = int(category) - 91
    time_limit_seconds = 90
    if entry and entry.get("time_limit_seconds") is not None:
        time_limit_seconds = int(entry["time_limit_seconds"])
    elif getattr(constant, "TimePerQuestion", None):
        time_limit_seconds = int(constant.TimePerQuestion)

    return render_template('exercise2.html',
                           user_id=user_id,
                           question=q,
                           selection1=a1,
                           selection2=a2,
                           selection3=a3,
                           selection4=a4,
                           choice_count=choice_count,
                           timeMin=0,
                           timeSec=0,
                           time_limit_seconds=time_limit_seconds,
                           selectStr="",
                           crct=crct,
                           cid=cid,
                           num=num,
                           permutation=permutation,
                           category=category,
                           area=abbreviation[n], # 領域（エリア）名：constant.pyで定義subject = constant.SUBJECT,
                           subject = constant.SUBJECT,
                           **_single_question_media(num, category, permutation),
    )

# ログインしているか調べる
@exam_module.route('/is_login')
def is_login():
    if 'login' in session:
        return "on"
    else:
        return "off"
    return 'login' in session