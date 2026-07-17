from constant import db_path
import constant
from flask import Flask, session, render_template, request, Blueprint
import sqlite3, json, hashlib, base64, os
import random
import string
import time, datetime
import re

user_module = Blueprint("user", __name__, static_folder='./static')

@user_module.route('/setpassword', methods=['POST'])
def setpassword():
    user_id = int(request.form.get('user_id'))
    id = str(request.form.get('id'))
    name = getLoginName(id)
    return render_template('setpassword.html',
                           user_id=user_id,
                           name=name,
                           id=id,
                           )


@user_module.route('/setpasswd', methods=['POST'])
def setpasswd():
    user_id = int(request.form.get('user_id'))
    xname = str(request.form.get('name'))  #
    name = xname.lower()                   # ログイン名は使っていない
    id = request.form.get('id')
    password = request.form.get('password')
    if setPassword(id, password):
        return render_template('success.html',
                               message='成功しました。',
                               user_id=user_id)
    else:
        return render_template('error2.html',
                               error_message='エラーが発生しました。',
                               user_id=user_id
                               )


@user_module.route('/resetpassword', methods=['POST'])
def resetpassword():
    user_id = int(request.form.get('user_id'))
    name = getLoginName(user_id)
    password = getLoginPassword(user_id)
    return render_template('resetpassword.html',
                           user_id=user_id,
                           name=name,
                           password=password,
                           )


@user_module.route('/resetpasswd', methods=['POST'])
def resetpasswd():
    user_id = int(request.form.get('user_id'))
    name = request.form.get('name')
    hashed_password = request.form.get('password')
    new_password = request.form.get('new_password')
    old_password = request.form.get('old_password')

#    if password == old_password:
    if password_verify(old_password, hashed_password):
        status = setPassword(user_id, new_password)
    else:
        return render_template('error2.html',
                               error_message='現在のパスワードが入力されていない。もしくは、正しくありません。',
                               user_id=user_id
                               )
    if status:
        return render_template('success.html',
                               message='成功しました。',
                               user_id=user_id)
    else:
        return render_template('error2.html',
                               error_message='エラーが発生しました。',
                               user_id=user_id
                               )

# パスワードからハッシュを生成する
def password_hash(password):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac('sha256',
                                 password.encode('utf-8'), salt, 10000)
    return base64.b64encode(salt + digest).decode('ascii')

# パスワードが正しいかを検証する
def password_verify(password, hash):
    b = base64.b64decode(hash)
    salt, digest_v = b[:16], b[16:]
    digest_n = hashlib.pbkdf2_hmac('sha256',
                                   password.encode('utf-8'), salt, 10000)
    return digest_n == digest_v

# 新規ユーザーを追加
def addUser(lastname, firstname, lastyomi, firstyomi, tel1, tel2, tel3, zip1, zip2,\
            company, department, prefecture, city, town, building, status, password, mail_adr, beginDate, endDate):

    mail_adrX = mail_adr.lower()
    hashedPassword = password_hash(password)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'INSERT INTO USER_TABLE (lastname, firstname, lastyomi, firstyomi,'\
          'tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town,'\
          'building, status, password, mail_adr, begin, end) VALUES ("'\
           + lastname + '", "' + firstname + '", "' + lastyomi + '", "' + firstyomi + '", "'\
           + str(tel1) + '", "' + str(tel2) + '", "' + str(tel3) + '", "' + str(zip1) + '", "' + str(zip2) + '", "'\
           + company + '", "' + department + '", "' + str(prefecture) + '", "' + city + '", "' + town + '", "'\
           + building + '", ' + str(status) + ', "' + hashedPassword + '", "' + mail_adrX + '", "'\
           + beginDate + '", "' + endDate + '")'
    try:
        # INSERT
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

# 既存ユーザー情報を更新
def modifyUser(id, lastname, firstname, lastyomi, firstyomi, tel1, tel2, tel3, zip1, zip2,\
            company, department, prefecture, city, town, building, status, password, mail_adr, beginDate, endDate):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'UPDATE USER_TABLE SET lastname="' + lastname + '", firstname="' + firstname +\
          '", lastyomi="' + lastyomi +'", firstyomi="' + firstyomi + \
          '", tel1="' + tel1 + '", tel2="' + tel2 + '", tel3="' + tel3 +\
          '", zip1="' + zip1 + '", zip2="' + zip2 + '", company="' + company +\
          '", department="' + department + '", prefecture="' + prefecture + \
          '", city="' + city + '", town="' + town + '", building="' + building + \
          '", mail_adr="' + mail_adr + '", begin="' + beginDate + '", end="' + endDate + \
          '" where user_id = ' + id
    try:
        # UPDATE
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

# ログインできるか確認
def check_login(id, password):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT USER_ID, PASSWORD FROM USER_TABLE WHERE MAIL_ADR = "' + id + '"'
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
        user_id = items[0][0]
        password2 = items[0][1]
        if password_verify(password, password2):
#            sql = 'UPDATE USER_TABLE SET STAGE = 1 WHERE USER_ID = ' + str(user_id)
#            c.execute(sql)
#            conn.commit()
            conn.close()
            return user_id
        else:
            conn.close()
            return False
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getUserInfo(user_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT lastname, firstname, lastyomi, firstyomi, ' \
          'tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, ' \
          'town, building ,mail_adr ,status, begin, end ' \
          'FROM USER_TABLE WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        return items
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getStage(user_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT STAGE FROM USER_TABLE WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def setStage(user_id, stage):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'UPDATE USER_TABLE SET STAGE = ' + str(stage) + \
          ' WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getUserList():

    userlist = []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT USER_ID, LASTNAME, MAIL_ADR FROM USER_TABLE'
    try:
        c.execute(sql)
        items = c.fetchall()

        conn.close()
        return items
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def deleteUser(user_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'DELETE FROM USER_TABLE where USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def compareAddrss( address1, address2):
    upper1 = address1.upper()
    upper2 = address2.upper()
    if(upper1 == upper2):
        return True
    else:
        return False

def setPassword(user_id, password):
    hashed_password = password_hash(password)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'UPDATE USER_TABLE SET PASSWORD = "' + hashed_password \
          + '" WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def resetPassword(user_id, old_password, new_password):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql1 = 'SELECT PASSWORD FROM USER_TABLE WHERE USER_ID = ' + str(user_id)
    sql2 = 'UPDATE USER_TABLE SET PASSWORD = "' + new_password + '" WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql1)
        items = c.fetchall()
        conn.close()
        if items[0][0] != old_password :
            return False
        c.execute(sql2)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getLoginName(id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT MAIL_ADR FROM USER_TABLE where USER_ID = ' + str(id)
    try:
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False


def getLoginPassword(id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT PASSWORD FROM USER_TABLE where USER_ID = ' + str(id)
    try:
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getStatus(user_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT STATUS FROM USER_TABLE where USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return 0
        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def setStatus(user_id, level):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = 'UPDATE USER_TABLE SET STATUS = ' + str(level) + \
          ' WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False
    conn.commit()
    conn.close()
    return True

def rankUp(user_id, level, type):

    old_status = getStatus(user_id)
    flag = 0

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT STATUS FROM USER_TABLE where USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n >= 1:
            rank = items[0][0]
        else:
            rank = 0    # STATUS値が設定されていない場合、初期状態とみなす (2025/12/18)
        if n < 1:
            status = 1
        elif level == 0 and n < 10:     # 模擬試験表示
            status = 10
        elif level >= 1 and rank < 20:  # 模擬試験カウント = 1
            status = 20
        elif level >= 1 and rank < 23:  # 模擬試験カウント < 5
            status = rank + 1
        elif level >=1 and rank < 30:   # 模擬試験カウント >= 5 → 修了試験表示
            status = 30
        elif type == constant.examType11:  # 模擬試験:グレード3で模擬試験を受けても、何も変わらない
            status = rank
        elif level < 2:                 # 修了試験は75点以上
            status = rank
        elif rank == 30 and type == constant.examType12:  # 修了試験:修了試験カウント = 1
            status = 31
            flag = 2
        else:                           # 修了試験合格
            status = 40
            flag = 3
        sql = 'UPDATE USER_TABLE SET STATUS = ' + str(status) +\
              ' WHERE USER_ID = ' + str(user_id)
        c.execute(sql)
        conn.commit()
        conn.close()
        return status, flag
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False, flag

def rankDown(user_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    status = 30
    sql = 'UPDATE USER_TABLE SET STATUS = 30'\
              ' WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getMailadress(user_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT LASTNAME, FIRSTNAME, MAIL_ADR FROM USER_TABLE where USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
        conn.close()
        return items
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def checkPeriod(user_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT BEGIN, END FROM USER_TABLE where USER_ID = ' + str(user_id)

    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
        conn.close()
        beginDate = items[0][0]
        endDate = items[0][1]

        date = datetime.date.today()
        strToday = date.strftime('%Y%m%d')
        if items[0][0] != '0':
            beginDate = re.sub('-', '',  items[0][0])
            if strToday < beginDate:
                return 99

        if items[0][1] != '0':
            endDate = re.sub('-', '',  items[0][1])
            if strToday > endDate:
                return 101
        return 1
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def makePassword():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
    # print("Random alphanumeric String is:", result_str)
    return result_str

def checkMailaddress(mail_address):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT USER_ID FROM USER_TABLE where MAIL_ADR = "' + str(mail_address) + '"'
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getPrivilege(user_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT PRIVILEGE FROM USER_TABLE where USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return 0
        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def setPrivilege(user_id, priv):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = 'UPDATE USER_TABLE SET PRIVILEGE = ' + str(priv) + \
          ' WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False
    conn.commit()
    conn.close()
    return True
