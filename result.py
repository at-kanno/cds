from constant import db_path, categoryCode, practice, areaname, return3, return4
import constant
from flask import Flask, session, render_template, request, Blueprint
from users import getStage, setStage, getStatus
from resultDB import getStartTime, getResult, makeComments, getComment
from examDB import stringToButton, getExamlist, Question, getQuestion, getCommentId

result_module = Blueprint("result", __name__, static_folder='./static')

# 分析結果をフィードバックする
@result_module.route('/summary', methods=['POST', 'GET'])
def summary():

    if request.method == 'POST':
        print('summary(POST)')
        command = int(request.form['command'])
        user_id = request.form['user_id']
        exam_id = request.form['exam_id']
        total = int(request.form['total'])
        arealist = request.form['arealist']
        resultlist = request.form['resultlist']
        #        result = request.form['result']
        correct = int(request.form['correct'])
        title = request.form['title']
        stime = getStartTime(exam_id)
        stage = getStage(user_id)
        if stage < 4:
            return render_template('error.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。')
        setStage(user_id, 5)

        practice2 = [[['' for k in range(3)] for j in range(constant.NumOfCategory)] for i in range(constant.NumOfArea)]

        for i, c in enumerate(arealist):
            p = categoryCode.find(c)
            if p != -1:
                if p < constant.NumOfCategory1:
                    if (practice2[0][p][2] != ""):
                        practice2[0][p][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[0][p][2] = practice2[0][p][2] + str(i + 1)
                    else:
                        practice2[0][p][2] = practice2[0][p][2] + "-" + str(i + 1)
                elif p < constant.NumOfCategory2:
                    if (practice2[1][p-(constant.NumOfCategory1)][2] != ""):
                        practice2[1][p-(constant.NumOfCategory1)][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[1][p-(constant.NumOfCategory1)][2] = practice2[1][p-(constant.NumOfCategory1)][2] + str(i + 1)
                    else:
                        practice2[1][p-(constant.NumOfCategory1)][2] = practice2[1][p-(constant.NumOfCategory1)][2] + "-" + str(i + 1)
                elif p < constant.NumOfCategory3:
                    if (practice2[2][p-(constant.NumOfCategory2)][2] != ""):
                        practice2[2][p-(constant.NumOfCategory2)][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[2][p-(constant.NumOfCategory2)][2] = practice2[2][p-(constant.NumOfCategory2)][2] + str(i + 1)
                    else:
                        practice2[2][p-(constant.NumOfCategory2)][2] = practice2[2][p-(constant.NumOfCategory2)][2] + "-" + str(i + 1)
                elif p < constant.NumOfCategory4:
                    if (practice2[3][p-(constant.NumOfCategory3)][2] != ""):
                        practice2[3][p-(constant.NumOfCategory3)][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[3][p-(constant.NumOfCategory3)][2] = practice2[3][p-(constant.NumOfCategory3)][2] + str(i + 1)
                    else:
                        practice2[3][p-(constant.NumOfCategory3)][2] = practice2[3][p-(constant.NumOfCategory3)][2] + "-" + str(i + 1)
                elif p < constant.NumOfCategory5:
                    if (practice2[4][p-(constant.NumOfCategory4)][2] != ""):
                        practice2[4][p-(constant.NumOfCategory4)][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[4][p-(constant.NumOfCategory4)][2] = practice2[4][p-(constant.NumOfCategory4)][2] + str(i + 1)
                    else:
                        practice2[4][p-(constant.NumOfCategory4)][2] = practice2[4][p-(constant.NumOfCategory4)][2] + "-" + str(i + 1)
                elif p < constant.NumOfCategory6:
                    if (practice2[5][p-(constant.NumOfCategory5)][2] != ""):
                        practice2[5][p-(constant.NumOfCategory5)][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[5][p-(constant.NumOfCategory5)][2] = practice2[5][p-(constant.NumOfCategory5)][2] + str(i + 1)
                    else:
                        practice2[5][p-(constant.NumOfCategory5)][2] = practice2[5][p-(constant.NumOfCategory5)][2] + "-" + str(i + 1)
                elif p < constant.NumOfCategory7:
                    if (practice2[6][p-(constant.NumOfCategory6)][2] != ""):
                        practice2[6][p-(constant.NumOfCategory6)][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[6][p-(constant.NumOfCategory6)][2] = practice2[6][p-(constant.NumOfCategory6)][2] + str(i + 1)
                    else:
                        practice2[6][p-(constant.NumOfCategory6)][2] = practice2[6][p-(constant.NumOfCategory6)][2] + "-" + str(i + 1)
                elif p < constant.NumOfCategory8:
                    if (practice2[7][p-(constant.NumOfCategory7)][2] != ""):
                        practice2[7][p-(constant.NumOfCategory7)][2] += str(",")
                    if (resultlist[i] == '1'):
                        practice2[7][p-(constant.NumOfCategory7)][2] = practice2[7][p-(constant.NumOfCategory7)][2] + str(i + 1)
                    else:
                        practice2[7][p-(constant.NumOfCategory7)][2] = practice2[7][p-(constant.NumOfCategory7)][2] + "-" + str(i + 1)
                else:
                    pass

        categoryNumber, categoryScore, categoryPercent, areaNumber, areaScore, areaPercent = \
            getResult(exam_id)

    else:
        print('summary(GET)')
        user_id = int(request.args.get('user_id'))

        stage = getStage(user_id)
        if stage == 0:
            return render_template('error.html',
                                   user_id=user_id,
                                   error_message='すでにログアウトしています。')

        setStage(user_id, 1)
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )

    rate = correct / total * 100
    result = ""

    if (command == 30):

        for i in range(constant.NumOfArea):
            areaname[i][2] = str(areaScore[i]) + "/" + str(areaNumber[i])
            if (areaNumber[i] != 0):
                areaname[i][3] = str(f'{areaPercent[i]:.1f}') + "%"
            else:
                areaname[i][3] = "-"

        for i in range(0, constant.NumOfCategory1):
            practice2[0][i][0] = str(categoryScore[i]) + "/" + str(categoryNumber[i])
            if (categoryNumber[i] != 0):
                practice2[0][i][1] = str(f'{categoryPercent[i]:.1f}') + "%"
            else:
                practice2[0][i][1] = "-"
        for i in range(0, (constant.NumOfCategory2 - constant.NumOfCategory1)):
            practice2[1][i][0] = str(categoryScore[i + constant.NumOfCategory1]) + "/" + str(categoryNumber[i + constant.NumOfCategory1])
            if (categoryNumber[i + constant.NumOfCategory1] != 0):
                practice2[1][i][1] = str(f'{categoryPercent[i + constant.NumOfCategory1]:.1f}') + "%"
            else:
                practice2[1][i][1] = "-"
        for i in range(0, (constant.NumOfCategory3 - constant.NumOfCategory2)):
            practice2[2][i][0] = str(categoryScore[i + constant.NumOfCategory2]) + "/" + str(categoryNumber[i + constant.NumOfCategory2])
            if (categoryNumber[i + constant.NumOfCategory2] != 0):
                practice2[2][i][1] = str(f'{categoryPercent[i + constant.NumOfCategory2]:.1f}') + "%"
            else:
                practice2[2][i][1] = "-"
        for i in range(0, (constant.NumOfCategory4 - constant.NumOfCategory3)):
            practice2[3][i][0] = str(categoryScore[i + constant.NumOfCategory3]) + "/" + str(categoryNumber[i + constant.NumOfCategory3])
            if (categoryNumber[i + constant.NumOfCategory3] != 0):
                practice2[3][i][1] = str(f'{categoryPercent[i + constant.NumOfCategory3]:.1f}') + "%"
            else:
                practice2[3][i][1] = "-"
        for i in range(0, (constant.NumOfCategory5 - constant.NumOfCategory4)):
            practice2[4][i][0] = str(categoryScore[i + constant.NumOfCategory4]) + "/" + str(categoryNumber[i + constant.NumOfCategory4])
            if (categoryNumber[i + constant.NumOfCategory4] != 0):
                practice2[4][i][1] = str(f'{categoryPercent[i + constant.NumOfCategory4]:.1f}') + "%"
            else:
                practice2[4][i][1] = "-"
        for i in range(0, (constant.NumOfCategory6 - constant.NumOfCategory5)):
            practice2[5][i][0] = str(categoryScore[i + constant.NumOfCategory5]) + "/" + str(categoryNumber[i + constant.NumOfCategory5])
            if (categoryNumber[i + constant.NumOfCategory5] != 0):
                practice2[5][i][1] = str(f'{categoryPercent[i + constant.NumOfCategory5]:.1f}') + "%"
            else:
                practice2[5][i][1] = "-"
        for i in range(0, (constant.NumOfCategory7 - constant.NumOfCategory6)):
            practice2[6][i][0] = str(categoryScore[i + constant.NumOfCategory6]) + "/" + str(categoryNumber[i + constant.NumOfCategory6])
            if (categoryNumber[i + constant.NumOfCategory6] != 0):
                practice2[6][i][1] = str(f'{categoryPercent[i + constant.NumOfCategory6]:.1f}') + "%"
            else:
                practice2[6][i][1] = "-"
        for i in range(0, (constant.NumOfCategory8 - constant.NumOfCategory7)):
            practice2[7][i][0] = str(categoryScore[i + constant.NumOfCategory7]) + "/" + str(categoryNumber[i + constant.NumOfCategory7])
            if (categoryNumber[i + constant.NumOfCategory7] != 0):
                practice2[7][i][1] = str(f'{categoryPercent[i + constant.NumOfCategory7]:.1f}') + "%"
            else:
                practice2[7][i][1] = "-"

        if rate >= constant.PassScore1:
            result = "合格"
        else:
            result = "不合格"

        #   結果表示のHTML

        s = "実施日時：" + \
            str(stime) + "<br>採点結果：" + str(correct) + "/" + str(total) + \
            " &nbsp; 正答率：" + str(round(rate,2)) + "% &nbsp; 合否：" + result

        f = r'<FORM action="analize" method="post">' + \
            r'<!-- 結果詳細テーブル -->' + \
            r'<TABLE cellSpacing=1 cellPadding=1 width=500 border=0>' + \
            r'<TBODY><TR><TD align=middle bgColor=blueviolet>' + \
            r'<TABLE cellSpacing=1 cellPadding=1 width=720 border=0 height=36 vspace=0 >' + \
            r'<TBODY><TR bgColor=#ffffff >' + \
            r'<TD class=blackb width=120 bgColor=lavender>' + \
            r'<center>章</center></TD>' + \
            r'<TD class=black width=40 bgColor=lavender>' + \
            r'<center>採点結果</center></TD>' + \
            r'<TD class=blackb width=56 bgColor=lavender>' + \
            r'<center>正答率</center></TD>' + \
            r'<TD class=blackb width=196 bgColor=lavender>' + \
            r'<center>節</center></TD>' + \
            r'<TD class=black width=40 bgColor=lavender>' + \
            r'<center>採点結果</center></TD>' + \
            r'<TD class=blackb width=56 bgColor=lavender>' + \
            r'<center>正答率</center></TD>' + \
            r'<TD class=blackb width=92 bgColor=lavender>' + \
            r'<center>正<font style="color:red">誤</font>リスト</center></TD>' + \
            r'</TR></TBODY>'

        yyy = ""
        for i in range(constant.NumOfArea):
            v = r'<TBODY>'
            j = int(areaname[i][1])
            v = v + r'<TR><TH ROWSPAN="' + str(j + 1) + r'" class=blackb width=196 bgColor=lavender >' + \
                str(areaname[i][0]) + \
                r'<TH bgColor=#ffffff ROWSPAN="' + str(j + 1) + r'">' + str(areaname[i][2]) + r'</TH>' + \
                r'<TH bgColor=#ffffff ROWSPAN="' + str(j + 1) + r'">' + str(areaname[i][3]) + r'</TH>' + \
                r'</TH></TR>'

            xxx = v
            for k in range(j):
                w = ""
                w = r'<TR bgColor=#ffffff ><TD class=blackb width=196 bgColor=lavender >' + \
                    r'<FORM style="height:24; margin:0px 0px 0px 0px">' + \
                    r'<INPUT TYPE="button" VALUE="' + \
                    str(practice[i][k]) + \
                    r'"　onClick="xxx()" style="color:royalblue; width:196; height:24"/></FORM></TD>' + \
                    r'<TD class=black ><center>' + str(practice2[i][k][0]) + r'</center></TD>' + \
                    r'<TD class=blackb ><center>' + str(practice2[i][k][1]) + r'</center></TD>' + \
                    r'<TD class=blackb ><center>' + \
                    stringToButton(practice2[i][k][2]) + \
                    r'</button></center></TD></TD></TR>'
                xxx = xxx + w
            yyy = yyy + xxx + r'</TBODY>'
            xxx = ""

        e = r'</TABLE></TD></TR></TBODY></TABLE><br>' + \
            r'<input type="hidden" name="user_id" value="' + str(user_id) + '" />' + \
            r'<input type="hidden" name="exam_id" value="' + str(exam_id) + '" />' + \
            r'<input type="hidden" id="total" name="total" value="' + str(total) + '" />' + \
            r'<input type="hidden" name="arealist" value="' + str(arealist) + '" />' + \
            r'<input type="hidden" name="resultlist" value="' + str(resultlist) + '" />' + \
            r'<input type="hidden" name="result" value="' + str(result) + '" />' + \
            r'<input type="hidden" name="correct" value="' + str(correct) + '" />' + \
            r'<input type="hidden" name="rate" value="' + str(rate) + '" />' + \
            r'<input type="hidden" name="stime" value="' + str(stime) + '" />' + \
            r'<input type="hidden" name="title" value="' + str(title) + '" />' + \
            r'</form>'

        #   制御の返却

        return '''
                <!DOCTYPE html>
                <html>
                <head>
                <title>詳細結果</title>
                </head>
                <body>
                <h3><b><ul>''' + title + '（領域ごとの結果）</ul></b></h3>' \
               + s + f + yyy + e + \
               return3 + user_id + return4 + \
               r'<form action="summary" method="post">' + \
               r'<input type="hidden" name="user_id" value="' + str(user_id) + '" />' + \
               r'<input type="hidden" name="exam_id" value="' + str(exam_id) + '" />' + \
               r'<input type="hidden" id="total" name="total" value="' + str(total) + '" />' + \
               r'<input type="hidden" name="arealist" value="' + str(arealist) + '" />' + \
               r'<input type="hidden" name="resultlist" value="' + str(resultlist) + '" />' + \
               r'<input type="hidden" name="result" value="' + str(result) + '" />' + \
               r'<input type="hidden" name="correct" value="' + str(correct) + '" />' + \
               r'<input type="hidden" name="rate" value="' + str(rate) + '" />' + \
               r'<input type="hidden" name="stime" value="' + str(stime) + '" />' + \
               r'<input type="hidden" name="title" value="' + str(title) + '" />' + \
               r'<button type="submit" name="command" value="50" style="margin:10px">' \
               r'答案の分析結果</button>' + \
               '</FORM></div></body></html>'

    elif (command == 40):
        print('command=40')
        if rate >= constant.PassScore1:
            result = "合格"
        else:
            result = "不合格"

        return render_template('analysis.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               rate=round(rate,2),
                               total=total,
                               correct=correct,
                               stime=stime,
                               resultlist=resultlist,
                               arealist=arealist,
                               result=result,
                               title=title,
                               )
    elif (command == 50):
        print('command=50')

        comments = makeComments(exam_id)

        if total != 0:
            if correct / total * 100 >= constant.PassScore1:
                result = '合格'
            else:
                result = '不合格'

        return render_template('comments.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               rate=round(rate,2),
                               total=total,
                               correct=correct,
                               stime=stime,
                               comments=comments,
                               resultlist=resultlist,
                               arealist=arealist,
                               result=result,
                               title=title,
                               )
    else:
        setStage(user_id, 1)
        status = getStatus(user_id)
        return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )


# 分析結果をフィードバックする
@result_module.route('/analize', methods=['GET', 'POST'])
def analize():
    qlist = [0 for QuestionList in range(constant.MaxQuestions)]

    if request.method == 'POST':
        print('analize(POST)')

        user_id = request.form['user_id']
        title = request.form['title']
        exam_id = request.form['exam_id']
        total = int(request.form['total'])
        arealist = request.form['arealist']
        resultlist = request.form['resultlist']
        result = request.form['result']
        correct = int(request.form['correct'])
        stime = request.form['stime']
        q_no = int(request.form['command'])

        examlist, arealist, answerlist = getExamlist(exam_id)

        q = Question
        q, conn, c = getQuestion(examlist, q_no)
        answers = "ABCD"
        answer = answers[q.crct]

        uanswer = (int)(answerlist[q_no-1])
        cid = getCommentId(examlist, q_no, q.crct+1, uanswer)
        comment = getComment(cid)

        return render_template('analysis.html',
                               user_id=user_id,
                               exam_id=exam_id,
                               total=total,
                               q_no=q_no,
                               q=q.q,
                               a1=q.a1,
                               a2=q.a2,
                               a3=q.a3,
                               a4=q.a4,
                               correct=correct,
                               comment=comment,
                               resultlist=resultlist,
                               result=result,
                               stime=stime,
                               arealist=arealist,
                               answer=answer,
                               title=title,
                               )

