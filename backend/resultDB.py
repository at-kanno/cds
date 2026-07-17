from constant import db_path, categoryCode
import constant
import sqlite3, os, json

class ResultInfo:
    def __init__(self, user_id, exam_id, arealist, answerlist, resultlist):
        self.user_id = user_id
        self.exam_id = exam_id
        self.arealist = arealist
        self.answerlist = answerlist
        self.resultlist = resultlist

# 試験結果を格納する
def putResult(user_id, exam_id, amount, arealist, answerlist, resultlist, correct, rate, usedTime):
    categoryNumber = [0 for i in range(constant.NumOfCategory)]
    categoryScore = [0 for i in range(constant.NumOfCategory)]
    categoryPercent = [0 for i in range(constant.NumOfCategory)]

    areaNumber = [0 for i in range(constant.NumOfArea)]
    areaScore = [0 for i in range(constant.NumOfArea)]
    areaPercent = [0 for i in range(constant.NumOfArea)]

# 領域ごとに採点する
    for i, c in enumerate(arealist):
        if i >= len(resultlist):
            flag = 0
        elif resultlist[i] == '1':
            flag = 1
        else:
            flag = 0
        n = categoryCode.find(c)
        if n == -1:
            continue
        categoryNumber[n] += 1
        categoryScore[n] = categoryScore[n] + flag
        if n < constant.NumOfCategory1:
            areaNumber[0] += 1
            areaScore[0] = areaScore[0] + flag
        elif n < constant.NumOfCategory2:
            areaNumber[1] += 1
            areaScore[1] = areaScore[1] + flag
        elif n < constant.NumOfCategory3:
            areaNumber[2] += 1
            areaScore[2] = areaScore[2] + flag
        elif n < constant.NumOfCategory4:
            areaNumber[3] += 1
            areaScore[3] = areaScore[3] + flag
        elif n < constant.NumOfCategory5:
            areaNumber[4] += 1
            areaScore[4] = areaScore[4] + flag
        elif n < constant.NumOfCategory6:
            areaNumber[5] += 1
            areaScore[5] = areaScore[5] + flag
        elif n < constant.NumOfCategory7:
            areaNumber[6] += 1
            areaScore[6] = areaScore[6] + flag
        else:
            areaNumber[7] += 1
            areaScore[7] = areaScore[7] + flag

    for i in range(constant.NumOfCategory):
        if categoryNumber[i] != 0:
            categoryPercent[i] = round(categoryScore[i] / categoryNumber[i] * 100, 2)

    for i in range(constant.NumOfArea):
        if areaNumber[i] != 0:
            areaPercent[i] = round(areaScore[i] / areaNumber[i] * 100, 2)

    half1 = half2 = 0
    length = round(len(resultlist) / 2)
    if length > 0:
        for i in range(length):
            if resultlist[i] == '1':
                half1 += 1
        for i in range(length, len(resultlist)):
            if resultlist[i] == '1':
                half2 += 1
        half1 = round(half1 / length * 100, 2)
        second_len = len(resultlist) - length
        half2 = round(half2 / second_len * 100, 2) if second_len > 0 else 0.0
    else:
        half1 = half2 = 0.0

    res = res_correct = 0

    for i, c in enumerate(answerlist):
        if c != '0' :
            res += 1                              # 解答数
    for i, c in enumerate(resultlist):
        if c == '1' :
            res_correct += 1                     # 正答数
    if res == 0:
        res_ratio = 0
    else:
        res_ratio = round(res_correct / res * 100, 2)          # 解答した問題に対する正答率
    total_time = amount * constant.TimePerQuestion
    remain_time = total_time - usedTime          # 残り時間
    remain_time_rate = remain_time / total_time  # 残り時間の割合

    # last3_answered                   # 最後の３問への解答数
    # last3_result                     # 最後の３問の採点結果
    last3_result = resultlist[-3:]
    last3 = 0
    for i, c in enumerate(last3_result):
        if c == '1':
            last3 += 1
    last3 = round(last3 / 3 * 100, 2)               # 最後の３問の正答率）

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "DROP TABLE RESULT_TABLE;"
#    c.execute(sql)
    sql = "CREATE TABLE IF NOT EXISTS RESULT_TABLE ( EXAM_ID INTEGER, USER_ID INTEGER, EXAM_TYPE LONG VARCHAR,"\
        + "TOTAL INTEGER, TOTAL_R INTEGER, TOTAL_P FLOAT," \
        + "HALF1 FLOAT, HALF2 FLOAT, RESPONSE INTEGER, CORRECT_RES_RATE FLOAT," \
        + "REMAIN_TIME INTEGER, REMAIN_TIME_RATE FLOAT, LAST3 INTEGER," \
        + "C1_NUMBER INTEGER, C1_SCORE INTEGER, C1_PERCENT FLOAT," \
        + "C2_NUMBER INTEGER, C2_SCORE INTEGER, C2_PERCENT FLOAT," \
        + "C3_NUMBER INTEGER, C3_SCORE INTEGER, C3_PERCENT FLOAT," \
        + "C4_NUMBER INTEGER, C4_SCORE INTEGER, C4_PERCENT FLOAT," \
        + "C5_NUMBER INTEGER, C5_SCORE INTEGER, C5_PERCENT FLOAT," \
        + "C6_NUMBER INTEGER, C6_SCORE INTEGER, C6_PERCENT FLOAT," \
        + "C7_NUMBER INTEGER, C7_SCORE INTEGER, C7_PERCENT FLOAT," \
        + "C8_NUMBER INTEGER, C8_SCORE INTEGER, C8_PERCENT FLOAT," \
        + "C9_NUMBER INTEGER, C9_SCORE INTEGER, C9_PERCENT FLOAT," \
        + "C10_NUMBER INTEGER, C10_SCORE INTEGER, C10_PERCENT FLOAT," \
        + "C11_NUMBER INTEGER, C11_SCORE INTEGER, C11_PERCENT FLOAT," \
        + "C12_NUMBER INTEGER, C12_SCORE INTEGER, C12_PERCENT FLOAT," \
        + "C13_NUMBER INTEGER, C13_SCORE INTEGER, C13_PERCENT FLOAT," \
        + "C14_NUMBER INTEGER, C14_SCORE INTEGER, C14_PERCENT FLOAT," \
        + "C15_NUMBER INTEGER, C15_SCORE INTEGER, C15_PERCENT FLOAT," \
        + "C16_NUMBER INTEGER, C16_SCORE INTEGER, C16_PERCENT FLOAT," \
        + "C17_NUMBER INTEGER, C17_SCORE INTEGER, C17_PERCENT FLOAT," \
        + "C18_NUMBER INTEGER, C18_SCORE INTEGER, C18_PERCENT FLOAT," \
        + "C19_NUMBER INTEGER, C19_SCORE INTEGER, C19_PERCENT FLOAT," \
        + "C20_NUMBER INTEGER, C20_SCORE INTEGER, C20_PERCENT FLOAT," \
        + "C21_NUMBER INTEGER, C21_SCORE INTEGER, C21_PERCENT FLOAT," \
        + "C22_NUMBER INTEGER, C22_SCORE INTEGER, C22_PERCENT FLOAT," \
        + "C23_NUMBER INTEGER, C23_SCORE INTEGER, C23_PERCENT FLOAT," \
        + "C24_NUMBER INTEGER, C24_SCORE INTEGER, C24_PERCENT FLOAT," \
        + "C25_NUMBER INTEGER, C25_SCORE INTEGER, C25_PERCENT FLOAT," \
        + "C26_NUMBER INTEGER, C26_SCORE INTEGER, C26_PERCENT FLOAT," \
        + "C27_NUMBER INTEGER, C27_SCORE INTEGER, C27_PERCENT FLOAT," \
        + "C28_NUMBER INTEGER, C28_SCORE INTEGER, C28_PERCENT FLOAT," \
        + "C29_NUMBER INTEGER, C29_SCORE INTEGER, C29_PERCENT FLOAT," \
        + "C30_NUMBER INTEGER, C30_SCORE INTEGER, C30_PERCENT FLOAT," \
        + "C31_NUMBER INTEGER, C31_SCORE INTEGER, C31_PERCENT FLOAT," \
        + "C32_NUMBER INTEGER, C32_SCORE INTEGER, C32_PERCENT FLOAT," \
        + "C33_NUMBER INTEGER, C33_SCORE INTEGER, C33_PERCENT FLOAT," \
        + "C34_NUMBER INTEGER, C34_SCORE INTEGER, C34_PERCENT FLOAT," \
        + "C35_NUMBER INTEGER, C35_SCORE INTEGER, C35_PERCENT FLOAT," \
        + "C36_NUMBER INTEGER, C36_SCORE INTEGER, C36_PERCENT FLOAT," \
        + "C37_NUMBER INTEGER, C37_SCORE INTEGER, C37_PERCENT FLOAT," \
        + "C38_NUMBER INTEGER, C38_SCORE INTEGER, C38_PERCENT FLOAT," \
        + "C39_NUMBER INTEGER, C39_SCORE INTEGER, C39_PERCENT FLOAT," \
        + "C40_NUMBER INTEGER, C40_SCORE INTEGER, C40_PERCENT FLOAT," \
        + "C41_NUMBER INTEGER, C41_SCORE INTEGER, C41_PERCENT FLOAT," \
        + "C42_NUMBER INTEGER, C42_SCORE INTEGER, C42_PERCENT FLOAT," \
        + "C43_NUMBER INTEGER, C43_SCORE INTEGER, C43_PERCENT FLOAT," \
        + "C44_NUMBER INTEGER, C44_SCORE INTEGER, C44_PERCENT FLOAT," \
        + "C45_NUMBER INTEGER, C45_SCORE INTEGER, C45_PERCENT FLOAT," \
        + "C46_NUMBER INTEGER, C46_SCORE INTEGER, C46_PERCENT FLOAT," \
        + "C47_NUMBER INTEGER, C47_SCORE INTEGER, C47_PERCENT FLOAT," \
        + "C48_NUMBER INTEGER, C48_SCORE INTEGER, C48_PERCENT FLOAT," \
        + "C49_NUMBER INTEGER, C49_SCORE INTEGER, C49_PERCENT FLOAT," \
        + "C50_NUMBER INTEGER, C50_SCORE INTEGER, C50_PERCENT FLOAT," \
        + "A1_NUMBER INTEGER, A1_SCORE INTEGER, A1_PERCENT FLOAT," \
        + "A2_NUMBER INTEGER, A2_SCORE INTEGER, A2_PERCENT FLOAT," \
        + "A3_NUMBER INTEGER, A3_SCORE INTEGER, A3_PERCENT FLOAT," \
        + "A4_NUMBER INTEGER, A4_SCORE INTEGER, A4_PERCENT FLOAT," \
        + "A5_NUMBER INTEGER, A5_SCORE INTEGER, A5_PERCENT FLOAT," \
        + "A6_NUMBER INTEGER, A6_SCORE INTEGER, A6_PERCENT FLOAT," \
        + "A7_NUMBER INTEGER, A7_SCORE INTEGER, A7_PERCENT FLOAT," \
        + "A8_NUMBER INTEGER, A8_SCORE INTEGER, A8_PERCENT FLOAT," \
        + "A9_NUMBER INTEGER, A9_SCORE INTEGER, A9_PERCENT FLOAT," \
        + "A10_NUMBER INTEGER, A10_SCORE INTEGER, A10_PERCENT FLOAT);"
    c.execute(sql)

    sql = "INSERT INTO RESULT_TABLE( USER_ID, EXAM_ID, TOTAL, TOTAL_R, TOTAL_P ";
    for i in range(1,constant.NumOfCategory+1):
        sql = sql + ", C"+ str(i) +"_NUMBER, C"+ str(i) +"_SCORE, C"+ str(i) +"_PERCENT";

    for i in range(1,constant.NumOfArea+1):
        sql = sql + ", A" + str(i) + "_NUMBER, A" + str(i) + "_SCORE, A" + str(i) + "_PERCENT";

    sql = sql + ", HALF1, HALF2, RESPONSE, CORRECT_RES_RATE, REMAIN_TIME, REMAIN_TIME_RATE, LAST3" \
          + ") VALUES (" + str(user_id)  + ", " + str(exam_id) + ", " + str(amount) +", " + str(correct) +", " + str(rate) + " ";
    for i in range(constant.NumOfCategory):
        sql = sql + ", " + str(categoryNumber[i]) + ", " + str(categoryScore[i]) + ", " + str(categoryPercent[i]);

    for i in range(constant.NumOfArea):
        sql = sql + ", " + str(areaNumber[i]) + ", " + str(areaScore[i]) + ", " + str(areaPercent[i]);

    sql = sql + ", " + str(half1) + ", " + str(half2) + ", " + str(res) + ", " + str(res_ratio) + ", "\
          + str(remain_time) + ", " + str(remain_time_rate) + ", " + str(last3) + " )"

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")
    conn.commit()

# 試験結果を抽出する
def getResult(exam_id):

    categoryNumber = [0 for i in range(constant.NumOfCategory)]
    categoryScore = [0 for i in range(constant.NumOfCategory)]
    categoryPercent = [0 for i in range(constant.NumOfCategory)]

    areaNumber = [0 for i in range(constant.NumOfArea)]
    areaScore = [0 for i in range(constant.NumOfArea)]
    areaPercent = [0 for i in range(constant.NumOfArea)]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT EXAM_ID, USER_ID, EXAM_TYPE, TOTAL, TOTAL_R, TOTAL_P,' \
        ' HALF1, HALF2, RESPONSE, CORRECT_RES_RATE, REMAIN_TIME, REMAIN_TIME_RATE, LAST3, '
    for i in range(constant.NumOfCategory):
        sql += 'C' + str(i+1) + '_NUMBER, C' + str(i+1) + '_SCORE, C' + str(i+1) + '_PERCENT, '
    for i in range(constant.NumOfArea):
        sql += 'A' + str(i+1) + '_NUMBER, A' + str(i+1) + '_SCORE, A' + str(i+1) + '_PERCENT, '

    sql = sql + 'EXAM_ID FROM RESULT_TABLE WHERE EXAM_ID = ' + str(exam_id)

    print(sql)
    if c.execute(sql):
        print("Success!")
    else:
        print("Error!")
    items = c.fetchall()
    user_id = items[0][1]
    total = items[0][3]
    correct = items[0][4]
    rate = items[0][5]

    for i in range(constant.NumOfCategory):
        a = items[0][i * 3 + constant.NumOfHeader]
        b = items[0][i * 3 + constant.NumOfHeader+1]

        categoryNumber[i] = int(a)
        categoryScore[i] = int(b)
        if categoryNumber[i] != 0:
            categoryPercent[i] = categoryScore[i] / categoryNumber[i] * 100

    for i in range(constant.NumOfArea):
        areaNumber[i] = items[0][(i+constant.NumOfCategory)*3+constant.NumOfHeader]
        areaScore[i] = items[0][(i+constant.NumOfCategory)*3+constant.NumOfHeader+1]
        areaPercent[i] = items[0][(i+constant.NumOfCategory)*3+constant.NumOfHeader+2]

    return categoryNumber, categoryScore, categoryPercent, areaNumber, \
           areaScore, areaPercent

#   コメントIDからコメントを得る
def getComment(cid):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "SELECT  COMMENT FROM COMMENTS_TABLE" \
          + " WHERE COMMENT_ID = " + str(cid) + ";"
    c.execute(sql)
    items = c.fetchall()
    conn.close()

    return items[0][0]

# コメント文を作成する
def makeComments(exam_id):

    categoryNumber = [0 for i in range(constant.NumOfCategory)]
    categoryScore = [0 for i in range(constant.NumOfCategory)]
    categoryPercent = [0 for i in range(constant.NumOfCategory)]

    areaNumber = [0 for i in range(constant.NumOfArea)]
    areaScore = [0 for i in range(constant.NumOfArea)]
    areaPercent = [0 for i in range(constant.NumOfArea)]

    result_data = [0 for i in range(9)]

    area, score, percent, user_id, half1, half2, res, correct_rate, \
    remain_time, remain_time_rate, last3 = getResultData(exam_id)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = 'SELECT TOTAL, TOTAL_P, TOTAL_R'
    for i in range(constant.NumOfArea):
        sql += ' ,A' + str(i+1) + '_NUMBER, A' + str(i+1) + '_SCORE, A' + str(i+1) + '_PERCENT'
    sql = sql + ' FROM RESULT_TABLE WHERE EXAM_ID = ' + str(exam_id)
    c.execute(sql)
    items = c.fetchall()

    total = items[0][0]
    total_p = items[0][1]
    total_r = items[0][2]

    for i in range(constant.NumOfArea):
        areaNumber[i] = items[0][i*3+3]
        areaScore[i] = items[0][i*3+4]
        areaPercent[i] = items[0][i*3+5]

    sql = 'SELECT '
    for i in range(constant.NumOfCategory):
        sql += 'C' + str(i+1) + '_NUMBER, C' + str(i+1) + '_SCORE, C' + str(i+1) + '_PERCENT, '
    sql = sql + 'EXAM_ID FROM RESULT_TABLE WHERE EXAM_ID = ' + str(exam_id)
    c.execute(sql)
    items = c.fetchall()

#
    for i in range(constant.NumOfCategory):
        a = items[0][i * 3]
        b = items[0][i * 3 + 1]

        categoryNumber[i] = int(a)
        categoryScore[i] = int(b)
        if categoryNumber[i] != 0:
            categoryPercent[i] = categoryScore[i] / categoryNumber[i] * 100

    weakArea = [0 for i in range(constant.NumOfArea)]
    weakCategory = [0 for i in range(constant.NumOfCategory)]
    weakAreaList1 = ""
    weakAreaList2 = ""
    weakCategoryList1 = ""
    weakCategoryList2 = ""

#
    for i in range(constant.NumOfCategory):
        if categoryNumber[i] != 0:
            if categoryPercent[i] == 0:
                weakCategory[i] = 1
                if( weakCategoryList1 != ""):
                    weakCategoryList1 = ',' + weakCategoryList1 + str(i)
                else:
                    weakCategoryList1 = weakCategoryList1 + str(i)
            elif categoryPercent[i] < 50:
                weakCategory[i] = 2
                if( weakCategoryList2 != ""):
                    weakCategoryList2 = ',' + weakCategoryList2 + str(i)
                else:
                    weakCategoryList2 = weakCategoryList2 + str(i)
            else:
                weakCategory[i] = 0

    n = 0
    for i in range(constant.NumOfArea):
        if areaNumber[i] != 0:
            areaPercent[i] = areaScore[i] / areaNumber[i]
            if areaPercent[i] == 0:
                weakArea[i] = 1
                n += 1
                weakAreaList1 = weakAreaList1 + str(i)
            elif areaPercent[i] < 50:
                weakArea[i] = 2
                weakAreaList2 = weakAreaList2 + str(i)
            else:
                weakArea[i] = 0

# 選択された領域を明かにする
    select = 0
    j = 0
    for i in range(constant.NumOfArea):
        if areaNumber[i] != 0:
            j += 1
            select = i+1
# j = 1 でなければ、全領域を指定しているはず
    if j != 1:
        select = 0

    if total_p >= 90:
        cid =500
    elif total_p >= 75:
        cid = 501
    elif total_p >= 65:
        cid = 502
    elif total_p >= 40:
        cid = 503
    elif total_p >= 20:
        cid = 504
    elif correct_rate < 60:
        cid = 510
    else:
        cid = 505

    comment = "<br>" + getComment(cid) + "<br>"

# 残り時間の量で試験への取り組みを判別する
    if remain_time_rate > 0.5:
        cid = 511
        comment = comment + getComment(cid) + "<br>"
# 最後の３問の成績で試験への取り組みを判別する
    if last3 == 0:
        cid = 520
        comment = comment + getComment(cid) + "<br>"
# 前半と後半の成績の差で試験への取り組みを判別する
    if half1 - half2 > 50:
        cid = 521
        comment = comment + getComment(cid) + "<br>"
# 解答数をベースとした正答率で理解度を判別する
    if correct_rate >=85:
        cid = 514
        comment = comment + getComment(cid) + "<br>"
    elif correct_rate > 70:
        cid = 513
        comment = comment + getComment(cid) + "<br>"

    if correct_rate < 30:
        cid = 512
        comment = comment + getComment(cid) + "<br>"

#   解答結果の分析とコメント選択
#   全領域選択の場合
    if total == constant.MaxQuestions or total == 10:
        has_low = any(x < constant.THRESHOLD_LOW for x in areaPercent[:constant.NumOfArea])
        has_high = any(x > constant.THRESHOLD_HIGH for x in areaPercent[:constant.NumOfArea])

        #   すべての領域で THRESHOLD_LOW % 以下の正答率の場合
        if all(areaPercent[n] < constant.THRESHOLD_LOW for n in range(constant.NumOfArea)):
            cid = 538
        #   全領域で THRESHOLD_HIGH % 以上、正解している場合
        elif all(areaPercent[n] > constant.THRESHOLD_HIGH for n in range(constant.NumOfArea)):
            cid = 590
        #   THRESHOLD_LOW % 以下の正答率の領域があった場合
        elif has_low:
            #   かつ、THRESHOLD_HIGH % 以上の正答率の領域もある場合
            if has_high:
                cid = 591
            #   かつ、THRESHOLD_HIGH % 　以上正答した領域がない場合
            else:
                cid = 537
        #   すべての領域が 50 % 以上の正答率であり、80 % を超える領域もある場合
        elif any(areaPercent[n] > constant.THRESHOLD_HIGH for n in range(constant.NumOfArea)):
            cid = 592
        # すべての領域が 50 % 以上、79 % 以下の正答率である場合
        else:
            cid = 594
#   各領域の正答率から判断した分析結果をコメントする
        comment = comment + getComment(cid) + "<br><br>"

#   弱点を指摘する
        list = ""
        if (cid == 537 or cid == 538 or cid == 591) and n != 0:

            j = 0
            for i, n in enumerate(weakArea) :
                if n == 1:
                    if j != 0:
                        list = list + '、'
                    list = list + '「' + constant.areaname[i][0] + '」'
                    j += 1
            list = list + getComment(539)
        comment = comment + list
        comment = comment + "<BR>"

#   出題領域を選択している場合
    else:
        if select != 0 :
            comment = comment + '「' + constant.areaname[select-1][0] + '」'
            cid = 589
            comment = comment + getComment(cid) + "<BR>"

        #   不得意領域を指摘する
        m = 0
        list = ""
        for i in range(constant.NumOfCategory):
            if weakCategory[i] == 1:
                if m != 0:
                    list = list + "、"
                m = m + 1
                list = list + '「' + constant.practice2[i] + '」'
        #   不得意領域がない場合
        if m == 0:
            cid = 595
            comment = comment + getComment(cid)
        else:
            comment = comment + list + getComment(539)
    comment = comment + "<BR>"
    return comment

def getResultData(exam_id):

    area = [0 for i in range(constant.NumOfArea+constant.NumOfCategory+3)]
    score = [0 for i in range(constant.NumOfArea+constant.NumOfCategory+3)]
    percent = [0 for i in range(constant.NumOfArea+constant.NumOfCategory+3)]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = 'SELECT EXAM_ID, USER_ID, EXAM_TYPE, TOTAL, TOTAL_R, TOTAL_P,'
    for i in range(constant.NumOfCategory):
        sql += 'C' + str(i+1) + '_NUMBER, C' + str(i+1) + '_SCORE, C' + str(i+1) + '_PERCENT, '
    for i in range(constant.NumOfArea):
        sql += 'A' + str(i+1) + '_NUMBER, A' + str(i+1) + '_SCORE, A' + str(i+1) + '_PERCENT, '

    sql = sql + 'HALF1, HALF2, RESPONSE, CORRECT_RES_RATE, REMAIN_TIME, REMAIN_TIME_RATE, LAST3 '
    sql = sql + 'FROM RESULT_TABLE WHERE EXAM_ID = ' + str(exam_id)

    c.execute(sql)
    items = c.fetchall()

    user_id = items[0][1]
    area[constant.NumOfArea+constant.NumOfCategory] = items[0][3]
    score[constant.NumOfArea+constant.NumOfCategory] = items[0][4]
    percent[constant.NumOfArea+constant.NumOfCategory] = items[0][5]
    for i in range(constant.NumOfArea+constant.NumOfCategory):
        area[i]= items[0][i*3+constant.NumOfHeader]
        score[i]= items[0][i*3+constant.NumOfHeader+1]
        percent[i]= items[0][i*3+constant.NumOfHeader+2]
    half1 = items[0][(constant.NumOfArea+constant.NumOfCategory)*3+6]
    half2 = items[0][(constant.NumOfArea+constant.NumOfCategory)*3+7]
    res = items[0][(constant.NumOfArea+constant.NumOfCategory)*3+8]
    correct_rate = items[0][(constant.NumOfArea+constant.NumOfCategory)*3+9]
    remain_time = items[0][(constant.NumOfArea+constant.NumOfCategory)*3+10]
    remain_time_rate = items[0][(constant.NumOfArea+constant.NumOfCategory)*3+11]
    last3 = items[0][(constant.NumOfArea+constant.NumOfCategory)*3+12]

    conn.close()
    return area, score, percent, user_id, half1, half2, res, correct_rate, \
           remain_time, remain_time_rate, last3

def getUserResultList(user_id):

    n = 0
    userlist = []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = 'SELECT USER_TABLE.LASTNAME, AMOUNT, SCORE,'\
       'RATE, START_TIME, EXAM_TYPE, '\
       'USER_TABLE.MAIL_ADR FROM EXAM_TABLE INNER JOIN USER_TABLE ON '\
       'EXAM_TABLE.USER_ID = USER_TABLE.USER_ID '
    sql = sql + 'where USER_TABLE.USER_ID = ' + str(user_id) + \
          ' AND EXAM_TYPE != "' + constant.examType12 + '" and score != ""'

    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        conn.close()
        return items, n
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False, n


def getStartTime(exam_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT START_TIME FROM EXAM_TABLE where EXAM_ID = ' + str(exam_id)
    try:
        c.execute(sql)
        items = c.fetchall()

        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getUserResultList1(user_id):

    userlist = []
    n = 0
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = 'SELECT USER_TABLE.LASTNAME, USER_TABLE.STATUS, AMOUNT, SCORE,'\
       'RATE, START_TIME, EXAM_TYPE, '\
       'USER_TABLE.MAIL_ADR FROM EXAM_TABLE INNER JOIN USER_TABLE ON '\
       'EXAM_TABLE.USER_ID = USER_TABLE.USER_ID '
    sql = sql + 'where USER_TABLE.USER_ID = ' + str(user_id) + \
          ' AND EXAM_TYPE = "' + constant.examType11 + '" and score != ""'

    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        conn.close()
        return items, n
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False, n

def getUserResultList2(user_id):

    n = 0
    userlist = []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = 'SELECT USER_TABLE.LASTNAME, USER_TABLE.STATUS, '\
       'RATE, START_TIME, EXAM_TYPE, '\
       'USER_TABLE.MAIL_ADR FROM EXAM_TABLE INNER JOIN USER_TABLE ON '\
       'EXAM_TABLE.USER_ID = USER_TABLE.USER_ID '
    sql = sql + 'where USER_TABLE.USER_ID = ' + str(user_id) + \
          ' AND EXAM_TYPE = "' + constant.examType12 + '" and score != ""'

    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        conn.close()
        return items, n
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False, n

