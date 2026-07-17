from constant import MaxQuestions, DIFF_JST_FROM_UTC, \
     PASS1_MESSAGE, FAIL_MESSAGE, \
     PASS_MESSAGE_IN_MAIL, PASS_MESSAGE_ON_SCREEN, FAIL_MESSAGE_ON_SCREEN
import constant
from flask import Flask, session, render_template, request, Blueprint
from users import getStage, setStage, getStatus, rankUp, rankDown, getMailadress
import sqlite3, os
import datetime
from examDB import getQuestion, getQuestions, Question, getCorrectList
from resultDB import putResult
from mail import sendMail

exec_module = Blueprint("exercise", __name__, static_folder='./static')

# 問題の出題
@exec_module.route('/exercise')
def exercise():

    command = request.args.get("command", "")
    q_no = request.args.get("q_no", "")
    user_id = request.args.get("user_id", "")
    title = request.args.get("title", "")
    exam_id = request.args.get("exam_id", "")
    total = int(request.args.get("total", ""))
    examlist = request.args.get("examlist", "")
    arealist = request.args.get("arealist", "")
#    timeMin = request.args.get("timeMin", "")
#    timeH = request.args.get("timeH", "")
#    timeSec = request.args.get("timeSec", "")

    timePerQ = request.args.get("timePerQ", "")

    stage = getStage(user_id)
    if (stage != 2 and stage != 3 and stage != 4):
        return render_template('error.html',
                               user_id=user_id,
                               error_message='エラーが発生しました。')
    if (stage == 2):
        setStage(user_id, 3)
    if (stage == 4):
        return render_template('error.html',
                               user_id=user_id,
                               error_message='試験が終了してから演習に戻ることはできません。ログインし直してください。')

    selectStr = ["", "", "", ""]
    backward = ""
    forward = ""
    if os.name != 'nt':
        now = datetime.datetime.now() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
    else:
        now = datetime.datetime.now()

    if command == 'start':
        q_no = 1
        q, conn, c = getQuestion(examlist, q_no)
        if q == None:
            code = getCode(arealist[q_no-1])
            return render_template('error3.html',
                                   error_message='該当する問題がありませんでした。コード：' + str(code)
                                   )

        backward = "disabled"
        answerlist = ""
        marklist = ""
        timePerQ = constant.TimePerQuestion

        stime = now.strftime("%H:%M:%S")
        sdate = now.strftime("%Y-%m-%d")
        stime = sdate + " " + stime

        timeH = 0
        timeMin = 0
        timeSec = 0

        for i in range(total):
            answerlist = answerlist + "0"
            marklist = marklist + "0"

        # データベースへ開始時間を格納
#        conn = sqlite3.connect(db_path)
#        c = conn.cursor()

        sql = 'SELECT START_TIME FROM EXAM_TABLE WHERE EXAM_ID = ' + exam_id + ";"
        c.execute(sql)
        items = c.fetchall()
        xtime = items[0][0]

        if xtime == None:
            sql = 'UPDATE EXAM_TABLE SET ANSWERLIST = "' + str(answerlist) + \
                '", START_TIME = "' + stime + '" WHERE EXAM_ID = ' + exam_id + ";"
            c.execute(sql)
            conn.commit()
            conn.close()
        else:
            timeH, timeMin, timeSec = getDelta(exam_id, now)

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeH=timeH,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               title=title,
                               timePerQ=timePerQ,
                               )

    elif command == 'next':
        q_no = (int)(request.args.get("q_no", ""))
        marklist = request.args.get("marklist", "")
        answerlist = request.args.get("answerlist", "")
        timeH, timeMin, timeSec = getDelta (exam_id, now)

        q_no += 1
        q, conn, c = getQuestion(examlist, q_no)
        if q == None:
            code = getCode(arealist[q_no-1])
            return render_template('error3.html',
                                   error_message='該当する問題がありませんでした。コード：' + str(code)
                                   )

        if (q_no >= total):
            forward = "disabled"

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeH=timeH,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               title=title,
                               timePerQ=timePerQ,
                               )

    elif command == 'previous':
        q_no = (int)(request.args.get("q_no", ""))
        marklist = request.args.get("marklist", "")
        answerlist = request.args.get("answerlist", "")
        timeH, timeMin, timeSec = getDelta (exam_id, now)

        q_no -= 1
        q, conn, c = getQuestion(examlist, q_no)
        if q == None:
            code = getCode(arealist[q_no-1])
            return render_template('error3.html',
                                   error_message='該当する問題がありませんでした。コード：' + str(code)
                                   )

        if (q_no == 1):
            backward = "disabled"

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeH=timeH,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               title=title,
                               timePerQ=timePerQ,
                               )

    elif command == 'move':
        q_no = (int)(request.args.get("q_no", ""))
        marklist = request.args.get("marklist", "")
        answerlist = request.args.get("answerlist", "")
        timeH, timeMin, timeSec = getDelta (exam_id, now)

        q, conn, c = getQuestion(examlist, q_no)
        if q == None:
            code = getCode(arealist[q_no-1])
            return render_template('error3.html',
                                   error_message='該当する問題がありませんでした。コード：' + str(code)
                                   )

        if (q_no == 1):
            backward = "disabled"
        if (q_no == total):
            forward = "disabled"

        return render_template('exercise.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               q_no=q_no,
                               question=q.q,
                               selection1=q.a1,
                               selection2=q.a2,
                               selection3=q.a3,
                               selection4=q.a4,
                               selectStr=selectStr,
                               marklist=marklist,
                               answerlist=answerlist,
                               backward=backward,
                               forward=forward,
                               timeH=timeH,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               title=title,
                               timePerQ=timePerQ,
                               )

    elif (command == 'finish') or (command == 'timeout'):
        timeH, timeMin, timeSec = getDelta (exam_id, now)
        #   終了
        setStage(user_id, 4)
        answerlist = request.args.get("answerlist", "")
        examlist = request.args.get("examlist", "")
        correctlist = getCorrectList(examlist)
        correct = 0
        resultlist = ""
        for i, c in enumerate(answerlist):
            if (c == correctlist[i]):
                correct += 1
                resultlist = resultlist + "1"
            else:
                resultlist = resultlist + "0"

        # デバックのためのコード
        # 正解数を35にする
        # correct = 35
        
        # conn, cを取得するためのコード
        q_no = 1
        q, conn, c = getQuestion(examlist, q_no)
        # データベースへ試験結果を格納
#        conn = sqlite3.connect(db_path)
#        c = conn.cursor()
        rate = round((correct / total * 100), 1)
        usedTime = int(timeSec) + int(timeMin) * 60 + int(timeH) * 3600
        total_time = total * constant.TimePerQuestion

        if len(answerlist) != total:
            for i in range(total):
                answerlist = answerlist + "0"

        sql = "UPDATE EXAM_TABLE SET ANSWERLIST = '" \
              + str(answerlist) + "', RESULTLIST = '" + resultlist + "', SCORE = " + str(correct) + ", USED_TIME = " \
              + str(usedTime) + ", TOTAL_TIME = " + str(total_time) + ", RATE = " + str(rate) \
              + " WHERE EXAM_ID = " + exam_id + ";"
        print(sql)
        c.execute(sql)

        sql = "SELECT START_TIME, EXAM_TYPE FROM EXAM_TABLE WHERE EXAM_ID = " + exam_id + ";"
        c.execute(sql)
        items = c.fetchall()
        stime = items[0][0]
        type = items[0][1]
        conn.commit()
        conn.close()

        putResult(user_id, exam_id, total, arealist, answerlist, resultlist, correct, rate, usedTime)

        flag = 0
        old_status = getStatus(user_id)

        # ユーザのステータスを更新
        if rate >= constant.PassScore2 and total == constant.MaxQuestions:
            status, flag = rankUp(user_id, 2, type)
        elif rate >= constant.PassScore1 and total == constant.MaxQuestions:
            status, flag = rankUp(user_id, 1, type)

        if old_status == 31 and type == constant.examType12 and rate < constant.PassScore2: # 75%を越えなければ、始めからやり直し
            rankDown(user_id)
            flag = 4
        # 修了試験で合格点を取った場合
        if flag == 3:
            userInfo = ["", "", ""]
            userInfo = getMailadress(user_id)
            username = str(userInfo[0][0]) + " " + str(userInfo[0][1])
            to_email = str(userInfo[0][2])
            if old_status == 31 and type == constant.examType12:
                sendMail(username, to_email, PASS_MESSAGE_IN_MAIL)
        # 修了試験受験時のメッセージ
        if old_status >= 30 and type == constant.examType12:
            if rate < constant.PassScore2:
                if old_status >= 40:
                    message = FAIL_MESSAGE_ON_SCREEN
                else:
                    message = FAIL_MESSAGE
            elif old_status == 30:
                message = PASS1_MESSAGE
            elif old_status == 31:
                message = constant.PASS2_MESSAGE_1 + constant.PASS2_MESSAGE_2 + \
                        constant.PASS2_MESSAGE_3 + constant.PASS2_MESSAGE_4 + constant.PASS2_MESSAGE_5
            else:
                message = PASS_MESSAGE_ON_SCREEN

            return render_template('finish2.html',
                               user_id=user_id,
                               title=title,
                               message=message,
                               )
        # 通常試験時のメッセージ
        else:
            return render_template('finish.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               examlist=examlist,
                               arealist=arealist,
                               answerlist=answerlist,
                               resultlist=resultlist,
                               correct=correct,
                               rate=round(rate,2),
                               timeH=timeH,
                               timeMin=timeMin,
                               timeSec=timeSec,
                               stime=stime,
                               stage=stage,
                               title=title,
                               flag=flag,
                               )

base_path = os.path.dirname(__file__)
db_path = base_path + '/exam.sqlite'

def getDelta(exam_id, now):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = "SELECT START_TIME FROM EXAM_TABLE WHERE EXAM_ID = " + exam_id + ";"
    c.execute(sql)
    items = c.fetchall()
    stime = items[0][0]
    conn.close()

    bdate = stime[0:10]
    bHour = stime[11:13]
    bMin = stime[14:16]
    bSec = stime[17:19]
    ntime = now.strftime("%H:%M:%S")
    ndate = now.strftime("%Y-%m-%d")
    nHour = ntime[0:2]
    nMin = ntime[3:5]
    nSec = ntime[6:8]

    dH=int(nHour)-int(bHour)
    dMin=int(nMin)-int(bMin)
    dSec=int(nSec)-int(bSec)

    begin = 3600 * int(bHour) + 60 * int(bMin) + int(bSec)
    end = 3600 * int(nHour) + 60 * int(nMin) + int(nSec)
    if bdate != ndate:
        end = end + 3600 * 24
    delta = end - begin

    timeH = int(delta / 3600)
    if timeH > 0:
        delta = delta - (timeH * 3600)
    timeMin = int(delta / 60)
    timeSec = delta % 60

    return  timeH, timeMin, timeSec

def getCode(n):
    i = 0
    while n != constant.categoryCode[i]:
        i = i + 1
    return constant.categoryNumber[i]
