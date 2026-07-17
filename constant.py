import os, json

# データベースのパスを特定
base_path = os.path.dirname(__file__)
db_path = base_path + '/exam.sqlite'
form_path = base_path + '/templates'
FILES_DIR = base_path + '/static'
json_path = base_path + '/static/config.json'

# 実行環境制御スイッチ
# 0: Linux, 1: Windows
PLATFORM = 1
# 0: non-SSL 1: SSL
SSL=1
# 時差
DIFF_JST_FROM_UTC = 9
cset = 'utf-8'
# デバック・スイッチ
# 0: 本番, 1: デバック
MAIL_DEBUG = 1

# メールサーバ
servername = "v1065.ssl-site.com"
# 送信元
from_email = "ITIL4 Exercise System"

# 受信先 (CC) & 受信先 (BCC)
if MAIL_DEBUG == 1:
    cc_email = "at.kanno17@gmail.com"
    bcc_email = "atsushi.kanno@nifty.com"
else:
    cc_email = "ark@gigamall.ne.jp"
    bcc_email = "miyauchi.ark@gmail.com,kanno@olivenet.co.jp"

abbreviation = ['組織', '技術', 'SVS', '活動調整・調達']

# 領域とカテゴリの関係
areaname = [
    ["組織と人材", 3, "", "", ""],
    ["情報と技術", 1, "", "", ""],
    ["サービスバリュー・ストリーム", 4, "", "", ""],
    ["活動の調整とリソースの調達", 2, "", "", ""],
]

practice = [
    ["組織の文化", "シフトレフト", "要員の計画と管理"],
    ["新たな技術"],
    ["新サービス導入のバリューストリーム", "新サービス導入に貢献するプラクティス", "ユーザサポートのバリューストリーム", "ユーザサポートに貢献するプラクティス"],
    ["活動の調整方法", "調達の手段"]
]

practice2 = [
    "組織の文化", "シフトレフト", "要員の計画と管理",
    "新たな技術",
    "新サービス導入のバリューストリーム", "新サービス導入に貢献するプラクティス", "ユーザサポートのバリューストリーム", "ユーザサポートに貢献するプラクティス",
    "活動の調整方法", "調達の手段"
]

categoryNumber = [11, 12, 13,
                  21,
                  31, 32, 33, 34,
                  41, 42]

# 問題作成のための情報（多めに設定している）
categoryCode = "0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW" \
               + "XYZ[]^`abcdefghijklmnopqrstuvwxyz"

PASS1_MESSAGE = "おめでとうございます。修了試験の前半合格です。<br>頑張ってこられた成果が出ました。<br>" \
    + "あと１回修了試験の後半があります。<br>それに合格すると、いよいよ本試験（認定試験）です。<br>" \
    +  "あと少しです。がんばってください。"

FAIL_MESSAGE = "残念ながら、今回合格ラインに達していませんでした。<br>" \
              + "模擬試験に立ち返り、弱い領域を確認して補強するようにしてください。<br>" \
              + "あとひと頑張りです。"

END_MESSAGE = '\n\n株式会社アーク\nTEL：03-5577-5311\n代表email: ark@gigamall.ne.jp\n' + \
    '\n本メールにご返信いただいても対応できません。\n上記メールアドレスにご連絡ください。'

PASS_MESSAGE_IN_MAIL = "合格です。"
PASS_MESSAGE_ON_SCREEN = "合格です。おめでとうございます。"
FAIL_MESSAGE_ON_SCREEN = "不合格でした。"

return1 = '<form action="makeExam" method="POST">' + \
          '<input type="hidden" name="user_id" value="'
return2 = '" /><button type="submit" class="btn btn-primary btn-block" name="category" value="99">' + \
          '管理画面へ戻る</button><br></p></form>'

return3 = '<div class="buttonwrap" style="display:inline-flex"><form action="summary" >' + \
          '<input type="hidden" name="user_id" value="'
return4 = '" /><button type="submit" style="margin:10px" name="category" value="99">' + \
          'メインメニューへ戻る</button><br></p></form>'

DefaultStatus=30

prefec = ["都道府県",
          "北海道",
          "青森県",
          "岩手県",
          "秋田県",
          "山形県",
          "宮城県",
          "福島県",
          "茨城県",
          "栃木県",
          "群馬県",
          "埼玉県",
          "千葉県",
          "東京都",
          "神奈川県",
          "新潟県",
          "富山県",
          "石川県",
          "福井県",
          "山梨県",
          "長野県",
          "岐阜県",
          "静岡県",
          "愛知県",
          "三重県",
          "滋賀県",
          "京都府",
          "大阪府",
          "兵庫県",
          "奈良県",
          "和歌山県",
          "鳥取県",
          "島根県",
          "岡山県",
          "広島県",
          "山口県",
          "徳島県",
          "香川県",
          "愛媛県",
          "高知県",
          "福岡県",
          "佐賀県",
          "長崎県",
          "熊本県",
          "大分県",
          "宮崎県",
          "鹿児島県",
          "沖縄県", ]

SUBJECT = None
APP_TITLE = None
PassScore1 = None
PassScore2 = None
TimePerQuestion = None
LOGIN_URL = None
PORT_NO = None
NEW_ACCOUNT_MESSAGE1_1 = None
NEW_ACCOUNT_MESSAGE1_2 = None
NEW_ACCOUNT_MESSAGE1_3 = None
NEW_ACCOUNT_MESSAGE2_1 = None
NEW_ACCOUNT_MESSAGE2_2 = None
NEW_ACCOUNT_MESSAGE2_3 = None
NEW_ACCOUNT_MESSAGE2_4 = None
NEW_ACCOUNT_MESSAGE2_5 = None
NEW_ACCOUNT_MESSAGE2_6 = None
NEW_ACCOUNT_MESSAGE2_7 = None
NEW_ACCOUNT_MESSAGE2_8 = None
NEW_ACCOUNT_MESSAGE2_9= None
PASS2_MESSAGE_1 = None
PASS2_MESSAGE_2 = None
PASS2_MESSAGE_3 = None
PASS2_MESSAGE_4 = None
PASS2_MESSAGE_5 = None
PASS3_MESSAGE_1 = None
PASS3_MESSAGE_2 = None
PASS3_MESSAGE_3 = None
PASS3_MESSAGE_4 = None
PASS3_MESSAGE_5 = None
MaxQuestions = None
THRESHOLD_HIGH = None
THRESHOLD_LOW = None
NumOfHeader = None
NumOfArea = None
NumOfCategory = None
NumOfCategory1 = None
NumOfCategory2 = None
NumOfCategory3 = None
NumOfCategory4 = None
NumOfCategory5 = None
NumOfCategory6 = None
NumOfCategory7 = None
NumOfCategory8 = None
examType1 = None
examType2 = None
examType3 = None
examType4 = None
examType5 = None
examType6 = None
examType7 = None
examType8 = None
examType10 = None
examType11 = None
examType12 = None
examType99 = None
examTitle1 = None
examTitle2 = None
examTitle3 = None
examTitle4 = None
examTitle5 = None
examTitle6 = None
examTitle7 = None
examTitle8 = None
examTitle10 = None
examTitle11 = None
examTitle12 = None
NumOfQuestions1 = None
NumOfQuestions2 = None
examEntry = None
examEntry1 = None
examEntry1s = None
examEntry2 = None
examEntry2s = None
examEntry3 = None
examEntry3s = None
examEntry4 = None
examEntry4s = None
examEntry5 = None
examEntry5s = None
examEntry6 = None
examEntry6s = None
examEntry7 = None
examEntry7s = None
examEntry8 = None
examEntry8s = None
examEntry10 = None
examEntry11 = None
examEntry12 = None
Comment_Base = None
Area_Base = None
Category_Base = None
FIRST_MAIL = None
LAST_MAIL = None
GradeMessage1 = None
GradeMessage2 = None
GradeMessage3 = None
GradeMessage3a = None
GradeMessage4 = None
StatusSetupMessage = None

def readConstant():
    global SUBJECT, APP_TITLE, PassScore1, PassScore2, TimePerQuestion, LOGIN_URL, \
        NEW_ACCOUNT_MESSAGE1_1,  NEW_ACCOUNT_MESSAGE1_2, NEW_ACCOUNT_MESSAGE1_3, \
        NEW_ACCOUNT_MESSAGE2_1, NEW_ACCOUNT_MESSAGE2_2, NEW_ACCOUNT_MESSAGE2_3, \
        NEW_ACCOUNT_MESSAGE2_4, NEW_ACCOUNT_MESSAGE2_5, NEW_ACCOUNT_MESSAGE2_6, \
        NEW_ACCOUNT_MESSAGE2_7, NEW_ACCOUNT_MESSAGE2_8, NEW_ACCOUNT_MESSAGE2_9, PORT_NO, \
        PASS2_MESSAGE_1, PASS2_MESSAGE_2, PASS2_MESSAGE_3, PASS2_MESSAGE_4, \
        PASS2_MESSAGE_5, PASS3_MESSAGE_1, PASS3_MESSAGE_2, PASS3_MESSAGE_3, \
        PASS3_MESSAGE_4, PASS3_MESSAGE_5, THRESHOLD_HIGH, THRESHOLD_LOW, \
        MaxQuestions, NumOfHeader, \
        NumOfArea, NumOfCategory, NumOfCategory1, NumOfCategory2, NumOfCategory3, \
        NumOfCategory4, NumOfCategory5, NumOfCategory6, NumOfCategory7, NumOfCategory8, \
        examType1, examType2, examType3, examType4, examType5, examType6, \
        examType7, examType8, examType10, examType11, examType12, examType99, \
        examTitle1, examTitle2, examTitle3, examTitle4, examTitle5, \
        examTitle6, examTitle7, examTitle8, examTitle10, examTitle11, examTitle12, \
        examEntry, examEntry1, examEntry2, examEntry3, examEntry4, examEntry5, \
        examEntry6, examEntry7, examEntry8, examEntry9, examEntry10, examEntry11, \
        examEntry12, examEntry1s, examEntry2s, examEntry3s, examEntry4s, examEntry5s, \
        examEntry6s, examEntry7s, examEntry8s, NumOfQuestions1, NumOfQuestions2, \
        Comment_Base, Area_Base, Category_Base, FIRST_MAIL, LAST_MAIL, \
        GradeMessage1, GradeMessage2, GradeMessage3, GradeMessage3a, GradeMessage4, \
        StatusSetupMessage

        # アプリケーションごとに変わる定数を読み込む (2026/2/4)
    with open(json_path, encoding="utf-8") as f:
        config = json.load(f)

    SUBJECT = config["CDS"]["SUBJECT"]
    APP_TITLE = config["CDS"]["APP_TITLE"]
    PassScore1 = config["DEFAULT"]["PassScore1"]
    PassScore2 = config["DEFAULT"]["PassScore2"]
    TimePerQuestion = config["DEFAULT"]["TimePerQuestion"]
    LOGIN_URL = config["CDS"]["LOGIN_URL"]
    PORT_NO = config["CDS"]["PORT_NO"]
    MaxQuestions = config["DEFAULT"]["MaxQuestions"]
    THRESHOLD_HIGH = config["DEFAULT"]["THRESHOLD_HIGH"]
    THRESHOLD_LOW = config["DEFAULT"]["THRESHOLD_LOW"]
    NumOfHeader = config["DEFAULT"]["NumOfHeader"]
    NumOfArea = config["CDS"]["NumOfArea"]
    NumOfCategory = config["CDS"]["NumOfCategory"]
    NumOfCategory1 = config["CDS"]["NumOfCategory1"]
    NumOfCategory2 = config["CDS"]["NumOfCategory2"]
    NumOfCategory3 = config["CDS"]["NumOfCategory3"]
    NumOfCategory4 = config["CDS"]["NumOfCategory4"]
    NumOfCategory5 = config["CDS"]["NumOfCategory5"]
    NumOfCategory6 = config["CDS"]["NumOfCategory6"]
    NumOfCategory7 = config["CDS"]["NumOfCategory7"]
    NumOfCategory8 = config["CDS"]["NumOfCategory8"]
    examType1 = config["CDS"]["examType1"]
    examType2 = config["CDS"]["examType2"]
    examType3 = config["CDS"]["examType3"]
    examType4 = config["CDS"]["examType4"]
    examType5 = config["CDS"]["examType5"]
    examType6 = config["CDS"]["examType6"]
    examType7 = config["CDS"]["examType7"]
    examType8 = config["CDS"]["examType8"]
    examType10 = config["DEFAULT"]["examType10"]
    examType11 = config["DEFAULT"]["examType11"]
    examType12 = config["DEFAULT"]["examType12"]
    examType99 = config["DEFAULT"]["examType99"]
    examTitle1 = config["CDS"]["examTitle1"]
    examTitle2 = config["CDS"]["examTitle2"]
    examTitle3 = config["CDS"]["examTitle3"]
    examTitle4 = config["CDS"]["examTitle4"]
    examTitle5 = config["CDS"]["examTitle5"]
    examTitle6 = config["CDS"]["examTitle6"]
    examTitle7 = config["CDS"]["examTitle7"]
    examTitle8 = config["CDS"]["examTitle8"]
    examTitle10 = config["DEFAULT"]["examTitle10"]
    examTitle11 = config["DEFAULT"]["examTitle11"]
    examTitle12 = config["DEFAULT"]["examTitle12"]
    NumOfQuestions1 = config["DEFAULT"]["NumOfQuestions1"]
    NumOfQuestions2 = config["DEFAULT"]["NumOfQuestions2"]
    examEntry =config["DEFAULT"]["examEntry"]
    examEntry1 = config["DEFAULT"]["examEntry1"]
    examEntry2 = config["DEFAULT"]["examEntry2"]
    examEntry3 = config["DEFAULT"]["examEntry3"]
    examEntry4 = config["DEFAULT"]["examEntry4"]
    examEntry5 = config["DEFAULT"]["examEntry5"]
    examEntry6 = config["CDS"]["examEntry6"]
    examEntry7 = config["CDS"]["examEntry7"]
    examEntry8 = config["CDS"]["examEntry8"]
    examEntry10 = config["CDS"]["examEntry10"]
    examEntry11 = config["CDS"]["examEntry11"]
    examEntry12 = config["CDS"]["examEntry12"]
    examEntry1s = config["DEFAULT"]["examEntry1s"]
    examEntry2s = config["DEFAULT"]["examEntry2s"]
    examEntry3s = config["DEFAULT"]["examEntry3s"]
    examEntry4s = config["DEFAULT"]["examEntry4s"]
    examEntry5s = config["DEFAULT"]["examEntry5s"]
    examEntry6s = config["DEFAULT"]["examEntry6s"]
    examEntry7s = config["DEFAULT"]["examEntry7s"]
    examEntry8s = config["DEFAULT"]["examEntry8s"]
    NEW_ACCOUNT_MESSAGE1_1 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE1_1"]
    NEW_ACCOUNT_MESSAGE1_2 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE1_2"]
    NEW_ACCOUNT_MESSAGE1_3 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE1_3"]
    NEW_ACCOUNT_MESSAGE2_1 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE2_1"]
    NEW_ACCOUNT_MESSAGE2_2 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE2_2"]
    NEW_ACCOUNT_MESSAGE2_3 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE2_3"]
    NEW_ACCOUNT_MESSAGE2_4 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE2_4"]
    NEW_ACCOUNT_MESSAGE2_5 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE2_5"]
    NEW_ACCOUNT_MESSAGE2_6 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE2_6"]
    NEW_ACCOUNT_MESSAGE2_7 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE2_7"]
    NEW_ACCOUNT_MESSAGE2_8 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE2_8"]
    NEW_ACCOUNT_MESSAGE2_9 = config["DEFAULT"]["NEW_ACCOUNT_MESSAGE2_9"]
    PASS2_MESSAGE_1 = config["DEFAULT"]["PASS2_MESSAGE_1"]
    PASS2_MESSAGE_2 = config["DEFAULT"]["PASS2_MESSAGE_2"]
    PASS2_MESSAGE_3 = config["DEFAULT"]["PASS2_MESSAGE_3"]
    PASS2_MESSAGE_4 = config["DEFAULT"]["PASS2_MESSAGE_4"]
    PASS2_MESSAGE_5 = config["DEFAULT"]["PASS2_MESSAGE_5"]
    PASS3_MESSAGE_1 = config["DEFAULT"]["PASS3_MESSAGE_1"]
    PASS3_MESSAGE_2 = config["DEFAULT"]["PASS3_MESSAGE_2"]
    PASS3_MESSAGE_3 = config["DEFAULT"]["PASS3_MESSAGE_3"]
    PASS3_MESSAGE_4 = config["DEFAULT"]["PASS3_MESSAGE_4"]
    PASS3_MESSAGE_5 = config["DEFAULT"]["PASS3_MESSAGE_5"]
    Comment_Base = config["CDS"]["Comment_Base"]
    Area_Base = config["CDS"]["Area_Base"]
    Category_Base = config["CDS"]["Category_Base"]
    FIRST_MAIL = config["CDS"]["FIRST_MAIL"]
    LAST_MAIL = config["CDS"]["LAST_MAIL"]
    GradeMessage1 = config["DEFAULT"]["GradeMessage1"]
    GradeMessage2 = config["DEFAULT"]["GradeMessage2"]
    GradeMessage3 = config["DEFAULT"]["GradeMessage3"]
    GradeMessage3a = config["DEFAULT"]["GradeMessage3a"]
    GradeMessage4 = config["DEFAULT"]["GradeMessage4"]
    StatusSetupMessage = config["DEFAULT"]["StatusSetupMessage"]