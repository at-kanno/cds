from constant import db_path, cc_email, bcc_email, from_email, cset, servername, \
     END_MESSAGE, FIRST_MAIL, LAST_MAIL
import constant
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import ssl
import sqlite3

def sendMail(to_name, to_email, message):

    rcpt = cc_email.split(",") + bcc_email.split(",") + [to_email]

# MIMETextを作成
    if message == '合格です。':
        message = to_name + '様\n\n' + constant.PASS3_MESSAGE_1 \
                  + constant.PASS3_MESSAGE_2 + constant.PASS3_MESSAGE_3 \
                  + constant.PASS3_MESSAGE_4 + constant.PASS3_MESSAGE_5 \
                  + END_MESSAGE
        subject = constant.FIRST_MAIL
    else:
        message = to_name + '様\n\n' + constant.NEW_ACCOUNT_MESSAGE1_1 + constant.NEW_ACCOUNT_MESSAGE1_2 \
                  + constant.LOGIN_URL + constant.NEW_ACCOUNT_MESSAGE1_3 \
                  + message + constant.NEW_ACCOUNT_MESSAGE2_1 \
                  + constant.NEW_ACCOUNT_MESSAGE2_2 + constant.PORT_NO \
                  + constant.NEW_ACCOUNT_MESSAGE2_3 + constant.NEW_ACCOUNT_MESSAGE2_4 \
                  + constant.NEW_ACCOUNT_MESSAGE2_5 + constant.PORT_NO \
                  + constant.NEW_ACCOUNT_MESSAGE2_6 + constant.NEW_ACCOUNT_MESSAGE2_7 \
                  + constant.NEW_ACCOUNT_MESSAGE2_8 + constant.NEW_ACCOUNT_MESSAGE2_9 \
                  + END_MESSAGE
        subject = constant.LAST_MAIL

    msg = MIMEText(message, 'plain', cset)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Cc"] = cc_email

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT MAIL_ADR, PASSWORD FROM USER_TABLE where USER_ID = 5;'
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

    account = items[0][0]
    password = items[0][1]

# サーバを指定する
    server = smtplib.SMTP_SSL(servername, 465, context=ssl.create_default_context())
    server.set_debuglevel(True)
    if server.has_extn('STARTTLS'):
        server.starttls()

# 認証を行う
    server.login(account, password)
# メールを送信する
    sendToList = to_email.split(',')
    server.sendmail(from_email, rcpt, msg.as_string())
# 閉じる
    return server.quit()
