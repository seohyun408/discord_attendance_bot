import pytz

KST = pytz.timezone("Asia/Seoul")

SPREADSHEET_ID = "1Q2wpa-htD2bB9LGpfubyPnrua_VX_WtmkWkvY-qv-LM"
SHEET_NAME = "🔥스터디 출석부(7~8월)🔥"
VOICE_CHANNEL_NAME = "모각공"

# discord display name → member info
MEMBERS = {
    "오상훈(UXUI)":    {"real_name": "오상훈", "morning_start": 7},
    "심하연(HR)":      {"real_name": "심하연", "morning_start": 7},
    "Seohyun":        {"real_name": "이서현", "morning_start": 7},
    "박나혜(서비스기획)": {"real_name": "박나혜",  "morning_start": 7},
    "정수미":          {"real_name": "정수미", "morning_start": 7},
    "다빈":            {"real_name": "이다빈", "morning_start": 7},
}

# 시트에서 멤버 이름이 쓰이는 방식
SHEET_NAME_MAP = {
    "오상훈(UXUI)":    "오상훈",
    "심하연(HR)":      "심하연",
    "Seohyun":        "이서현",
    "박나혜(서비스기획)": "박나혜",
    "정수미":          "정수미",
    "다빈":            "이다빈",
}

# 날짜가 있는 열 (L열, 0-based index 11)
DATE_COL_INDEX = 11

# discord display name → 시트 열 (0-based index)
# M=12(오상훈), N=13(심하연), O=14(이서현), P=15(박나혜), Q=16(정수미), R=17(다빈)
# key는 반드시 MEMBERS / SHEET_NAME_MAP 의 key(= discord display_name)와 동일해야 함
MEMBER_COL_MAP = {
    "오상훈(UXUI)":    12,
    "심하연(HR)":      13,
    "Seohyun":         14,
    "박나혜(서비스기획)": 15,
    "정수미":          16,
    "다빈":            17,
}

# 오전 체크: 7:40 KST (멤버별 morning_start 기준으로 지각 계산)
MORNING_CHECK = (7, 40)
# 오후 체크: 15:30 KST
AFTERNOON_CHECK = (14, 40)
# 수요일 오후는 체크 안 함 (0=월, 2=수)
# SKIP_AFTERNOON_WEEKDAYS = {2}
