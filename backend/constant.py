import os, json

# データベースのパスを特定
base_path = os.path.dirname(__file__)
form_path = base_path + '/templates'
FILES_DIR = base_path + '/static'
json_path = base_path + '/static/config.json'


def _load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(os.path.join(base_path, ".env"), override=True)
    except ImportError:
        pass


_load_env()


def resolve_db_path() -> str:
    """Return the sqlite path for the active subject.

    Priority:
    1. EXAM_DB_PATH environment variable (absolute or relative)
    2. exam-{APP_PROFILE}.sqlite (e.g. exam-SPANISH4.sqlite)
    3. exam.sqlite when APP_PROFILE=CDS (legacy production file)
    4. otherwise exam-{APP_PROFILE}.sqlite (even if not created yet)
    """
    override = os.environ.get("EXAM_DB_PATH", "").strip()
    if override:
        return override if os.path.isabs(override) else os.path.join(base_path, override)

    profile = os.environ.get("APP_PROFILE", "CDS").upper()
    profile_db = os.path.join(base_path, f"exam-{profile}.sqlite")
    legacy_db = os.path.join(base_path, "exam.sqlite")

    if os.path.isfile(profile_db):
        return profile_db
    if profile == "CDS" and os.path.isfile(legacy_db):
        return legacy_db
    return profile_db


db_path = resolve_db_path()

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
_CATEGORY_CODE_ALPHABET = (
    "0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW"
    + "XYZ[]^`abcdefghijklmnopqrstuvwxyz"
)


def _build_category_code(num_categories: int) -> str:
    return _CATEGORY_CODE_ALPHABET[: max(num_categories, 1)]


categoryCode = _build_category_code(10)

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

def _profile_value(profile: dict, default: dict, key: str, fallback=None):
    if key in profile:
        return profile[key]
    if key in default:
        return default[key]
    return fallback


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
        StatusSetupMessage, abbreviation, areaname, practice, practice2, categoryNumber, categoryCode

    from config_loader import build_area_globals, get_default_section, get_profile_section

    default = get_default_section()
    profile = get_profile_section()

    SUBJECT = profile["SUBJECT"]
    APP_TITLE = profile["APP_TITLE"]
    PassScore1 = _profile_value(profile, default, "PassScore1")
    PassScore2 = _profile_value(profile, default, "PassScore2")
    TimePerQuestion = _profile_value(profile, default, "TimePerQuestion")
    LOGIN_URL = profile["LOGIN_URL"]
    PORT_NO = profile["PORT_NO"]
    MaxQuestions = _profile_value(profile, default, "MaxQuestions")
    THRESHOLD_HIGH = _profile_value(profile, default, "THRESHOLD_HIGH")
    THRESHOLD_LOW = _profile_value(profile, default, "THRESHOLD_LOW")
    NumOfHeader = _profile_value(profile, default, "NumOfHeader")
    NumOfArea = profile["NumOfArea"]
    NumOfCategory = profile["NumOfCategory"]
    NumOfCategory1 = profile["NumOfCategory1"]
    NumOfCategory2 = profile["NumOfCategory2"]
    NumOfCategory3 = profile["NumOfCategory3"]
    NumOfCategory4 = profile["NumOfCategory4"]
    NumOfCategory5 = profile["NumOfCategory5"]
    NumOfCategory6 = profile["NumOfCategory6"]
    NumOfCategory7 = profile["NumOfCategory7"]
    NumOfCategory8 = profile["NumOfCategory8"]
    examType1 = profile["examType1"]
    examType2 = profile["examType2"]
    examType3 = profile["examType3"]
    examType4 = profile["examType4"]
    examType5 = profile["examType5"]
    examType6 = profile["examType6"]
    examType7 = profile["examType7"]
    examType8 = profile["examType8"]
    examType10 = _profile_value(profile, default, "examType10")
    examType11 = _profile_value(profile, default, "examType11")
    examType12 = _profile_value(profile, default, "examType12")
    examType99 = _profile_value(profile, default, "examType99")
    examTitle1 = profile["examTitle1"]
    examTitle2 = profile["examTitle2"]
    examTitle3 = profile["examTitle3"]
    examTitle4 = profile["examTitle4"]
    examTitle5 = profile["examTitle5"]
    examTitle6 = profile["examTitle6"]
    examTitle7 = profile["examTitle7"]
    examTitle8 = profile["examTitle8"]
    examTitle10 = _profile_value(profile, default, "examTitle10")
    examTitle11 = _profile_value(profile, default, "examTitle11")
    examTitle12 = _profile_value(profile, default, "examTitle12")
    NumOfQuestions1 = _profile_value(profile, default, "NumOfQuestions1")
    NumOfQuestions2 = _profile_value(profile, default, "NumOfQuestions2")
    examEntry = _profile_value(profile, default, "examEntry")
    examEntry1 = _profile_value(profile, default, "examEntry1")
    examEntry2 = _profile_value(profile, default, "examEntry2")
    examEntry3 = _profile_value(profile, default, "examEntry3")
    examEntry4 = _profile_value(profile, default, "examEntry4")
    examEntry5 = _profile_value(profile, default, "examEntry5")
    examEntry6 = profile["examEntry6"]
    examEntry7 = profile["examEntry7"]
    examEntry8 = profile["examEntry8"]
    examEntry9 = _profile_value(profile, default, "examEntry9")
    examEntry10 = profile["examEntry10"]
    examEntry11 = profile["examEntry11"]
    examEntry12 = profile["examEntry12"]
    examEntry1s = _profile_value(profile, default, "examEntry1s")
    examEntry2s = _profile_value(profile, default, "examEntry2s")
    examEntry3s = _profile_value(profile, default, "examEntry3s")
    examEntry4s = _profile_value(profile, default, "examEntry4s")
    examEntry5s = _profile_value(profile, default, "examEntry5s")
    examEntry6s = _profile_value(profile, default, "examEntry6s")
    examEntry7s = _profile_value(profile, default, "examEntry7s")
    examEntry8s = _profile_value(profile, default, "examEntry8s")
    NEW_ACCOUNT_MESSAGE1_1 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE1_1")
    NEW_ACCOUNT_MESSAGE1_2 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE1_2")
    NEW_ACCOUNT_MESSAGE1_3 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE1_3")
    NEW_ACCOUNT_MESSAGE2_1 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE2_1")
    NEW_ACCOUNT_MESSAGE2_2 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE2_2")
    NEW_ACCOUNT_MESSAGE2_3 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE2_3")
    NEW_ACCOUNT_MESSAGE2_4 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE2_4")
    NEW_ACCOUNT_MESSAGE2_5 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE2_5")
    NEW_ACCOUNT_MESSAGE2_6 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE2_6")
    NEW_ACCOUNT_MESSAGE2_7 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE2_7")
    NEW_ACCOUNT_MESSAGE2_8 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE2_8")
    NEW_ACCOUNT_MESSAGE2_9 = _profile_value(profile, default, "NEW_ACCOUNT_MESSAGE2_9")
    PASS2_MESSAGE_1 = _profile_value(profile, default, "PASS2_MESSAGE_1")
    PASS2_MESSAGE_2 = _profile_value(profile, default, "PASS2_MESSAGE_2")
    PASS2_MESSAGE_3 = _profile_value(profile, default, "PASS2_MESSAGE_3")
    PASS2_MESSAGE_4 = _profile_value(profile, default, "PASS2_MESSAGE_4")
    PASS2_MESSAGE_5 = _profile_value(profile, default, "PASS2_MESSAGE_5")
    PASS3_MESSAGE_1 = _profile_value(profile, default, "PASS3_MESSAGE_1")
    PASS3_MESSAGE_2 = _profile_value(profile, default, "PASS3_MESSAGE_2")
    PASS3_MESSAGE_3 = _profile_value(profile, default, "PASS3_MESSAGE_3")
    PASS3_MESSAGE_4 = _profile_value(profile, default, "PASS3_MESSAGE_4")
    PASS3_MESSAGE_5 = _profile_value(profile, default, "PASS3_MESSAGE_5")
    Comment_Base = profile["Comment_Base"]
    Area_Base = profile["Area_Base"]
    Category_Base = profile["Category_Base"]
    FIRST_MAIL = profile["FIRST_MAIL"]
    LAST_MAIL = profile["LAST_MAIL"]
    GradeMessage1 = _profile_value(profile, default, "GradeMessage1")
    GradeMessage2 = _profile_value(profile, default, "GradeMessage2")
    GradeMessage3 = _profile_value(profile, default, "GradeMessage3")
    GradeMessage3a = _profile_value(profile, default, "GradeMessage3a")
    GradeMessage4 = _profile_value(profile, default, "GradeMessage4")
    StatusSetupMessage = _profile_value(profile, default, "StatusSetupMessage")

    from config_loader import get_areas

    areas = get_areas()
    if areas:
        (
            abbreviation,
            areaname,
            practice,
            practice2,
            categoryNumber,
        ) = build_area_globals(areas)
        categoryCode = _build_category_code(len(categoryNumber))


readConstant()