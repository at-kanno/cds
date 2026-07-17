from constant import db_path, categoryNumber, categoryCode, DIFF_JST_FROM_UTC
import constant
from flask import Flask, request, render_template
import sqlite3, os, json
import random
import datetime
import re

class Question:
    def __init__(self, category, level, q, a1, a2, a3, a4, correct, cid1, cid2, cid3, cid4):
        self.category = category
        self.level = level
        self.q = q
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.correct = correct
        self.cid1 = cid1
        self.cid2 = cid2
        self.cid3 = cid3
        self.cid4 = cid4

    def show(self):
        print(f'質問 {self.q}')
        print(f'A. {self.a1}')
        print(f'B. {self.a2}')
        print(f'C. {self.a3}')
        print(f'D. {self.a4}')

class QuestionList:
    def __init__(self):
        self.data = []

    def add(self, question):
        self.data.append(question)

# 演習IDから問題を取得する
def getQuestion(examlist, q_no):

    print(examlist)
    s1 = examlist.strip('()')
    print(s1)
    s2 = s1.replace(')(', ',')
    print(s2)
    examlist2 = re.split('[:,]', s2)
    print(examlist2)

    number = examlist2[(q_no-1) * 5]
    idx = examlist2[(q_no-1)*5+1:(q_no) * 5]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = Question

    sql = "SELECT Q,A1,A2,A3,A4,CID1, CID2, CID3, CID4 FROM knowledge_base WHERE NUMBER = " + str(number)
    try:
        c.execute(sql)
    except:
        return None, None, None

    items = c.fetchall()

    for k, r in enumerate(items):
        for s in range(4):
            if ((int(idx[s])) == 1):
                q.crct = s
        else:
            pass

    q.q = r[0]
    q.a1 = r[int(idx[0])]
    q.a2 = r[int(idx[1])]
    q.a3 = r[int(idx[2])]
    q.a4 = r[int(idx[3])]
    q.cid1 = r[4+int(idx[0])]
    q.cid2 = r[4+int(idx[1])]
    q.cid3 = r[4+int(idx[2])]
    q.cid4 = r[4+int(idx[3])]

    print('Question=' + q.q)
    return q, conn, c

# 演習IDと解答からコメントIDを取得する
def getCommentId(examlist, q_no, canswer, uanswer):
    print(examlist)
    s1 = examlist.strip('()')
    print(s1)
    s2 = s1.replace(')(', ',')
    print(s2)
    examlist2 = re.split('[:,]', s2)
    print(examlist2)

    number = examlist2[(q_no - 1) * 5]
    idx = examlist2[(q_no - 1) * 5 + 1:(q_no) * 5]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = Question

    sql = "SELECT CID1, CID2, CID3, CID4 FROM knowledge_base WHERE NUMBER = " + str(number)
    c.execute(sql)
    items = c.fetchall()

    i = int(idx[uanswer - 1]) - 1
    if uanswer == 0 or uanswer == canswer:
        return items[0][0]
    else:
        return items[0][i]

# 演習IDから問題を取得する
def getQuestions(exam_id, qlist):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = Question
    #    qlist = QuestionList()

    sql = "SELECT  CDATE, CTIME, CATEGORY, LEVEL, AMOUNT," \
          + " EXAMLIST, AREALIST FROM EXAM_TABLE" \
          + " WHERE EXAM_ID = " + str(exam_id) + ";"

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")

    items = c.fetchall()
    cdate = items[0][0]
    ctime = items[0][1]
    category = items[0][2]
    level = items[0][3]
    amount = items[0][4]
    examlist = items[0][5]
    arealist = items[0][6]

    print(examlist)
    s1 = examlist.strip('()')
    print(s1)
    s2 = s1.replace(')(', ',')
    print(s2)
    examlist2 = re.split('[:,]', s2)
    print(examlist2)

    idlist = examlist2[::5]
    idlistnum = len(idlist)
    idxlist = [['' for i in range(4)] for j in range(idlistnum)]
    for i in range(0, idlistnum):
        idxlist[i] = examlist2[i * 5 + 1:i * 5 + 5]
    print(idxlist[0])

    for j in range(0, idlistnum):
        sql = "SELECT Q,A1,A2,A3,A4,CID1,CID2,CID3,CID4 FROM knowledge_base WHERE NUMBER = " \
              + str(idlist[j])
        c.execute(sql)

        items = c.fetchall()

        for k, r in enumerate(items):
            for s in range(4):
                if ((int(idxlist[k][s])) == 1):
                    crct = s
                else:
                    pass

            q = Question(
                category, level, r[0],
                r[int(idxlist[k][0])],
                r[int(idxlist[k][1])],
                r[int(idxlist[k][2])],
                r[int(idxlist[k][3])],
                crct,
                r[4+int(idxlist[k][0])],
                r[4+int(idxlist[k][1])],
                r[4+int(idxlist[k][2])],
                r[4+int(idxlist[k][3])],
                )
            print('Question=' + q.q)
            qlist[j] = q

    conn.close()
    return idlistnum

def getExamlist(exam_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = Question

    sql = "SELECT  CDATE, CTIME, CATEGORY, LEVEL, AMOUNT," \
          + " EXAMLIST, AREALIST, ANSWERLIST FROM EXAM_TABLE" \
          + " WHERE EXAM_ID = " + str(exam_id) + ";"

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")

    items = c.fetchall()
    cdate = items[0][0]
    ctime = items[0][1]
    category = items[0][2]
    level = items[0][3]
    amount = items[0][4]
    examlist = items[0][5]
    arealist = items[0][6]
    answerlist = items[0][7]

    return examlist, arealist, answerlist

def getExamCandidate(amount, category, level, mode):
    dt_now = datetime.datetime.now()
    condition = ""

    if (amount <= 0):
        return -1
    elif (amount > constant.MaxQuestions):
        return -1
    else:
        pass

    categoryStr = "CATEGORY = " + str(category)

    if (category != 0):
        condition = " WHERE " + categoryStr + " "

    sql = "SELECT NUMBER FROM knowledge_base " + str(condition)

    # データベースから値を取得
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(sql)
    items = c.fetchall()
    glist = []

    for i, r in enumerate(items):
        glist.append(r[0])
        print(str(glist))
    conn.close()

    print("候補数=" + str(len(glist)))
    print("要求数=" + str(amount))

    cnt = len(glist)
    index = []
    index = combination(cnt, amount)
    print('組み合わせ列={0}'.format(index))

    candidate = []
    try:
        for i in range(amount):
            candidate.append(glist[index[i]])
    except:
        return 'NotEnough'
    return (candidate)

def combination(total, select):
    ns = []
    if total < select:
        return render_template('error.html',
                               error_message='内部エラーが発生しました。')
    while len(ns) < select:
        n = random.randint(0, total - 1)
        print('n=' + str(n))
        if not n in ns:
            ns.append(n)
    return ns

def getCorrectList( examlist ):

    correctlist = ""
    s1 = examlist.strip('()')
    print(s1)
    s2 = s1.replace(')(', ',')
    print(s2)
    examlist2 = re.split('[:,]', s2)
    print(examlist2)
    for i,n in enumerate(examlist2):
        if i%5 == 0:
            cnt = 0
            continue
        else:
            cnt += 1
            if(n != '1'):
                continue
            else:
                correctlist = correctlist + str(cnt)
    return correctlist

def getQuestionFromCategory(start, end):

    items = [['' for i in range(100)] for j in range(6)]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = Question

    sql = "SELECT Q,A1,A2,A3,A4,CID1,NUMBER FROM knowledge_base WHERE "\
            "CATEGORY >= " + str(start) + " AND CATEGORY <= " + str(end) + ";"

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")

    items = c.fetchall()
    n = len(items)
    if n < 1:
        return render_template('error.html',
                               error_message='内部エラーが発生しました。')

    m = 0
    m = random.randint(0, n-1)
    q = items[m][0]

    permutation = GetRandom()
    a1 = items[m][permutation[0]]
    a2 = items[m][permutation[1]]
    a3 = items[m][permutation[2]]
    a4 = items[m][permutation[3]]
    perm = str(permutation[0]) + str(permutation[1]) + str(permutation[2]) + str(permutation[3])

    for i in range(4):
        if (permutation[i] == 1):
            crct = i
    cid = items[m][5]
    num = items[m][6]

    return q,a1,a2,a3,a4,crct,cid,num, perm

def getQuestionFromNum(number,permutation):

    items = [['' for i in range(1)] for j in range(6)]
    a = ['' for i in range(4)]
    cid = ['' for i in range(4)]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = Question

    sql = "SELECT Q,A1,A2,A3,A4,CID1,CID2,CID3,CID4 FROM knowledge_base WHERE "\
            "NUMBER == " + str(number) + ";"

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")

    items = c.fetchall()
    n = len(items)
    if n < 1:
        return False

    q = items[0][0]
    for i in range(4):
        idx = int(permutation[i])
        a[i] = items[0][idx]
        cid[i] = int(items[0][idx+4])

    return q,a[0],a[1],a[2],a[3],cid[0],cid[1],cid[2],cid[3], conn, c

def saveExam(user, category, level, amount, examlist, arealist):

    if os.name != 'nt':
        now = datetime.datetime.now() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
    else:
        now = datetime.datetime.now()

    cdate = now.strftime("%Y-%m-%d")
    ctime = now.strftime("%H:%M:%S")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

#   演習テーブルを再構成したい場合
    sql = "DROP TABLE EXAM_TABLE;"
#    c.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS EXAM_TABLE (" \
          + " EXAM_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
          + " USER_ID INTEGER, CDATE TIMESTAMP, CTIME TIMESTAMP," \
          + " CATEGORY INTEGER, LEVEL INTEGER, AMOUNT INTEGER," \
          + " EXAMLIST LONG VARCHAR, AREALIST LONG VARCHAR," \
          + " ANSWERLIST LONG VARCHAR, RESULTLIST LONG VARCHAR, EXAM_TYPE LONG VARCHAR," \
          + " SCORE INTEGER, RATE FLOAT, TOTAL_TIME INTEGER, USED_TIME INTEGER," \
          + " START_TIME TIMESTAMP);"

    c.execute(sql)

    if category == '10':
        examType = constant.examType1
    elif category == '20':
        examType = constant.examType2
    elif category == '30':
        examType = constant.examType3
    elif category == '40':
        examType = constant.examType4
    elif category == '50':
        examType = constant.examType5
    elif category == '60':
        examType = constant.examType10
    elif category == '70':
        examType = constant.examType11
    elif category == '80':
        examType = constant.examType12
    else:
        examType = constant.examType99

    answerlist = '0' * amount

    sql = 'INSERT INTO EXAM_TABLE( USER_ID, CDATE, CTIME,'\
          + 'CATEGORY, LEVEL, AMOUNT, EXAMLIST, AREALIST, ANSWERLIST, EXAM_TYPE ) VALUES ("'\
          + str(user) + '", "' + cdate + '" , "' + ctime + '" , ' \
          + str(category) + ', ' + str(level) + ', ' + str(amount) + ',"' \
          + examlist + '", "' + arealist + '", "' + answerlist + '", "' + examType + '");'

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")
    conn.commit()

    sql = 'SELECT EXAM_ID FROM EXAM_TABLE WHERE USER_ID = ' \
          + str(user) + ' AND CDATE = "' + cdate + '" AND CTIME = "' + ctime + '";';

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")
    items = c.fetchall()
    conn.close()

    print(items[0][0])
    return (items[0][0])

def makeExam2(userid, amount, category: int, level, time, arealist):
    print('userid={0},amount={1}, category={2}, level={3},\
          time={4}, arealist={5}'.format(userid, amount, \
                                         category, level, time, arealist))
    list = [0 for i in range(constant.MaxQuestions)]
    selectArea = [0 for i in range(constant.NumOfArea)]
    selectCategory = [0 for i in range(constant.NumOfCategory+1)]
    index = [0 for i in range(constant.NumOfCategory+1)]
    genlist = [[0 for i in range(5)] for j in range(constant.NumOfCategory+1)]

    total = amount;
    if total < 0 or total > constant.MaxQuestions:
        return 0
    assign = [0 for i in range(constant.MaxQuestions)]

    total = assignQuestions(total, assign, category)

    if total == -1:
        return 0

    print("Total:" + str(total))

# 選択された「エリア（領域）の個数」と「カテゴリの個数」を算出する
    arealist = ''
    for i in range(total):
        for j in range(constant.NumOfCategory):
            #            print( 'categoryNumber[{0}])={1}'.format( j, categoryNumber[j]))
            if (assign[i] == categoryNumber[j]):
                arealist = arealist + categoryCode[j]
                selectCategory[j] += 1
                print('arealist=' + arealist)

                if (j < constant.NumOfCategory1):
                    selectArea[0] += 1
                elif (j < constant.NumOfCategory2):
                    selectArea[1] += 1
                elif (j < constant.NumOfCategory3):
                    selectArea[2] += 1
                elif (j < constant.NumOfCategory4):
                    selectArea[3] += 1
                elif (j < constant.NumOfCategory5):
                    selectArea[4] += 1
                else:
                    selectArea[5] += 1
                break
            else:
                pass
    #        print('i={0}'.format(i))

    print('arealist=' + arealist)
    business_status = 0

    # ユーザーIDをチェックする（ログインいしているか、有料か無料か）

    for i in range(constant.NumOfCategory):
        if (selectCategory[i]!=0):
            genlist[i] = getExamCandidate(selectCategory[i], categoryNumber[i], level, business_status)
        else:
            genlist[i] = '0'

    for i in range(total):
        j = categoryCode.find(arealist[i])
        list[i] = genlist[j][index[j]]
        index[j] += 1

    print('リスト={0}'.format(list))

    # デバッグ・コード：　演習ID（list[i]）が０なら、異常なので埋め合わせる
    #    if(list[i]==0):
    #        print("list[" + i + "]:" + list[i])
    #        print("*************** ERROR ****************\n")

    examlist = ""

    for i in range(amount):
        # 選択肢の配列を決定する
        permutation = GetRandom()
        print('permutation={0}'.format(permutation))

        examlist = examlist + "(" + str(list[i]) + ":" \
                   + str(permutation[0]) + "," + str(permutation[1]) + "," \
                   + str(permutation[2]) + "," + str(permutation[3]) + ")"

        print(examlist)

    return examlist, arealist


def GetRandom():
    data = [
        [1, 2, 3, 4],
        [1, 2, 4, 3],
        [1, 3, 2, 4],
        [1, 3, 4, 2],
        [1, 4, 2, 3],
        [1, 4, 3, 2],
        [2, 1, 3, 4],
        [2, 1, 4, 3],
        [2, 3, 1, 4],
        [2, 3, 4, 1],
        [2, 4, 1, 3],
        [2, 4, 3, 1],
        [3, 2, 1, 4],
        [3, 2, 4, 1],
        [3, 1, 2, 4],
        [3, 1, 4, 2],
        [3, 4, 2, 1],
        [3, 4, 1, 2],
        [4, 2, 3, 1],
        [4, 2, 1, 3],
        [4, 3, 2, 1],
        [4, 3, 1, 2],
        [4, 1, 2, 3],
        [4, 1, 3, 2],
    ]

    n = random.randint(0, 23)
    #    print(n)
    return data[n]

def assignQuestions(amount, assign, category:int):
    if (amount > constant.MaxQuestions or amount < 0):
        return -1

# CDS (2022.12.27)
    if category == 10:
        assign[0] = 11
        assign[1] = 13
        assign[2] = 11
        assign[3] = 12
        assign[4] = 11
    elif category == 20:
        assign[0] = 21
        assign[1] = 21
        assign[2] = 21
        assign[3] = 21
        assign[4] = 21
    elif category == 30:
        assign[0] = 34
        assign[1] = 31
        assign[2] = 32 + (random.randint(0, 1)*2)
        assign[3] = 33
        assign[4] = 32
    elif category == 40:
        assign[0] = 41
        assign[1] = 42
        assign[2] = 41
        assign[3] = 42
        assign[4] = 41
    elif category == 60 or category == 70 or category == 80:
        assign[0] = 31    # バリューストリーム（新サービスSVS）
        assign[1] = 21    # 情報と技術
        assign[2] = 11    # 組織の文化
        assign[3] = 42    # 調達の手段
        assign[4] = 34    # ユーザサポート・プラクティス
        assign[5] = 12    # シフトレフト
        assign[6] = 33    # バリューストリーム（ユーザサポート）
        assign[7] = 41    # 活動の調整
        assign[8] = 13    # 人材の計画と管理
        assign[9] = 32    # 新サービス・プラクティス
        if amount == 40:
            assign[10] = 21    # 情報と技術(2)
            assign[11] = 32    # 新サービス・プラクティス(2)
            assign[12] = 41    # 活動の調整(2)
            assign[13] = 42    # 調達の手段(2)
            assign[14] = 34    # ユーザサポート・プラクティス(2)
            assign[15] = 11    # 組織の文化(2)
            assign[16] = 12    # 組織変更の管理
            assign[17] = 41    # 活動の調整(3)
            assign[18] = 33    # バリューストリーム（ユーザサポート）(2)
            assign[19] = 21    # 情報と技術(3)
            assign[20] = 31    # バリューストリーム（新サービスSVS）(2)
            assign[21] = 13    # 人材の計画と管理(2)
            assign[22] = 32    # 新サービス・プラクティス(3)
            assign[23] = 13    # 人材の計画と管理(3)
            assign[24] = 31    # バリューストリーム（新サービスSVS）(3)
            assign[25] = 11    # 組織の文化(3)
            assign[26] = 42    # 調達の手段(3)
            assign[27] = 34    # ユーザサポート・プラクティス(3)
            assign[28] = 12    # シフトレフト（2）
            assign[29] = 32    # 新サービス・プラクティス(4)
            assign[30] = 41    # 活動の調整(4)
            assign[31] = 34    # ユーザサポート・プラクティス(4)
            assign[32] = 42    # 調達の手段(4)
            assign[33] = 33    # バリューストリーム（ユーザサポート）(3)
            assign[34] = 11    # 組織の文化(4)
            assign[35] = 13    # 人材の計画と管理(4)
            assign[36] = 32    # 新サービス・プラクティス(5)
            assign[37] = 21    # 情報と技術(4)
            assign[38] = 41    # 活動の調整(5)
            assign[39] = 34    # ユーザサポート・プラクティス(5)
    else:
        print("Error!")
        return -1

    return amount

def stringToButton(s):
    if(s == ""):
        return ""
    if ',' in s:
        numlist = s.split(',')
        xxx = ""
        for i, m in enumerate(numlist):
            if '-' in m:
                n = m.lstrip('-')
                xxx = xxx + '<button type=submit style="color:red" name="command" value="' + n + '">' + n + '</button>'
            else:
                xxx = xxx + '<button type=submit style="color:black" name="command" value="' + m + '">' + m + '</button>'
        return xxx
    elif '-' in s:
        n = s.lstrip('-')
        return '<button type=submit style="color:red" name="command" value="' + n + '">' + n + '</button>'
    else:
        return '<button type=submit style="color:black" name="command" value="' + s + '">' + s + '</button>'



