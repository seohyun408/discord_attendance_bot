import pytz

KST = pytz.timezone("Asia/Seoul")

SPREADSHEET_ID = "1Q2wpa-htD2bB9LGpfubyPnrua_VX_WtmkWkvY-qv-LM"
SHEET_NAME = "스터디 출석부"
VOICE_CHANNEL_NAME = "모각공"

# discord display name → member info
MEMBERS = {
    "UXUI":    {"real_name": "오상훈", "morning_start": 7},
    "HR":      {"real_name": "심하연", "morning_start": 7},
    "Seohyun": {"real_name": "이서현", "morning_start": 7},
    "FE":      {"real_name": "이상희", "morning_start": 7},
    "서비스기획": {"real_name": "박나혜",  "morning_start": 7},
}

# 시트에서 멤버 이름이 쓰이는 방식 (header 행 검색용)
SHEET_NAME_MAP = {
    "UXUI":    "오상훈",
    "HR":      "심하연",
    "Seohyun": "이서현",
    "FE":      "이상희",
    "서비스기획": "박나혜",
}

# 오전 체크: 7:40 KST (7:00 기준 30분 지각자까지 포착)
MORNING_CHECK = (7, 40)
# 오후 체크: 15:30 KST
AFTERNOON_CHECK = (15, 30)
# 수요일 오후는 체크 안 함 (0=월, 2=수)
SKIP_AFTERNOON_WEEKDAYS = {2}
