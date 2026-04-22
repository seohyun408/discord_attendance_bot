import pytz

KST = pytz.timezone("Asia/Seoul")

SPREADSHEET_ID = "1Q2wpa-htD2bB9LGpfubyPnrua_VX_WtmkWkvY-qv-LM"
SHEET_NAME = "스터디 출석부"
VOICE_CHANNEL_NAME = "모각공"

# discord display name → member info
MEMBERS = {
    "오상훈(UXUI)":    {"real_name": "오상훈", "morning_start": 7},
    "심하연(HR)":      {"real_name": "심하연", "morning_start": 7},
    "Seohyun":        {"real_name": "이서현", "morning_start": 7},
    "이상희(FE)":      {"real_name": "이상희", "morning_start": 7},
    "박나혜(서비스기획)": {"real_name": "박나혜",  "morning_start": 7},
}

# 시트에서 멤버 이름이 쓰이는 방식
SHEET_NAME_MAP = {
    "오상훈(UXUI)":    "오상훈",
    "심하연(HR)":      "심하연",
    "Seohyun":        "이서현",
    "이상희(FE)":      "이상희",
    "박나혜(서비스기획)": "박나혜",
}

# 날짜가 있는 열 (L열, 0-based index 11)
DATE_COL_INDEX = 11

# discord display name → 시트 열 (0-based index)
# M=12(오상훈), N=13(심하연), O=14(이서현), Q=16(이상희), R=17(박나혜)
# key는 반드시 MEMBERS / SHEET_NAME_MAP 의 key(= discord display_name)와 동일해야 함
MEMBER_COL_MAP = {
    "오상훈(UXUI)":    12,
    "심하연(HR)":      13,
    "Seohyun":         14,
    "이상희(FE)":      16,
    "박나혜(서비스기획)": 17,
}

# 오전 체크: 7:40 KST (7:00 기준 30분 지각자까지 포착)
MORNING_CHECK = (7, 40)
# 오후 체크: 15:30 KST
AFTERNOON_CHECK = (15, 30)
# 수요일 오후는 체크 안 함 (0=월, 2=수)
SKIP_AFTERNOON_WEEKDAYS = {2}
