from constant import db_path, categoryNumber, categoryCode, DIFF_JST_FROM_UTC
import constant
from flask import Flask, request, render_template
import sqlite3, os, json, sys
import random
import datetime
import re


def _debug_print(*parts) -> None:
    message = "".join(str(part) for part in parts)
    try:
        print(message)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        print(message.encode(encoding, errors="replace").decode(encoding, errors="replace"))


def get_choice_count_for_category(category: int, default: int = 4) -> int:
    """Return 2/3/4 from YAML/config area metadata for the knowledge_base category."""
    try:
        from config_loader import get_areas

        for area in get_areas():
            if int(category) in [int(c) for c in area.get("categories", [])]:
                count = int(area.get("choice_count", default))
                if 2 <= count <= 4:
                    return count
                return default
    except Exception as exc:
        print(f"choice_count lookup failed for category={category}: {exc}")
    return default


def _answer_from_row(row, perm_value):
    """Map permutation slot (1..4) to A1..A4; 0 means unused choice."""
    idx = int(perm_value)
    if idx <= 0:
        return ""
    return row[idx]


def _cid_from_row(row, perm_value, cid_offset: int = 4):
    idx = int(perm_value)
    if idx <= 0:
        return 0
    return row[cid_offset + idx]


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
        _debug_print(f'質問 {self.q}')
        _debug_print(f'A. {self.a1}')
        _debug_print(f'B. {self.a2}')
        _debug_print(f'C. {self.a3}')
        _debug_print(f'D. {self.a4}')

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
    if not items:
        conn.close()
        return None, None, None

    for k, r in enumerate(items):
        for s in range(4):
            if ((int(idx[s])) == 1):
                q.crct = s
        else:
            pass

    q.q = r[0]
    q.a1 = _answer_from_row(r, idx[0])
    q.a2 = _answer_from_row(r, idx[1])
    q.a3 = _answer_from_row(r, idx[2])
    q.a4 = _answer_from_row(r, idx[3])
    q.cid1 = _cid_from_row(r, idx[0])
    q.cid2 = _cid_from_row(r, idx[1])
    q.cid3 = _cid_from_row(r, idx[2])
    q.cid4 = _cid_from_row(r, idx[3])
    q.choice_count = sum(1 for value in idx if int(value) != 0) or 4

    _debug_print('Question=', q.q)
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
            _debug_print('Question=', q.q)
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

def get_passage_settings_for_category(category: int):
    """Return passage-grouping settings from YAML area metadata, or None."""
    try:
        from config_loader import get_areas

        for area in get_areas():
            if int(category) not in [int(c) for c in area.get("categories", [])]:
                continue
            if not (area.get("passages") or area.get("passage_group")):
                return None
            return {
                "passages": int(area.get("passages", 2)),
                "group": str(area.get("passage_group", "flag")).lower(),
            }
    except Exception as exc:
        print(f"passage settings lookup failed for category={category}: {exc}")
    return None


# Reading passages use knowledge_base.FLAG in this reserved range only.
PASSAGE_FLAG_MIN = 101
PASSAGE_FLAG_MAX = 199


def is_passage_flag(flag) -> bool:
    """True when FLAG is reserved for Spanish reading passage grouping (101-199)."""
    if flag is None or flag == "":
        return False
    try:
        value = int(flag)
    except (TypeError, ValueError):
        return False
    return PASSAGE_FLAG_MIN <= value <= PASSAGE_FLAG_MAX


def order_passage_selection(
    groups: dict, passage_count: int, amount: int
) -> list | None:
    """Pick ``passage_count`` FLAG groups, sample ``amount`` questions, keep groups contiguous.

    ``groups`` maps passage key -> list of question NUMBERs.
    Any group size is allowed (e.g. 3 or 5 rows sharing the same FLAG).
    Only FLAG values in 101-199 are treated as passage groups.
    """
    eligible = {
        key: list(values)
        for key, values in groups.items()
        if values and is_passage_flag(key)
    }
    keys = list(eligible.keys())
    if len(keys) < passage_count:
        print(
            f"Not enough passages: have={len(keys)}, need={passage_count}"
        )
        return None

    chosen_keys = random.sample(keys, passage_count)
    pool_by_key = {key: list(eligible[key]) for key in chosen_keys}
    pool: list[int] = []
    for key in chosen_keys:
        pool.extend(int(n) for n in pool_by_key[key])

    if len(pool) < amount:
        print(
            f"Not enough passage questions: pool={len(pool)}, need={amount}, "
            f"passages={chosen_keys}"
        )
        return None

    selected = set(random.sample(pool, amount))
    random.shuffle(chosen_keys)

    ordered: list[int] = []
    for key in chosen_keys:
        picks = [int(n) for n in pool_by_key[key] if int(n) in selected]
        random.shuffle(picks)
        ordered.extend(picks)
    return ordered


def get_exam_candidates_by_passage_flag(amount, category, passage_count: int):
    """Select questions grouped by knowledge_base.FLAG (Spanish passage id)."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT NUMBER, FLAG FROM knowledge_base WHERE CATEGORY = ?",
        (int(category),),
    )
    rows = cursor.fetchall()
    conn.close()

    groups: dict[int, list[int]] = {}
    for number, flag in rows:
        if not is_passage_flag(flag):
            continue
        flag_key = int(flag)
        groups.setdefault(flag_key, []).append(int(number))

    print(
        f"passage candidates: category={category}, groups={len(groups)}, "
        f"flag_range={PASSAGE_FLAG_MIN}-{PASSAGE_FLAG_MAX}, "
        f"passages={passage_count}, amount={amount}"
    )
    return order_passage_selection(groups, passage_count, amount)


def getExamCandidate(amount, category, level, mode):
    if amount <= 0 or amount > constant.MaxQuestions:
        return None

    passage = get_passage_settings_for_category(int(category))
    if passage and passage.get("group") == "flag":
        candidate = get_exam_candidates_by_passage_flag(
            amount, category, passage["passages"]
        )
        if candidate is None:
            print(
                f"Passage selection failed: category={category}, "
                f"amount={amount}, passages={passage['passages']}"
            )
        return candidate

    condition = ""
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
    index = combination(cnt, amount)
    if index is None:
        print(f"Not enough questions: category={category}, have={cnt}, need={amount}")
        return None
    print('組み合わせ列={0}'.format(index))

    candidate = []
    for i in range(amount):
        candidate.append(glist[index[i]])
    return candidate

def combination(total, select):
    ns = []
    if total < select:
        return None
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

    # start is the lower bound of the category range for this single-question exam.
    choice_n = get_choice_count_for_category(int(start))
    permutation = GetRandom(choice_n)
    a1 = _answer_from_row(items[m], permutation[0])
    a2 = _answer_from_row(items[m], permutation[1])
    a3 = _answer_from_row(items[m], permutation[2])
    a4 = _answer_from_row(items[m], permutation[3])
    perm = "".join(str(value) for value in permutation)

    crct = 0
    for i in range(4):
        if permutation[i] == 1:
            crct = i
    cid = items[m][5]
    num = items[m][6]

    return q, a1, a2, a3, a4, crct, cid, num, perm, choice_n

def getQuestionFromNum(number,permutation):

    items = [['' for i in range(1)] for j in range(6)]
    a = ['' for i in range(4)]
    cid = [0 for i in range(4)]

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
    # permutation may be a digit string "2130" or a sequence of ints.
    if isinstance(permutation, str):
        slots = [int(ch) for ch in permutation[:4]]
        while len(slots) < 4:
            slots.append(0)
    else:
        slots = [int(permutation[i]) if i < len(permutation) else 0 for i in range(4)]

    for i in range(4):
        a[i] = _answer_from_row(items[0], slots[i])
        cid[i] = _cid_from_row(items[0], slots[i])

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

    examType = None
    try:
        from config_loader import get_exam_entry

        entry = get_exam_entry(int(category))
        if entry:
            examType = entry.get("exam_type") or entry.get("title")
    except Exception:
        examType = None

    if not examType:
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
    num_categories = len(categoryNumber)
    question_ids = [0 for i in range(constant.MaxQuestions)]
    selectArea = [0 for i in range(max(constant.NumOfArea, 6))]
    selectCategory = [0 for i in range(num_categories + 1)]
    index = [0 for i in range(num_categories + 1)]
    genlist = [[] for _ in range(num_categories + 1)]

    total = amount;
    if total < 0 or total > constant.MaxQuestions:
        return None
    assign = [0 for i in range(constant.MaxQuestions)]

    total = assignQuestions(total, assign, category)

    if total == -1:
        return None

    print("Total:" + str(total))

# 選択された「エリア（領域）の個数」と「カテゴリの個数」を算出する
    arealist = ''
    for i in range(total):
        matched = False
        for j in range(num_categories):
            if assign[i] == categoryNumber[j]:
                arealist = arealist + categoryCode[j]
                selectCategory[j] += 1
                matched = True
                print('arealist=' + arealist)

                if j < constant.NumOfCategory1:
                    selectArea[0] += 1
                elif j < constant.NumOfCategory2:
                    selectArea[1] += 1
                elif j < constant.NumOfCategory3:
                    selectArea[2] += 1
                elif j < constant.NumOfCategory4:
                    selectArea[3] += 1
                elif j < constant.NumOfCategory5:
                    selectArea[4] += 1
                else:
                    selectArea[5] += 1
                break
        if not matched:
            print(f"Unknown category in assignment: {assign[i]}")
            return None
    #        print('i={0}'.format(i))

    print('arealist=' + arealist)
    business_status = 0

    # ユーザーIDをチェックする（ログインいしているか、有料か無料か）

    for i in range(num_categories):
        if selectCategory[i] != 0:
            candidates = getExamCandidate(
                selectCategory[i], categoryNumber[i], level, business_status
            )
            if not isinstance(candidates, list):
                print(
                    f"Failed to build exam for category {categoryNumber[i]} "
                    f"(count={selectCategory[i]})"
                )
                return None
            genlist[i] = candidates
        else:
            genlist[i] = []

    for i in range(total):
        if i >= len(arealist):
            print(f"arealist too short: index={i}, length={len(arealist)}")
            return None
        j = categoryCode.find(arealist[i])
        if j < 0 or not isinstance(genlist[j], list):
            print(f"Invalid category mapping at question {i}: char={arealist[i]!r}, j={j}")
            return None
        if index[j] >= len(genlist[j]):
            print(
                f"Not enough prepared questions for category index {j} "
                f"(need index {index[j]}, have {len(genlist[j])})"
            )
            return None
        question_ids[i] = genlist[j][index[j]]
        index[j] += 1

    print('リスト={0}'.format(question_ids))

    # デバッグ・コード：　演習ID（question_ids[i]）が０なら、異常なので埋め合わせる
    #    if(question_ids[i]==0):
    #        print("question_ids[" + i + "]:" + question_ids[i])
    #        print("*************** ERROR ****************\n")

    examlist = ""

    for i in range(total):
        # 選択肢の配列を決定する（2/3/4択は YAML areas.choice_count）
        choice_n = get_choice_count_for_category(int(assign[i]))
        permutation = GetRandom(choice_n)
        print('permutation={0}'.format(permutation))

        examlist = examlist + "(" + str(question_ids[i]) + ":" \
                   + str(permutation[0]) + "," + str(permutation[1]) + "," \
                   + str(permutation[2]) + "," + str(permutation[3]) + ")"

        print(examlist)

    return examlist, arealist


def GetRandom(choice_count: int = 4):
    """Return a length-4 permutation. Unused slots (beyond choice_count) are 0.

    Example for 3-choice: [2, 1, 3, 0]
    """
    count = int(choice_count)
    if count < 2:
        count = 2
    if count > 4:
        count = 4

    if count == 4:
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
        return list(data[random.randint(0, 23)])

    pool = list(range(1, count + 1))
    random.shuffle(pool)
    while len(pool) < 4:
        pool.append(0)
    return pool

def assignQuestions(amount, assign, category:int):
    if (amount > constant.MaxQuestions or amount < 0):
        return -1

    try:
        from exam_plan_loader import resolve_assign_categories

        categories = resolve_assign_categories(category)
        if categories:
            if len(categories) != amount:
                print(
                    f"adjusting amount from {amount} to {len(categories)} "
                    f"for category {category}"
                )
                amount = len(categories)
            for i, cat in enumerate(categories):
                assign[i] = int(cat)
            return amount
    except Exception as exc:
        print(f"exam plan slot resolution failed: {exc}")

    print(f"Error! No exam plan assignment for category {category}")
    return -1

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



