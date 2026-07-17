from constant import db_path, abbreviation
import constant
from flask import Flask, session, render_template, request, Blueprint
import sqlite3, os
from users import getStage, setStage, getStatus, getPrivilege
from examDB import makeExam2, getQuestionFromCategory, getQuestionFromNum, saveExam, getCorrectList

exam_module = Blueprint("exam", __name__, static_folder='./static')

# 基本概念を選択
@exam_module.route('/makeExam', methods=['POST'])
def makeExam():
    user_id = request.form.get('user_id')
    stage = getStage(user_id)
    #    if(stage != 1 and stage !=2):
    #        return """
    #        <h1>異常を検出しました。<br>
    #        ログインし直してください。</h1>
    #        <p><a href="/">→ログインする</a></p>
    #        """
    if (stage == 1):
        setStage(user_id, 2)

    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/">→ログインする</a></p>
        """
    if request.method == 'POST':
        category = request.form['category']
        print('category=' + str(category))

        level = 1
        if (category == constant.examEntry):
            status = getStatus(user_id)
            return render_template('main-menu.html',
                                   user_id=user_id,
                                   status=status,
                                   )
        elif (category == constant.examEntry10):
            amount = 10
            title = constant.examTitle10
            examlist, arealist = makeExam2(user_id, amount, int(category), level,
                    constant.NumOfQuestions2 * constant.TimePerQuestion, '')
        elif (category == constant.examEntry11):
            amount = constant.MaxQuestions
            title = constant.examTitle11
            examlist, arealist = makeExam2(user_id, amount, int(category), level,
                    constant.MaxQuestions * constant.TimePerQuestion, '')
        elif (category == constant.examEntry12):
            amount = constant.MaxQuestions
            title = constant.examTitle12
            examlist, arealist = makeExam2(user_id, amount, int(category), level,
                    constant.MaxQuestions * constant.TimePerQuestion, '')
        elif (category == constant.examEntry1):
            amount = 5
            title = constant.examTitle1
            examlist, arealist = makeExam2(user_id, amount, int(category), level,
                    constant.NumOfQuestions1 * constant.TimePerQuestion, '')
        elif (category == constant.examEntry2):
            amount = 5
            title = constant.examTitle2
            examlist, arealist = makeExam2(user_id, amount, int(category), level,
                    constant.NumOfQuestions1 * constant.TimePerQuestion, '')
        elif (category == constant.examEntry3):
            amount = 5
            title = constant.examTitle3
            examlist, arealist = makeExam2(user_id, amount, int(category), level,
                    constant.NumOfQuestions1 * constant.TimePerQuestion, '')
        elif (category == constant.examEntry4):
            amount = 5
            title = constant.examTitle4
            examlist, arealist = makeExam2(user_id, amount, int(category), level,
                    constant.NumOfQuestions1 * constant.TimePerQuestion, '')
        elif (category == constant.examEntry5):
            amount = 5
            title = constant.examTitle5
            examlist, arealist = makeExam2(user_id, amount, int(category), level,
                    constant.NumOfQuestions1 * constant.TimePerQuestion, '')
        elif category == constant.examEntry1s or category == constant.examEntry2s or \
            category == constant.examEntry3s or category == constant.examEntry4s or \
            category == constant.examEntry5s:
            amount = 5
            examlist, arealist = makeExam2(user_id, amount, int(category), level,
                                           constant.TimePerQuestion, '')
        else:
            setStage(user_id, 9)
            priv = getPrivilege(user_id)
            return render_template('admin.html',
                                   user_id=int(user_id),
                                   priv=priv,
                                   )
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
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )

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

        q, a1, a2, a3, a4, cidx[0], cidx[1],cidx[2],cidx[3], conn, c = getQuestionFromNum(num, permutation)

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
        return render_template('analysis2.html',
                               user_id=user_id,
                               q=q,
                               a1=a1,
                               a2=a2,
                               a3=a3,
                               a4=a4,
                               correct=correct,
                               comment=comment,
                               answer="ABCD"[crct],
                               category=category,
                               area=area,
                               subject=constant.SUBJECT,
                               )
    else:
        stage = getStage(user_id)
        if (stage == 1):
            setStage(user_id, 2)

        if not is_login():
            return """
            <h1>ログインしてください</h1>
            <p><a href="/">→ログインする</a></p>
            """

        #        category = request.form['category']
        print('category=' + str(category))

# １問１答の処理（91:FND,92:CDS,93:DSV,94:HVIT,95:DPI）
        if (category == '91'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(11, 19)
        elif (category == '92'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(21, 29)
        elif (category == '93'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(31, 39)
        elif (category == '94'):
            q, a1, a2, a3, a4, crct, cid, num, permutation = getQuestionFromCategory(41, 49)
        else:
            setStage(user_id, 1)
            status = getStatus(user_id)
            return render_template('main-menu.html',
                                   user_id=user_id,
                                   status=status,
                                   )

    n = int(category) - 91
    return render_template('exercise2.html',
                           user_id=user_id,
                           question=q,
                           selection1=a1,
                           selection2=a2,
                           selection3=a3,
                           selection4=a4,
                           timeMin=0,
                           timeSec=0,
                           selectStr="",
                           crct=crct,
                           cid=cid,
                           num=num,
                           permutation=permutation,
                           category=category,
                           area=abbreviation[n], # 領域（エリア）名：constant.pyで定義subject = constant.SUBJECT,
                           subject = constant.SUBJECT,
    )

# ログインしているか調べる
@exam_module.route('/is_login')
def is_login():
    if 'login' in session:
        return "on"
    else:
        return "off"
    return 'login' in session