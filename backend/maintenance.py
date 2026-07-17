from flask import render_template, request, Blueprint
from constant import db_path
import sqlite3
from resultDB import getComment

# 解説文の最小番号
MIN_NUM = 1000
maintenance_module = Blueprint("maintenance", __name__, static_folder='./static')

# エラーコード
ERR_NUMBER_EMPTY = 1 << 0
ERR_NUMBER_INVALID = 1 << 1
ERR_AREA_EMPTY = 1 << 2
ERR_AREA_INVALID = 1 << 3
ERR_CATEGORY_EMPTY = 1 << 4
ERR_CATEGORY_INVALID = 1 << 5
ERR_Q_EMPTY = 1 << 6
ERR_A1_EMPTY = 1 << 7
ERR_A2_EMPTY = 1 << 8
ERR_A3_EMPTY = 1 << 9
ERR_A4_EMPTY = 1 << 10
ERR_CID_EMPTY = 1 << 11
ERR_CID_INVALID = 1 << 12
ERR_COMMENT_EMPTY = 1 << 13
ERR_CID1_EMPTY = 1 << 14
ERR_CID1_INVALID = 1 << 15
ERR_COMMENT1_EMPTY = 1 << 16
ERR_CID2_EMPTY = 1 << 17
ERR_CID2_INVALID = 1 << 18
ERR_COMMENT2_EMPTY = 1 << 19
ERR_CID3_EMPTY = 1 << 20
ERR_CID3_INVALID = 1 << 21
ERR_COMMENT3_EMPTY = 1 << 22
ERR_CID_COMBINATION1 = 1 << 31
ERR_CID_COMBINATION2 = 1 << 32
ERR_CID_COMBINATION3 = 1 << 33
ERR_CID_COMBINATION4 = 1 << 34
ERR_CID_COMBINATION5 = 1 << 35
ERR_CID_COMBINATION6 = 1 << 36

#NO_OLD_COMMENT0 = 1 << 31
#NO_OLD_COMMENT1 = 1 << 32
#NO_OLD_COMMENT2 = 1 << 33
#NO_OLD_COMMENT3 = 1 << 34
NO_OLD_COMMENT0 = 0
NO_OLD_COMMENT1 = 0
NO_OLD_COMMENT2 = 0
NO_OLD_COMMENT3 = 0

@maintenance_module.route('/maintenance', methods=['POST'])
def maintenance():
    user_id = request.form.get('user_id')
    command = request.form.get('command')
    retrieveFlag = request.form.get('retrieveFlag')
    firstFlag = request.form.get('firstFlag')
    if (command == 'retrieve' or command == 'new'):
        if (command == 'retrieve'):
            retrieveFlag = 1
            firstFlag = 0
            try:
                qid = int(request.form.get('number'))
            except:
                return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='問題番号を入力してください。',
                                   )
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            sql = "SELECT CATEGORY,LEVEL,Q,A1,A2,A3,A4,CID1,CID2,CID3,CID4 FROM knowledge_base WHERE " \
              "NUMBER == " + str(qid) + ";"
            try:
                c.execute(sql)
                print("Success!")
            except Exception as e:
                conn.close()
                return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='データベースでエラーが発生しました。',
                                   )
            else:
                items = c.fetchall()
                n = len(items)
                conn.close()
                if n < 1:
                    return render_template('error3.html',
                                       user_id=user_id,
                                       error_message='該当する演習問題はありません。',
                                       )
                category = items[0][0]
                area = items[0][1]
                question = items[0][2]
                answer = items[0][3]
                choice1 = items[0][4]
                choice2 = items[0][5]
                choice3 = items[0][6]
                cid0 = items[0][7]
                cid1 = items[0][8]
                cid2 = items[0][9]
                cid3= items[0][10]
                old_cid0 = items[0][7]
                old_cid1 = items[0][8]
                old_cid2 = items[0][9]
                old_cid3 = items[0][10]

                comment1=comment2=comment3=''
                old_comment1=old_comment2=old_comment3=''
                advice0=advice1=advice2=advice3=''

                try:
                    comment0 = old_comment0 = getComment(cid0)
                except:
                    comment0 = old_comment0 = ''
                    advice0 = '該当する解説がありません。解説番号＝' + str(cid0)

                cidFlag = checkCombination(cid0, cid1, cid2, cid3)
                if cidFlag <= 5:
                    advice1 = '正解の解説と同じ番号です。'
                else:
                    try:
                        comment1 = old_comment1 = getComment(cid1)
                    except:
                        comment1 = old_comment1 = ''
                        advice1 = '該当する解説がありません。解説番号＝' + str(cid1)

                if (cidFlag >=3 and cidFlag <= 5 ) or cidFlag >=12:
                    try:
                        comment2 = old_comment2 = getComment(cid2)
                    except:
                        comment2 = old_comment2 = ''
                        advice2 = '該当する解説がありません。解説番号＝' + str(cid2)
                elif cidFlag <= 8:
                    advice2 = '正解の解説と同じ番号です。'
                else:
                    advice2 = '選択肢１の解説と同じ番号です。'

                if cidFlag ==2 or cidFlag == 5 or cidFlag ==8 \
                    or cidFlag == 11 or cidFlag ==15:
                    try:
                        comment3 = old_comment3 = getComment(cid3)
                    except:
                        comment3 = old_comment3 = ''
                        advice3 = '該当する解説がありません。解説番号＝' + str(cid3)
                elif cidFlag == 7 or cidFlag == 10 or cidFlag == 13:
                    advice3 = '選択肢１の解説と同じ番号です。'
                elif cidFlag == 4 or cidFlag == 14:
                    advice3 = '選択肢２の解説と同じ番号です。'
                else:
                    advice3 = '正解の解説と同じ番号です。'

        else: # new (add question)
            retrieveFlag = 0
            firstFlag = 1
            qid = 0
            category = 0
            area = 0
            question = ""
            answer = ""
            choice1 = choice2 = choice3 = ""
            cid0 = cid1 = cid2 = cid3 = 0
            comment0 = comment1 = comment2 = comment3 = ""
            old_comment0 = old_comment1 = old_comment2 = old_comment3 = ""
            advice0 = advice1 = advice2 = advice3 = ""
            cidFlag = 0
            old_cid0 = old_cid1 = old_cid2 = old_cid3 = 0

        commentFlag='off'   # 最初はコメントデータは表示しない
        errorFlags=0

        return render_template('question.html',
                               user_id=user_id,
                               qid = qid,
                               category = category,
                               area = area,
                               question = question,
                               answer = answer,
                               choice1 = choice1,
                               choice2 = choice2,
                               choice3 = choice3,
                               cid0 = cid0,
                               cid1 = cid1,
                               cid2 = cid2,
                               cid3 = cid3,
                               comment0 = comment0,
                               comment1 = comment1,
                               comment2 = comment2,
                               comment3 = comment3,
                               old_cid0 = old_cid0,
                               old_cid1 = old_cid1,
                               old_cid2 = old_cid2,
                               old_cid3 = old_cid3,
                               old_comment0 = old_comment0,
                               old_comment1 = old_comment1,
                               old_comment2 = old_comment2,
                               old_comment3 = old_comment3,
                               advice0 = advice0,
                               advice1 = advice1,
                               advice2 = advice2,
                               advice3 = advice3,
                               commentFlag=commentFlag,
                               main_check='off', # cidごとの編集なし［デフォルト］
                               sub_check1='off', # cidごとの編集なし［デフォルト］
                               sub_check2='off', # cidごとの編集なし［デフォルト］
                               sub_check3='off', # cidごとの編集なし［デフォルト］
                               firstFlag=firstFlag,
                               retrieveFlag=retrieveFlag,
                               errorFlags=errorFlags,
                               )
    elif (command == 'confirm'):
        errorFlags = int(request.form.get('errorFlags' or 0))
        retrieveFlag = request.form.get('retrieveFlag')
        firstFlag = request.form.get('firstFlag')

        qid = int(request.form.get('qid'))
        category = int(request.form.get('category'))
        area = int(request.form.get('area'))

        question = request.form.get('question')
        if question==None or question=='':
            question=''
        question = question.strip()
        answer = request.form.get('answer')
        if answer==None or answer=='':
            answer=''
        answer = answer.strip()
        choice1 = request.form.get('choice1')
        if choice1==None or choice1=='':
            choice1=''
        choice1 = choice1.strip()
        choice2 = request.form.get('choice2')
        if choice2==None or choice2=='':
            choice2=''
        choice2 = choice2.strip()
        choice3 = request.form.get('choice3')
        if choice3==None or choice3=='':
            choice3=''
        choice3 = choice3.strip()

        advice0 = advice1 = advice2 = advice3 = ''

        cid0 = int(request.form.get('cid0') or 0)
        comment0 = request.form.get('comment0')
        commentFlag = request.form.get('commentFlag')

        if cid0=='' or cid0==None or cid0 <= 1000:
            errorFlags |= ERR_CID_INVALID
#        else:
#            if int(retrieveFlag) == 1 and commentFlag != 'on':  # commentFlag がoffの時、過去の解説を入れておく

        if commentFlag != 'on' and int(retrieveFlag) == 0:
            try:
                old_comment0 = getComment(cid0)
            except:
                old_comment0 = ''

            if category == '' or category == 'None' :
                errorFlags |= ERR_CATEGORY_EMPTY
            elif int(category) <= 0:
                errorFlags |= ERR_CATEGORY_INVALID
            if area == '' or area == 'None' :
                errorFlags |= ERR_AREA_EMPTY
            elif int(area) <= 0:
                errorFlags |= ERR_AREA_INVALID
            if not question.strip():
                errorFlags |= ERR_Q_EMPTY
            if not answer.strip():
                errorFlags |= ERR_A1_EMPTY
            if not choice1.strip():
                errorFlags |= ERR_A2_EMPTY
            if not choice2.strip():
                errorFlags |= ERR_A3_EMPTY
            if not choice3.strip():
                errorFlags |= ERR_A4_EMPTY
            if commentFlag == 'on':
                if not comment0.strip():
                    errorFlags |= ERR_COMMENT_EMPTY

            if errorFlags != 0:
                if errorFlags & ERR_AREA_EMPTY:
                    area_invalid = True
                elif errorFlags & ERR_AREA_INVALID:
                    area_invalid = True
                else:
                    area_invalid = False

                if errorFlags & ERR_CATEGORY_EMPTY:
                    category_invalid = True
                elif errorFlags & ERR_CATEGORY_INVALID:
                    category_invalid = True
                else:
                    category_invalid = False

                if errorFlags & ERR_Q_EMPTY:
                    question_invalid = True
                else:
                    question_invalid = False
                if errorFlags & ERR_A1_EMPTY:
                    answer_invalid = True
                else:
                    answer_invalid = False
                if errorFlags & ERR_A2_EMPTY:
                    choice1_invalid = True
                else:
                    choice1_invalid = False
                if errorFlags & ERR_A3_EMPTY:
                    choice2_invalid = True
                else:
                    choice2_invalid = False
                if errorFlags & ERR_A4_EMPTY:
                    choice3_invalid = True
                else:
                    choice3_invalid = False

                if errorFlags & ERR_CID_EMPTY:
                    cid0_invalid = True
                elif errorFlags & ERR_CID_INVALID:
                    cid0_invalid = True
                else:
                    cid0_invalid = False

                if errorFlags & ERR_COMMENT_EMPTY:
                    comment0_invalid = True
                else:
                    comment0_invalid = False

                return render_template('question.html',
                                       user_id=user_id,
                                       qid=qid,
                                       category=category,
                                       area=area,
                                       question=question,
                                       answer=answer,
                                       choice1=choice1,
                                       choice2=choice2,
                                       choice3=choice3,
                                       cid0=cid0,
                                       comment0=comment0,
                                       comment1='',
                                       comment2='',
                                       comment3='',
                                       cid1=cid0,
                                       cid2=cid0,
                                       cid3=cid0,
                                       main_check='off',
                                       sub_check1='off',
                                       sub_check2='off',
                                       sub_check3='off',
                                       old_cid0=0,
                                       old_cid1=0,
                                       old_cid2=0,
                                       old_cid3=0,
                                       old_comment0=old_comment0,
                                       advice0=advice0,
                                       commentFlag=commentFlag,
                                       firstFlag=firstFlag,
                                       retrieveFlag=retrieveFlag,
                                       errorFlags=errorFlags,
                                       area_invalid=area_invalid,
                                       category_invalid=category_invalid,
                                       question_invalid=question_invalid,
                                       answer_invalid=answer_invalid,
                                       choice1_invalid=choice1_invalid,
                                       choice2_invalid=choice2_invalid,
                                       choice3_invalid=choice3_invalid,
                                       cid0_invalid=cid0_invalid,
                                       comment0_invalid=comment0_invalid,
                                       )

            return render_template('qconfirmX.html',
                                   user_id=user_id,
                                   qid=qid,
                                   category=category,
                                   area=area,
                                   question=question,
                                   answer=answer,
                                   choice1=choice1,
                                   choice2=choice2,
                                   choice3=choice3,
                                   cid0=cid0,
                                   comment0=comment0,
                                   comment1='',
                                   comment2='',
                                   comment3='',
                                   cid1=cid0,
                                   cid2=cid0,
                                   cid3=cid0,
                                   main_check='off',
                                   sub_check1='off',
                                   sub_check2='off',
                                   sub_check3='off',
                                   old_cid0=0,
                                   old_cid1=0,
                                   old_cid2=0,
                                   old_cid3=0,
                                   old_comment0=old_comment0,
                                   errorFlags=errorFlags,
                                   commentFlag=commentFlag,
                                   retrieveFlag=retrieveFlag,
                                   firstFlag=firstFlag,
                                   advice0=advice0,
                                   )
        else:
            if comment0 == None or comment0 == '':
                errorFlags |= ERR_COMMENT_EMPTY
                comment0 = ''
            else:
                comment0 = comment0.strip()

        sub_check1 = request.form.get('sub_check1')
        sub_check2 = request.form.get('sub_check2')
        sub_check3 = request.form.get('sub_check3')
        old_comment0 = request.form.get('old_comment0')
        old_comment1 = request.form.get('old_comment1')
        old_comment2 = request.form.get('old_comment2')
        old_comment3 = request.form.get('old_comment3')
        old_cid0 = int(request.form.get('old_cid0'))
        old_cid1 = int(request.form.get('old_cid1'))
        old_cid2 = int(request.form.get('old_cid2'))
        old_cid3 = int(request.form.get('old_cid3'))

        cid1 = int(request.form.get('cid1'))
        comment1 = request.form.get('comment1')
        if sub_check1 == '1':
            if cid1 == '' or cid1 == None:
                errorFlags |= ERR_CID1_EMPTY
            elif cid1 <= 1000:
                errorFlags |= ERR_CID1_INVALID
            if comment1 == '' or comment1 == None:
                errorFlags |= ERR_COMMENT1_EMPTY
        else:
            cid1 = old_cid1
            comment1 = old_comment1

        cid2 = int(request.form.get('cid2'))
        comment2 = request.form.get('comment2')
        if sub_check2 == '2':
            if cid2 == '' or cid2 == None:
                errorFlags |= ERR_CID2_EMPTY
            elif cid2 <= 1000:
                errorFlags |= ERR_CID2_INVALID
            if comment2 == '' or comment2 == None:
                errorFlags |= ERR_COMMENT2_EMPTY
        else:
            cid2 = old_cid2
            comment2 = old_comment2

        cid3 = int(request.form.get('cid3'))
        comment3 = request.form.get('comment3')
        if sub_check3 == '3':
            if cid3 == '' or cid3 == None:
                errorFlags |= ERR_CID3_EMPTY
            elif cid3 <= 1000:
                errorFlags |= ERR_CID3_INVALID
            if comment3 == '' or comment3 == None:
                errorFlags |= ERR_COMMENT3_EMPTY
        else:
            cid3 = old_cid3
            comment3 = old_comment3

        main_check = request.form.get('main_check')

        if main_check != 'on':

            sub_check1 = sub_check2 = sub_check3 = 'off'

            if old_cid1 == 0:
                cid1 = cid0
            else:
                cid1 = old_cid1
            if old_cid2 == 0:
                cid2 = cid0
            else:
                cid2 = old_cid2
            if old_cid3 == 0:
                cid3 = cid0
            else:
                cid3 = old_cid3

            try:
                comment1 = getComment(int(cid1))
            except:
                comment1 = ''
            if cid1 == cid0:
                advice1 = '現在の解説番号と同じです。'

            try:
                comment2 = getComment(int(cid2))
            except:
                comment2 = ''
            if cid2 == cid0:
                advice2 = '現在の解説番号と同じです。'

            try:
                comment3 = getComment(int(cid3))
            except:
                comment3 = ''
            if cid3 == cid0:
                advice3 = '現在の解説番号と同じです。'

            if category == '' or category == 'None' :
                errorFlags |= ERR_CATEGORY_EMPTY
            elif int(category) <= 0:
                errorFlags |= ERR_CATEGORY_INVALID
            if area == '' or area == 'None' :
                errorFlags |= ERR_AREA_EMPTY
            elif int(area) <= 0:
                errorFlags |= ERR_AREA_INVALID
            if not question.strip():
                errorFlags |= ERR_Q_EMPTY
            if not answer.strip():
                errorFlags |= ERR_A1_EMPTY
            if not choice1.strip():
                errorFlags |= ERR_A2_EMPTY
            if not choice2.strip():
                errorFlags |= ERR_A3_EMPTY
            if not choice3.strip():
                errorFlags |= ERR_A4_EMPTY
            if commentFlag == 'on':
                if not comment0.strip():
                    errorFlags |= ERR_COMMENT_EMPTY

            if errorFlags != 0:
                if errorFlags & ERR_AREA_EMPTY:
                    area_invalid = True
                elif errorFlags & ERR_AREA_INVALID:
                    area_invalid = True
                else:
                    area_invalid = False

                if errorFlags & ERR_CATEGORY_EMPTY:
                    category_invalid = True
                elif errorFlags & ERR_CATEGORY_INVALID:
                    category_invalid = True
                else:
                    category_invalid = False

                if errorFlags & ERR_Q_EMPTY:
                    question_invalid = True
                else:
                    question_invalid = False
                if errorFlags & ERR_A1_EMPTY:
                    answer_invalid = True
                else:
                    answer_invalid = False
                if errorFlags & ERR_A2_EMPTY:
                    choice1_invalid = True
                else:
                    choice1_invalid = False
                if errorFlags & ERR_A3_EMPTY:
                    choice2_invalid = True
                else:
                    choice2_invalid = False
                if errorFlags & ERR_A4_EMPTY:
                    choice3_invalid = True
                else:
                    choice3_invalid = False

                if errorFlags & ERR_CID_EMPTY:
                    cid0_invalid = True
                elif errorFlags & ERR_CID_INVALID:
                    cid0_invalid = True
                else:
                    cid0_invalid = False

                if errorFlags & ERR_COMMENT_EMPTY:
                    comment0_invalid = True
                else:
                    comment0_invalid = False

                return render_template('question.html',
                                       user_id=user_id,
                                       qid=qid,
                                       category=category,
                                       area=area,
                                       question=question,
                                       answer=answer,
                                       choice1=choice1,
                                       choice2=choice2,
                                       choice3=choice3,
                                       cid0=cid0,
                                       cid1=cid1,
                                       cid2=cid2,
                                       cid3=cid3,
                                       comment0=comment0,
                                       comment1=comment1,
                                       comment2=comment2,
                                       comment3=comment3,
                                       old_cid0=old_cid0,
                                       old_cid1=old_cid1,
                                       old_cid2=old_cid2,
                                       old_cid3=old_cid3,
                                       old_comment0=old_comment0,
                                       old_comment1=old_comment1,
                                       old_comment2=old_comment2,
                                       old_comment3=old_comment3,
                                       advice0=advice0,
                                       commentFlag=commentFlag,
                                       main_check=main_check,
                                       sub_check1=sub_check1,
                                       sub_check2=sub_check2,
                                       sub_check3=sub_check3,
                                       firstFlag=firstFlag,
                                       retrieveFlag=retrieveFlag,
                                       errorFlags=errorFlags,
                                       area_invalid=area_invalid,
                                       category_invalid=category_invalid,
                                       question_invalid=question_invalid,
                                       answer_invalid=answer_invalid,
                                       choice1_invalid=choice1_invalid,
                                       choice2_invalid=choice2_invalid,
                                       choice3_invalid=choice3_invalid,
                                       cid0_invalid=cid0_invalid,
                                       comment0_invalid=comment0_invalid,
                                       )

            return render_template('qconfirm.html',
                                   user_id=user_id,
                                   qid=qid,
                                   category=category,
                                   area=area,
                                   question=question,
                                   answer=answer,
                                   choice1=choice1,
                                   choice2=choice2,
                                   choice3=choice3,
                                   cid0=cid0,
                                   comment0=comment0,
                                   comment1=comment1,
                                   comment2=comment2,
                                   comment3=comment3,
                                   cid1=cid1,
                                   cid2=cid2,
                                   cid3=cid3,
                                   main_check=main_check,
                                   sub_check1=sub_check1,
                                   sub_check2=sub_check2,
                                   sub_check3=sub_check3,
                                   old_cid0=old_cid0,
                                   old_cid1=old_cid1,
                                   old_cid2=old_cid2,
                                   old_cid3=old_cid3,
                                   old_comment0=old_comment0,
                                   errorFlags=errorFlags,
                                   commentFlag=commentFlag,
                                   retrieveFlag=retrieveFlag,
                                   firstFlag=firstFlag,
                                   )

        else:  # 複数コメントの処理
            cidFlag = checkCombination(cid0, cid1, cid2, cid3)
            # sub_check=1
            if cidFlag >= 1 and cidFlag <= 5:
                if comment0 != comment1 and comment1 != '':
                    advice1 = '正解と選択肢１の解説番号が同じにもかかわらず、解説文が異なります。'
                    errorFlags |= ERR_CID_COMBINATION1
                else:
                    advice1 = '正解の解説と同じ番号です。'

            # sub_check=2
            if (cidFlag >= 1 and cidFlag <= 2) or (cidFlag >= 6 and cidFlag <= 8):
                if comment0 != comment2 and comment2 != '':
                    advice2 = '正解と選択肢２の解説番号が同じにもかかわらず、解説文が異なります。'
                    errorFlags |= ERR_CID_COMBINATION2
                else:
                    advice2 = '正解の解説と同じ番号です。'
            elif (cidFlag >= 9 and cidFlag <= 11):
                if comment1 != comment2 and comment2 != '':
                    advice2 = '選択肢１と選択肢２の解説番号が同じにもかかわらず、解説文が異なります。'
                    errorFlags |= ERR_CID_COMBINATION3
                else:
                    advice2 = '選択肢１の解説と同じ番号です。'

            # sub_check=3
            if cidFlag == 1 or cidFlag == 3 or cidFlag == 6 or cidFlag == 9 or cidFlag == 12 \
                    or cidFlag == 26 or cidFlag == 28 or cidFlag == 31 or cidFlag == 33 or cidFlag == 45:
                if comment0 != comment3 and comment3 != '':
                    advice3 = '正解と選択肢３の解説番号が同じにもかかわらず、解説文が異なります。'
                    errorFlags |= ERR_CID_COMBINATION4
                else:
                    advice3 = '正解の解説と同じ番号です。'
            elif cidFlag == 7 or cidFlag == 10 or cidFlag == 13 or cidFlag == 29 or cidFlag == 34:
                if comment1 != comment3 and comment3 != '':
                    advice3 = '選択肢１と選択肢３の解説番号が同じにもかかわらず、解説文が異なります。'
                    errorFlags |= ERR_CID_COMBINATION5  # 選択肢１と選択肢３の解説番号が同じにもかかわらず、解説文が異なります。
                else:
                    advice3 = '選択肢１の解説と同じ番号です。'
            elif cidFlag == 4 or cidFlag == 14:
                if comment2 != comment3 and comment3 != '':
                    advice3 = '選択肢２と選択肢３の解説番号が同じにもかかわらず、解説文が異なります。'
                    errorFlags |= ERR_CID_COMBINATION6  # 選択肢２と選択肢３の解説番号が同じにもかかわらず、解説文が異なります。
                else:
                    advice3 = '選択肢２の解説と同じ番号です。'

            if errorFlags != 0:
                if errorFlags & ERR_AREA_EMPTY:
                    area_invalid = True
                elif errorFlags & ERR_AREA_INVALID:
                    area_invalid = True
                else:
                    area_invalid = False

                if errorFlags & ERR_CATEGORY_EMPTY:
                    category_invalid = True
                elif errorFlags & ERR_CATEGORY_INVALID:
                    category_invalid = True
                else:
                    category_invalid = False

                if errorFlags & ERR_Q_EMPTY:
                    question_invalid = True
                else:
                    question_invalid = False
                if errorFlags & ERR_A1_EMPTY:
                    answer_invalid = True
                else:
                    answer_invalid = False
                if errorFlags & ERR_A2_EMPTY:
                    choice1_invalid = True
                else:
                    choice1_invalid = False
                if errorFlags & ERR_A3_EMPTY:
                    choice2_invalid = True
                else:
                    choice2_invalid = False
                if errorFlags & ERR_A4_EMPTY:
                    choice3_invalid = True
                else:
                    choice3_invalid = False

                if errorFlags & ERR_CID_EMPTY:
                    cid0_invalid = True
                elif errorFlags & ERR_CID_INVALID:
                    cid0_invalid = True
                else:
                    cid0_invalid = False

                if errorFlags & ERR_COMMENT_EMPTY:
                    comment0_invalid = True
                else:
                    comment0_invalid = False

                if errorFlags & ERR_CID1_EMPTY:
                    cid1_invalid = True
                elif errorFlags & ERR_CID1_INVALID:
                    cid1_invalid = True
                else:
                    cid1_invalid = False
                if errorFlags & ERR_COMMENT1_EMPTY:
                    comment1_invalid = True
                else:
                    comment1_invalid = False

                if errorFlags & ERR_CID2_EMPTY:
                    cid2_invalid = True
                elif errorFlags & ERR_CID2_INVALID:
                    cid2_invalid = True
                else:
                    cid2_invalid = False
                if errorFlags & ERR_COMMENT2_EMPTY:
                    comment2_invalid = True
                else:
                    comment2_invalid = False

                if errorFlags & ERR_CID3_EMPTY:
                    cid3_invalid = True
                elif errorFlags & ERR_CID3_INVALID:
                    cid3_invalid = True
                else:
                    cid3_invalid = False
                if errorFlags & ERR_COMMENT3_EMPTY:
                    comment3_invalid = True
                else:
                    comment3_invalid = False

                if errorFlags & ERR_CID_COMBINATION1:
                    cidcomb_err1 = True
                else:
                    cidcomb_err1 = False
                if errorFlags & ERR_CID_COMBINATION2:
                    cidcomb_err2 = True
                else:
                    cidcomb_err2 = False
                if errorFlags & ERR_CID_COMBINATION3:
                    cidcomb_err3 = True
                else:
                    cidcomb_err3 = False
                if errorFlags & ERR_CID_COMBINATION4:
                    cidcomb_err4 = True
                else:
                    cidcomb_err4 = False
                if errorFlags & ERR_CID_COMBINATION5:
                    cidcomb_err5 = True
                else:
                    cidcomb_err5 = False
                if errorFlags & ERR_CID_COMBINATION6:
                    cidcomb_err6 = True
                else:
                    cidcomb_err6 = False

                errorFlags = 0
                return render_template('question.html',
                                       user_id=user_id,
                                       qid=qid,
                                       category=category,
                                       area=area,
                                       question=question,
                                       answer=answer,
                                       choice1=choice1,
                                       choice2=choice2,
                                       choice3=choice3,
                                       cid0=cid0,
                                       cid1=cid1,
                                       cid2=cid2,
                                       cid3=cid3,
                                       comment0=comment0,
                                       comment1=comment1,
                                       comment2=comment2,
                                       comment3=comment3,
                                       old_cid0=old_cid0,
                                       old_cid1=old_cid1,
                                       old_cid2=old_cid2,
                                       old_cid3=old_cid3,
                                       old_comment0=old_comment0,
                                       old_comment1=old_comment1,
                                       old_comment2=old_comment2,
                                       old_comment3=old_comment3,
                                       advice0=advice0,
                                       advice1=advice1,
                                       advice2=advice2,
                                       advice3=advice3,
                                       main_check=main_check,
                                       sub_check1=sub_check1,
                                       sub_check2=sub_check2,
                                       sub_check3=sub_check3,
                                       errorFlags=errorFlags,
                                       area_invalid=area_invalid,
                                       category_invalid=category_invalid,
                                       question_invalid=question_invalid,
                                       answer_invalid=answer_invalid,
                                       choice1_invalid=choice1_invalid,
                                       choice2_invalid=choice2_invalid,
                                       choice3_invalid=choice3_invalid,
                                       cid0_invalid=cid0_invalid,
                                       comment0_invalid=comment0_invalid,
                                       commentFlag=commentFlag,
                                       cid1_invalid=cid1_invalid,
                                       cid2_invalid=cid2_invalid,
                                       cid3_invalid=cid3_invalid,
                                       comment1_invalid=comment1_invalid,
                                       comment2_invalid=comment2_invalid,
                                       comment3_invalid=comment3_invalid,
                                       retrieveFlag=retrieveFlag,
                                       firstFlag=firstFlag,
                                       cidcomb_err1=cidcomb_err1,
                                       cidcomb_err2=cidcomb_err2,
                                       cidcomb_err3=cidcomb_err3,
                                       cidcomb_err4=cidcomb_err4,
                                       cidcomb_err5=cidcomb_err5,
                                       cidcomb_err6=cidcomb_err6,
                                       )
            # 複数コメント・エラーなしの画面推移

            if cid1!=old_cid1 and sub_check1=='1':
                try:
                    old_comment1 = getComment(old_cid1)
                except:
                    old_comment1 = ''
            if cid2!=old_cid2 and sub_check2=='2':
                try:
                    old_comment2 = getComment(old_cid2)
                except:
                    old_comment2 = ''
            if cid3!=old_cid3 and sub_check3=='3':
                try:
                    old_comment3 = getComment(old_cid3)
                except:
                    old_comment3 = ''

            return render_template('qconfirm.html',
                                   user_id=user_id,
                                   qid=qid,
                                   category=category,
                                   area=area,
                                   question=question,
                                   answer=answer,
                                   choice1=choice1,
                                   choice2=choice2,
                                   choice3=choice3,
                                   cid0=cid0,
                                   cid1=cid1,
                                   cid2=cid2,
                                   cid3=cid3,
                                   comment0=comment0,
                                   comment1=comment1,
                                   comment2=comment2,
                                   comment3=comment3,
                                   old_cid0=old_cid0,
                                   old_cid1=old_cid1,
                                   old_cid2=old_cid2,
                                   old_cid3=old_cid3,
                                   old_comment0=old_comment0,
                                   old_comment1=old_comment1,
                                   old_comment2=old_comment2,
                                   old_comment3=old_comment3,
                                   main_check=main_check,
                                   sub_check1=sub_check1,
                                   sub_check2=sub_check2,
                                   sub_check3=sub_check3,
                                   errorFlags=errorFlags,
                                   commentFlag=commentFlag,
                                   advice0=advice0,
                                   advice1=advice1,
                                   advice2=advice2,
                                   advice3=advice3,
                                   retrieveFlag=retrieveFlag,
                                   firstFlag=firstFlag,
                                   )


    elif(command == 'update'):
        qid = int(request.form.get('qid'))
        category = int(request.form.get('category'))
        area = int(request.form.get('area'))
        question = request.form.get('question')
        answer = request.form.get('answer')
        choice1 = request.form.get('choice1')
        choice2 = request.form.get('choice2')
        choice3 = request.form.get('choice3')
        cid0 = int(request.form.get('cid0'))
        if cid0=='' or cid0=='None':
            cid0 = 0
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。',
                                   )

        cid1 = int(request.form.get('cid1'))
        if cid1=='' or cid1=='None':
            cid1 = cid0
        cid2 = int(request.form.get('cid2'))
        if cid2=='' or cid2=='None':
            cid2 = cid0
        cid3 = int(request.form.get('cid3'))
        if cid3=='' or cid3=='None':
            cid3 = cid0

        comment0 = request.form.get('comment0')
        comment1 = request.form.get('comment1')
        comment2 = request.form.get('comment2')
        comment3 = request.form.get('comment3')
        main_check = request.form.get('main_check')
        commentFlag = request.form.get('commentFlag','')

        if main_check != 'on':
            if firstFlag == 1:
                cid1 = cid2 = cid3 = cid0

            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            if qid != 0:
                sql = 'UPDATE knowledge_base SET LEVEL=?,CATEGORY=?,Q=?,A1=?,A2=?,A3=?,A4=?,CID1=?,CID2=?,CID3=?,CID4=? WHERE NUMBER = ' + str(qid)
            else:
                sql = 'INSERT INTO knowledge_base (CATEGORY,LEVEL,Q,A1,A2,A3,A4,CID1,CID2,CID3,CID4) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            try:
                if (qid == 0):
                    c.execute(sql,
                                 [category, area, question, answer, choice1, choice2, choice3, cid0, cid1, cid2, cid3])
                else:
                    c.execute(sql,
                                 [category, area, question, answer, choice1, choice2, choice3, cid0, cid1, cid2, cid3])
                conn.commit()
                if (qid == 0):
                    qid = c.lastrowid
                if commentFlag != 'on':
                    message = "問題番号＝" + str(qid) + "で登録（更新）しました。"
                    return render_template('success3.html',
                                           user_id=user_id,
                                           message=message,
                                           )
                sql = 'select comment_id from comments_table where comment_id = ' + str(cid0) + ';'
                c.execute(sql)

                row = c.fetchone()
                if row is None:
                    sql = "INSERT INTO comments_table ( comment_id, comment ) " + \
                          "VALUES (" + str(cid0) + ",'" + str(comment0) + "')"
                else:
                    sql = "UPDATE comments_table SET COMMENT = '" + str(comment0) \
                          + "' WHERE COMMENT_ID = " + str(cid0) + ";"
                c.execute(sql)
                conn.commit()
                conn.close()
            except Exception as e:
                conn.close()
                return render_template('error3.html',
                                       user_id=user_id,
                                       error_message='エラーが発生しました。',
                                       )
            else:
                message = "問題番号＝" + str(qid) + "で登録（更新）しました。"
                return render_template('success3.html',
                                       user_id=user_id,
                                       message=message,
                                       )

        else: # CID=1-3を処理する
            sub1String = request.form.get('sub_check1')
            if sub1String=='1':
                sub_check1 = 1
            else:
                sub_check1 = 0
            sub2String = request.form.get('sub_check2')
            if sub2String=='2':
                sub_check2 = 1
            else:
                sub_check2 = 0
            sub3String = request.form.get('sub_check3')
            if sub3String=='3':
                sub_check3 = 1
            else:
                sub_check3 = 0

            sql1=sql2=sql3=''
            cidSQL = "',CID1="
            cidSQL2 = ""
            if cid1 == 0:
                cid1 = cid0
            if cid2 == 0:
                cid2 = cid0
            if cid3 == 0:
                cid3 = cid0
            cidFlag = checkCombination(cid0, cid1, cid2, cid3)
            # sub_check=1
            if cidFlag >= 1 and cidFlag <= 5:
                cidSQL = cidSQL + str(cid0) + ",CID2=" + str(cid0)
                cidSQL2 = cidSQL2 + str(cid0) + "," + str(cid0) + ","
            else:
                cidSQL = cidSQL + str(cid0) + ",CID2=" + str(cid1)
                cidSQL2 = cidSQL2 + str(cid0) + "," + str(cid1) + ","
            sql1 = "INSERT INTO COMMENTS_TABLE ( COMMENT_ID, COMMENT) VALUES (" \
                       + str(cid1) + ",'" + str(comment1) + "');"

            # sub_check=2
            if (cidFlag >= 1 and cidFlag <= 2) or (cidFlag >= 6 and cidFlag <= 8):
                cidSQL = cidSQL + ",CID3=" + str(cid0)
                cidSQL2 = cidSQL2 + str(cid0) + ","
            elif (cidFlag >= 9 and cidFlag <= 11):
                cidSQL = cidSQL + ",CID3=" + str(cid1)
                cidSQL2 = cidSQL2 + str(cid1) + ","
            else:
                cidSQL = cidSQL + ",CID3=" + str(cid2)
                cidSQL2 = cidSQL2 + str(cid2) + ","
            sql2 = "INSERT INTO COMMENTS_TABLE ( COMMENT_ID, COMMENT) VALUES (" \
                       + str(cid2) + ",'" + str(comment2) + "');"

            # sub_check=3
            if cidFlag == 1 or cidFlag == 3 or cidFlag == 6 or cidFlag == 9 or cidFlag == 12 \
                    or cidFlag == 26 or cidFlag == 28 or cidFlag == 31 or cidFlag == 33 or cidFlag == 45:
                cidSQL = cidSQL + ",CID4=" + str(cid0)
                cidSQL2 = cidSQL2 + str(cid0) + ")"
            elif cidFlag == 7 or cidFlag == 10 or cidFlag == 13 or cidFlag == 29 or cidFlag == 34:
                cidSQL = cidSQL + ",CID4=" + str(cid1)
                cidSQL2 = cidSQL2 + str(cid1) + ")"
            elif cidFlag == 4 or cidFlag == 14:
                cidSQL = cidSQL + ",CID4=" + str(cid2)
                cidSQL2 = cidSQL2 + str(cid2) + ")"
            else:
                cidSQL = cidSQL + ",CID4=" + str(cid3)
                cidSQL2 = cidSQL2 + str(cid3) + ")"
            sql3 = "INSERT INTO COMMENTS_TABLE ( COMMENT_ID, COMMENT) VALUES (" \
                       + str(cid3) + ",'" + str(comment3) + "');"

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        if (qid != 0):
            sql = "UPDATE knowledge_base SET LEVEL=" + str(area) + ",CATEGORY=" + str(category) + ",Q='" + str(question) + \
                  "',A1='" + str(answer) + "',A2='" + str(choice1) + "',A3='" + str(choice2) + "',A4='" + str(choice3) + \
                  str(cidSQL) + ' WHERE NUMBER = ' + str(qid)
        else:
            sql = "INSERT INTO knowledge_base (LEVEL,CATEGORY,Q,A1,A2,A3,A4,CID1,CID2,CID3,CID4) VALUES (" + \
                    str(area) + "," + str(category) + ",'" + str(question) + "','" + str(answer) + "','" + str(choice1) + "','" + \
                  str(choice2) + "','" + str(choice3) + "'," + str(cidSQL2)
        try:
            c.execute(sql)
            conn.commit()
            if (qid == 0):
                qid = c.lastrowid

            sql = 'select comment_id from comments_table where comment_id = ' + str(cid0) + ';'
            c.execute(sql)
            row = c.fetchone()
            if row is None:
                sql = "INSERT INTO comments_table ( comment_id, comment ) " + \
                "VALUES (" + str(cid0) + ",'" + str(comment0) + "')"
            else:
                sql = "UPDATE comments_table SET COMMENT = '" + str(comment0) \
                      + "' WHERE COMMENT_ID = " + str(cid0) + ";"
            c.execute(sql)
            conn.commit()

            if sql1!='' and sql1!='None' and sub_check1==1:
                sql = 'select comment_id from comments_table where comment_id = ' + str(cid1) + ';'
                c.execute(sql)
                row = c.fetchone()
                if row is None:
                    pass
                else:
                    sql1 = "UPDATE comments_table SET COMMENT = '" + str(comment1) \
                      + "' WHERE COMMENT_ID = " + str(cid1) + ";"
                c.execute(sql1)
                conn.commit()
            if sql2!='' and sql2!='None' and sub_check2==1:
                sql = 'select comment_id from comments_table where comment_id = ' + str(cid2) + ';'
                c.execute(sql)
                row = c.fetchone()
                if row is None:
                    pass
                else:
                    sql2 = "UPDATE comments_table SET COMMENT = '" + str(comment2) \
                      + "' WHERE COMMENT_ID = " + str(cid2) + ";"
                c.execute(sql2)
                conn.commit()
            if sql3!='' and sql3!='None' and sub_check3==1:
                sql = 'select comment_id from comments_table where comment_id = ' + str(cid3) + ';'
                c.execute(sql)
                row = c.fetchone()
                if row is None:
                    pass
                else:
                    sql3 = "UPDATE comments_table SET COMMENT = '" + str(comment3) \
                      + "' WHERE COMMENT_ID = " + str(cid3) + ";"
                c.execute(sql3)
                conn.commit()

            conn.close()
            print("Success!")
        except Exception as e:
            conn.close()
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。',
                                   )
        else:
            message = "問題番号＝" + str(qid) + "で登録（更新）しました。"
            return render_template('success3.html',
                               user_id=user_id,
                               message = message,
                               )
    elif(command == 'delete'):
        qid = int(request.form.get('qid'))
        question = request.form.get('question')
        answer = request.form.get('answer')
        choice1 = request.form.get('choice1')
        choice2 = request.form.get('choice2')
        choice3 = request.form.get('choice3')
        cid0 = int(request.form.get('cid0'))
        comment0 = request.form.get('comment0')
        comment1 = request.form.get('comment1')
        comment2 = request.form.get('comment2')
        comment3 = request.form.get('comment3')
        cid1 = int(request.form.get('cid1'))
        cid2 = int(request.form.get('cid2'))
        cid3 = int(request.form.get('cid3'))
        advice1 = advice2 = advice3 = ''

        cidFlag = checkCombination(cid0, cid1, cid2, cid3)
        # comment1
        if cidFlag >= 1 and cidFlag <= 5:
            advice1 = '正解の解説番号(' + str(cid0) + ')と同じです。'
            delCheck1 = 0
        else:
            delCheck1 = 1

        # comment2
        if (cidFlag >= 1 and cidFlag <= 2) or (cidFlag >= 6 and cidFlag <= 8):
            advice2 = '正解の解説番号(' + str(cid0) + ')と同じです。'
            delCheck2 = 0
        elif (cidFlag >= 9 and cidFlag <= 11):
            advice2 = '選択肢１の解説番号(' + str(cid1) + ')と同じです。'
            delCheck2 = 0
        else:
            delCheck2 = 1

        # comment3
        if cidFlag == 1 or cidFlag == 3 or cidFlag == 6 or cidFlag == 9 or cidFlag == 12 \
                or cidFlag == 26 or cidFlag == 28 or cidFlag == 31 or cidFlag == 33 or cidFlag == 45:
            advice3 = '正解の解説番号(' + str(cid0) + ')と同じです。'
            delCheck3 = 0
        elif cidFlag == 7 or cidFlag == 10 or cidFlag == 13 or cidFlag == 29 or cidFlag == 34:
            advice3 = '選択肢１の解説番号(' + str(cid1) + ')と同じです。'
            delCheck3 = 0
        elif cidFlag == 4 or cidFlag == 14:
            advice3 = '選択肢２の解説番号(' + str(cid2) + ')と同じです。'
            delCheck3 = 0
        else:
            delCheck3 = 1

        return render_template('del_check.html',
                                   user_id=user_id,
                                   qid=qid,
                                   question=question,
                                   answer=answer,
                                   choice1=choice1,
                                   choice2=choice2,
                                   choice3=choice3,
                                   cid0=cid0,
                                   comment0=comment0,
                                   cid1=cid1,
                                   cid2=cid2,
                                   cid3=cid3,
                                   comment1=comment1,
                                   comment2=comment2,
                                   comment3=comment3,
                                   delCheck1=delCheck1,
                                   delCheck2=delCheck2,
                                   delCheck3=delCheck3,
                                   advice1=advice1,
                                   advice2=advice2,
                                   advice3=advice3,
                                   retrieveFlag=retrieveFlag,
                                   firstFlag=firstFlag,
                               )
    elif(command == 'deletey'):
        qid = int(request.form.get('qid'))
        cid0 = int(request.form.get('cid0'))
        cid1 = int(request.form.get('cid1'))
        cid2 = int(request.form.get('cid2'))
        cid3 = int(request.form.get('cid3'))
        option0 = request.form.get('option0')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        sql = 'DELETE from knowledge_base where number = ' + str(qid) + ';'
        try:
            c.execute(sql)
            if option0 == 'on':
                sql = 'DELETE from comments_table where comment_id = ' + str(cid0) + ';'
                c.execute(sql)
            if option1 == 'on':
                sql = 'DELETE from comments_table where comment_id = ' + str(cid1) + ';'
                c.execute(sql)
            if option2 == 'on':
                sql = 'DELETE from comments_table where comment_id = ' + str(cid2) + ';'
                c.execute(sql)
            if option3 == 'on':
                sql = 'DELETE from comments_table where comment_id = ' + str(cid3) + ';'
                c.execute(sql)
            conn.commit()
        except:
            conn.close()
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。',
                                   )
        else:
            conn.close()
            message = "問題番号＝" + str(qid) + "を削除しました。"
            return render_template('success3.html',
                                   user_id=user_id,
                                   message=message,
                                   )
    elif (command == 'redraw'):
        user_id = request.form.get('user_id')
        qid = int(request.form.get('qid'))
        category = int(request.form.get('category'))
        area = int(request.form.get('area'))
        question = request.form.get('question')
        answer = request.form.get('answer')
        choice1 = request.form.get('choice1')
        choice2 = request.form.get('choice2')
        choice3 = request.form.get('choice3')
        commentFlag = request.form.get('commentFlag')
        cid0 = int(request.form.get('cid0'))
        cid1 = int(request.form.get('cid1'))
        cid2 = int(request.form.get('cid2'))
        cid3 = int(request.form.get('cid3'))
        comment0 = request.form.get('comment0')
        comment1 = request.form.get('comment1')
        comment2 = request.form.get('comment2')
        comment3 = request.form.get('comment3')
        advice0 = request.form.get('advice0')
        advice1 = request.form.get('advice1')
        advice2 = request.form.get('advice2')
        advice3 = request.form.get('advice3')
        retrieveFlag = request.form.get('retrieveFlag')
        firstFlag = request.form.get('firstFlag')
        sql1 = request.form.get('sql1')
        sql2 = request.form.get('sql2')
        sql3 = request.form.get('sql3')
        old_cid0 = int(request.form.get('old_cid0'))
        old_cid1 = int(request.form.get('old_cid1'))
        old_cid2 = int(request.form.get('old_cid2'))
        old_cid3 = int(request.form.get('old_cid3'))
        old_comment0 = request.form.get('old_comment0')
        old_comment1 = request.form.get('old_comment1')
        old_comment2 = request.form.get('old_comment2')
        old_comment3 = request.form.get('old_comment3')
        main_check = request.form.get('main_check')
        sub_check1 = request.form.get('sub_check1')
        sub_check2 = request.form.get('sub_check2')
        sub_check3 = request.form.get('sub_check3')
        if comment1 == "None":
            comment1 = ''
        if comment2 == "None":
            comment2 = ''
        if comment3 == "None":
            comment3 = ''
        #
        return render_template('question.html',
                               user_id=user_id,
                               qid = qid,
                               category = category,
                               area = area,
                               question = question,
                               answer = answer,
                               choice1 = choice1,
                               choice2 = choice2,
                               choice3 = choice3,
                               cid0 = cid0,
                               comment0 = comment0,
                               comment1 = comment1,
                               comment2 = comment2,
                               comment3 = comment3,
                               advice0 = advice0,
                               advice1 = advice1,
                               advice2 = advice2,
                               advice3 = advice3,
                               retrieveFlag = retrieveFlag,
                               firstFlag=firstFlag,
                               cid1 = cid1,
                               cid2 = cid2,
                               cid3 = cid3,
                               sql1 = sql1,
                               sql2 = sql2,
                               sql3 = sql3,
                               main_check = main_check,
                               sub_check1 = sub_check1,
                               sub_check2 = sub_check2,
                               sub_check3 = sub_check3,
                               commentFlag = commentFlag,
                               old_cid0=old_cid0,
                               old_cid1=old_cid1,
                               old_cid2=old_cid2,
                               old_cid3=old_cid3,
                               old_comment0=old_comment0,
                               old_comment1=old_comment1,
                               old_comment2=old_comment2,
                               old_comment3=old_comment3,
                               )
    elif (command == 'restart'):
        user_id = request.form.get('user_id')
        return render_template('maintenance.html',
                               user_id=user_id,
                               )
    else:
        return render_template('error2.html',
                               user_id=user_id,
                               error_message='要求を処理できませんでした。',
                               )


@maintenance_module.route('/commentEditor', methods=['POST'])
def commentEditor():
    user_id = int(request.form.get('user_id'))
    command = request.form.get('command')
    if (command == 'retrieve' or command == 'new'):
        if (command == 'retrieve'):
            try:
                cid = int(request.form.get('number'))
            except:
                return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='コメント番号が入力されていません。',
                                   )
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            sql = "SELECT COMMENT FROM comments_table WHERE " \
              "COMMENT_ID == " + str(cid) + ";"
            try:
                c.execute(sql)
                print("Success!")
            except Exception as e:
                return render_template('error2.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。',
                                   )
            else:
                items = c.fetchall()
                n = len(items)
                if n < 1:
                    return render_template('error3.html',
                                       user_id=user_id,
                                       error_message='該当するコメントはありません。',
                                       )
                comment = items[0][0]
            flag=1
            return render_template('commentEditor.html',
                               user_id=user_id,
                               cid = cid,
                               comment = comment,
                               flag=flag,
                               )
        else:
            cid = 0
            flag = 0
            comment = ""

            return render_template('commentEditor.html',
                               user_id=user_id,
                               cid = cid,
                               comment = comment,
                               flag=flag,
                               )
    elif (command == 'confirm'):
        cid = int(request.form.get('cid'))
        comment = request.form.get('comment','')
        if cid == 0:
            new_cid = int(request.form.get('new_cid'))
            if comment=='' or comment=='None':
                advice1 = 'コメントを入力してください。'
                return render_template('commentEditor.html',
                                       user_id=user_id,
                                       cid=cid,
                                       comment=comment,
                                       advice1=advice1,
                                       )
            if new_cid < 1001 :
                advice0 = '1001以上の数字を入力してください。'
                return render_template('commentEditor.html',
                                       user_id=user_id,
                                       cid=cid,
                                       comment=comment,
                                       advice0=advice0,
                                       )
            flag=0
        else:
            old_comment = request.form.get('old_comment')
            new_cid = cid
            flag = 1
            return render_template('cconfirm.html',
                                   user_id=user_id,
                                   cid=cid,
                                   new_cid=new_cid,
                                   comment=comment,
                                   old_comment=old_comment,
                                   flag=flag,
                                   )
        try:
            old_comment = getComment(new_cid)
            advice0 = 'この番号は既に使用されています。新規登録ではなく、コメント変更を選択してください。'
            return render_template('commentEditor.html',
                                   user_id=user_id,
                                   cid=new_cid,
                                   comment=comment,
                                   advice0=advice0,
                                   )
        except:
            flag = 0
            return render_template('cconfirm.html',
                                   user_id=user_id,
                                   cid=cid,
                                   new_cid=new_cid,
                                   comment=comment,
                                   flag=flag,
                                   )
    elif(command == 'update'):
        cid = int(request.form.get('cid'))
        flag = int(request.form.get('flag'))
        comment = request.form.get('comment')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        if flag != 0:
            sql = 'UPDATE comments_table SET COMMENT=? WHERE COMMENT_ID = ' + str(cid)
        else:
            # sql = 'INSERT INTO comments_table (COMMENT) VALUES (?)'
            sql = 'INSERT INTO comments_table ( comment_id, comment ) VALUES (?, ?)'
        try:
            if flag != 0:
                conn.execute(sql, [comment])
            else:
                conn.execute(sql, [cid, comment])
            conn.commit()
            conn.close()
            print("Success!")
        except Exception as e:
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。',
                                   )
        else:
            message = "コメント番号＝" + str(cid) + "で登録（更新）しました。"
            return render_template('success4.html',
                               user_id=user_id,
                               message = message,
                               )
    elif(command == 'delete'):
        cid = int(request.form.get('cid'))
        comment = request.form.get('comment')

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        sql = 'SELECT COMMENT from COMMENTS_TABLE where COMMENT_ID = ' + str(cid) + ';'
        try:
            c.execute(sql)
            result = c.fetchall()
        except:
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。',
                                   )
        message = '次のコメントを削除します。よろしいですか？'
        return render_template('del_check2.html',
                                   user_id=user_id,
                                   cid=cid,
                                   comment=comment,
                                   message=message,
                                   )
    elif(command == 'deletey'):
        cid = int(request.form.get('cid'))
        conn = sqlite3.connect(db_path)

        sql = 'DELETE from COMMENTS_TABLE where COMMENT_ID = ' + str(cid) + ';'
        try:
            conn.execute(sql)
            conn.commit()
            conn.close()
        except:
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。',
                                   )
        message = "コメント番号＝" + str(cid) + "を削除しました。"
        return render_template('success4.html',
                                   user_id=user_id,
                                   message=message,
                                   )
    else:
        return render_template('error2.html',
                               user_id=user_id,
                               error_message='要求を処理できませんでした。',
                               )

def checkCombination(cid1, cid2, cid3, cid4):
    if cid1==cid2 and cid1==cid3 and cid1==cid4:
        return 1
    elif cid1==cid2 and cid2==cid3 and cid2!=cid4:
        return 2
    elif cid1==cid2 and cid2!=cid3 and cid1==cid4:
        return 3
    elif cid1==cid2 and cid3==cid4 and cid1!=cid2:
        return 4
    elif cid1==cid2 and cid1!=cid3 and cid1!=cid4 and cid3!=cid4:
        return 5
    elif cid1!=cid2 and cid1==cid3 and cid1==cid4:
        return 6
    elif cid1!=cid2 and cid1==cid3 and cid2==cid4:
        return 7
    elif cid1!=cid2 and cid1==cid3 and cid1!=cid4 and cid2!=cid4:
        return 8
    elif cid1!=cid2 and cid2==cid3 and cid1==cid4:
        return 9
    elif cid1!=cid2 and cid2==cid3 and cid2==cid4:
        return 10
    elif cid1!=cid2 and cid2==cid3 and cid1!=cid4 and cid2!=cid4:
        return 11
    elif cid1!=cid2 and cid1!=cid3 and cid2!=cid3 and cid1==cid4:
        return 12
    elif cid1!=cid2 and cid1!=cid3 and cid2!=cid3 and cid2==cid4:
        return 13
    elif cid1!=cid2 and cid1!=cid3 and cid2!=cid3 and cid3==cid4:
        return 14
    else:
        return 15

def checkCombination3(cid1, cid2, cid3):

    if cid1==cid2 and cid1==cid3:
        return 1
    elif cid1==cid2 and cid1!=cid3:
        return 2
    elif cid1!=cid2 and cid1==cid3:
        return 3
    elif cid1!=cid2 and cid2==cid3:
        return 4
    else:
        return 1

