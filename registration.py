from constant import db_path, prefec
import sqlite3, csv
from flask import Flask, render_template, request, Blueprint
from users import checkMailaddress, makePassword, addUser, modifyUser
from mail import sendMail

regist_module = Blueprint("regist", __name__, static_folder='./static')

@regist_module.route('/registration', methods=['POST'])
def registration():
    user_id = int(request.form['user_id'])

    lastname = request.form.get('lastname')
    if lastname is None:
        lastname = ''
    firstname = request.form.get('firstname')
    if firstname is None:
        firstname = ''
    lastyomi = request.form.get('lastyomi')
    if lastyomi is None:
        lastyomi = ''
    firstyomi = request.form.get('firstyomi')
    if firstyomi is None:
        firstyomi = ''
    tel1 = request.form.get('tel1')
    if tel1 is None:
        tel1 = ''
    tel2 = request.form.get('tel2')
    if tel2 is None:
        tel2 = ''
    tel3 = request.form.get('tel3')
    if tel3 is None:
        tel3 = ''
    company = request.form.get('company')
    if company is None:
        company = ''
    department = request.form.get('department')
    if department is None:
        department = ''
    zip1 = request.form.get('zip1')
    if zip1 is None:
        zip1 = ''
    zip2 = request.form.get('zip2')
    if zip2 is None:
        zip2  = ''
    prefecture = request.form.get('prefecture')
    city = request.form.get('city')
    if city is None:
        city = ''
    town = request.form.get('town')
    if town is None:
        town = ''
    building = request.form.get('building')
    if building is None:
        building = ''
    mail_adr = request.form.get('mail_adr')
    if mail_adr is None:
        mail_adr = ''
    retype = request.form.get('retype')
    if retype is None:
        retype = ''
    error_no = 0

    return render_template('registration.html',
                           lastname=lastname,
                           firstname=firstname,
                           lastyomi=lastyomi,
                           firstyomi=firstyomi,
                           tel1=tel1,
                           tel2=tel2,
                           tel3=tel3,
                           company=company,
                           department=department,
                           zip1=zip1,
                           zip2=zip2,
                           prefecture=prefecture,
                           prefec=prefec,
                           #                           pref = pref,
                           city=city,
                           town=town,
                           building=building,
                           mail_adr=mail_adr,
                           retype=retype,
                           user_id=user_id,
                           error_no=error_no,
                           )


@regist_module.route('/confirmation', methods=['POST'])
def confirmation():
    user_id = int(request.form.get('user_id'))
    command = request.form.get('command')

#    error_no = int(request.form.get('error_no'))
    error_no = 0

    if command == 'modify':
        id = int(request.form.get('id'))
    else:
        id = 0
    lastname = request.form.get('lastname')
    firstname = request.form.get('firstname')
    lastyomi = request.form.get('lastyomi')
    firstyomi = request.form.get('firstyomi')
    tel1 = request.form.get('tel1')
    tel2 = request.form.get('tel2')
    tel3 = request.form.get('tel3')
    company = request.form.get('company')
    department = request.form.get('department')
    zip1 = request.form.get('zip1')
    zip2 = request.form.get('zip2')
    prefecture = request.form.get('prefecture')
    city = request.form.get('city')
    town = request.form.get('town')
    building = request.form.get('building')
    mail_adr = request.form.get('mail_adr')
    retype = request.form.get('retype')

    autoPassword =request.form.get('autoPassword')
    if autoPassword == 'on':
        ap = 'Checked'
    else:
        ap = ''
    beginDate = str(request.form.get('beginDate'))
    endDate = str(request.form.get('endDate'))

    if beginDate is None or beginDate=='':
        pass
    elif endDate is None or endDate=='':
        pass
    else:
        begin,tmp = beginDate.split('T', 1)
        fin,tmp = endDate.split('T', 1)
        if begin > fin:
            error_no = 20

    if firstname == "" or lastname == "":
        error_no = 11
    if mail_adr == "" or retype == "":
        error_no = 12
    if mail_adr != retype:
        error_no = 1
    mail_adrX = mail_adr.lower()
    if command == "register":
        if checkMailaddress(mail_adrX):
            error_no = 13
    if error_no != 0:
        # エラー処理
        if prefecture != "":
            try:
                pref = prefec.index(prefecture)
            except:
                pref = 0
        if id == 0:
            return render_template('registration.html',
                                   lastname=lastname,
                                   firstname=firstname,
                                   lastyomi=lastyomi,
                                   firstyomi=firstyomi,
                                   tel1=tel1,
                                   tel2=tel2,
                                   tel3=tel3,
                                   company=company,
                                   department=department,
                                   zip1=zip1,
                                   zip2=zip2,
                                   prefecture=prefecture,
                                   prefec=prefec,
                                   pref = pref,
                                   city=city,
                                   town=town,
                                   building=building,
                                   beginDate=beginDate,
                                   endDate=endDate,
                                   mail_adr=mail_adr,
                                   retype=retype,
                                   user_id=user_id,
                                   error_no=error_no,
                                   )

        else:
            return render_template('modification.html',
                                   lastname=lastname,
                                   firstname=firstname,
                                   lastyomi=lastyomi,
                                   firstyomi=firstyomi,
                                   tel1=tel1,
                                   tel2=tel2,
                                   tel3=tel3,
                                   company=company,
                                   department=department,
                                   zip1=zip1,
                                   zip2=zip2,
                                   prefecture=prefecture,
                                   prefec=prefec,
                                   pref=pref,
                                   city=city,
                                   town=town,
                                   building=building,
                                   beginDate=beginDate,
                                   endDate=endDate,
                                   mail_adr=mail_adr,
                                   retype=retype,
                                   user_id=user_id,
                                   id=id,
                                   error_no=error_no,
                                   )

    return render_template('confirm.html',
                           lastname=lastname,
                           firstname=firstname,
                           lastyomi=lastyomi,
                           firstyomi=firstyomi,
                           tel1=tel1,
                           tel2=tel2,
                           tel3=tel3,
                           company=company,
                           department=department,
                           zip1=zip1,
                           zip2=zip2,
                           prefecture=prefecture,
                           city=city,
                           town=town,
                           building=building,
                           mail_adr=mail_adr,
                           retype=retype,
                           autoPassword=ap,
                           beginDate=beginDate,
                           endDate=endDate,
                           user_id=user_id,
                           id=id,
                           )


@regist_module.route('/modification', methods=['POST'])
def modification():
    user_id = int(request.form['user_id'])
    id = int(request.form['id'])
    error_no = request.form['error_no']

    lastname = request.form.get('lastname')
    firstname = request.form.get('firstname')
    lastyomi = request.form.get('lastyomi')
    firstyomi = request.form.get('firstyomi')
    tel1 = request.form.get('tel1')
    tel2 = request.form.get('tel2')
    tel3 = request.form.get('tel3')
    company = request.form.get('company')
    department = request.form.get('department')
    zip1 = request.form.get('zip1')
    zip2 = request.form.get('zip2')
    prefecture = request.form.get('prefecture')
    city = request.form.get('city')
    town = request.form.get('town')
    building = request.form.get('building')
    beginDate = request.form.get('beginDate')
    endDate = request.form.get('endDate')
    mail_adr = request.form.get('mail_adr')
    retype = request.form.get('retype')

    if prefecture != "":
        try:
            pref = prefec.index(prefecture)
        except:
            pref = 0

    return render_template('modification.html',
                           lastname=lastname,
                           firstname=firstname,
                           lastyomi=lastyomi,
                           firstyomi=firstyomi,
                           tel1=tel1,
                           tel2=tel2,
                           tel3=tel3,
                           company=company,
                           department=department,
                           zip1=zip1,
                           zip2=zip2,
                           prefecture=prefecture,
                           prefec=prefec,
                           pref=pref,
                           city=city,
                           town=town,
                           building=building,
                           beginDate=beginDate,
                           endDate=endDate,
                           mail_adr=mail_adr,
                           retype=retype,
                           user_id=user_id,
                           id=id,
                           error_no=error_no,
                           )


@regist_module.route('/updateX', methods=['GET', 'POST'])
def updateX():
    user_id = request.form.get("user_id", "")
    id = request.form.get("id", "")
    if id == "":
        id = 0

    lastname = request.form.get("lastname", "")
    firstname = request.form.get("firstname", "")
    lastyomi = request.form.get("lastyomi", "")
    firstyomi = request.form.get("firstyomi", "")
    tel1 = request.form.get("tel1", "")
    tel2 = request.form.get("tel2", "")
    tel3 = request.form.get("tel3", "")
    zip1 = request.form.get("zip1", "")
    zip2 = request.form.get("zip2", "")
    company = request.form.get("company", "")
    department = request.form.get("department", "")
    pref = request.form.get("pref", "")
    prefecture = request.form.get("prefecture", "")
    city = request.form.get("city", "")
    town = request.form.get("town", "")
    building = request.form.get("building", "")
    mail_adr = request.form.get("mail_adr", "")

    autoPassword = request.form.get('autoPassword')
    status = 10    # 模擬試験が受験可能
    if autoPassword == 'on' or autoPassword == 'Checked':
        password = makePassword()
    else:
        password = ""

    beginDate = request.form.get('beginDate')
    if beginDate != '':
        begin,tmp = beginDate.split('T', 1)
    else:
        begin = '0'

    endDate = request.form.get('endDate')
    if endDate != '':
        fin,tmp = endDate.split('T', 1)
    else:
        fin = '0'

    try:
        if id == 0 or id == '0':
            addUser(lastname, firstname, lastyomi, firstyomi, tel1, tel2, tel3, zip1, zip2, \
                    company, department, prefecture, city, town, building, status, password, mail_adr, \
                    begin, fin)
        else:
            modifyUser(id, lastname, firstname, lastyomi, firstyomi, tel1, tel2, tel3, zip1, zip2, \
                       company, department, prefecture, city, town, building, status, password, mail_adr, \
                       begin, fin)
    except:
        return render_template('error2.html',
                               user_id=user_id,
                               error_message='失敗しました。',
                               )
    if autoPassword == 'on' or autoPassword == 'Checked':
        sendMail(lastname + '  ' + firstname, mail_adr, password)
    return render_template('success.html',
                           user_id=user_id,
                           message='成功しました。',
                           )
