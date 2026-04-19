import json
import os
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from config import KST, SPREADSHEET_ID, SHEET_NAME, SHEET_NAME_MAP

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

_worksheet_cache = None


def get_worksheet():
    global _worksheet_cache
    creds_json = os.environ["GOOGLE_CREDENTIALS_JSON"]
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SPREADSHEET_ID)
    return sh.worksheet(SHEET_NAME)


def _day_name(weekday: int) -> str:
    return ["월", "화", "수", "목", "금", "토", "일"][weekday]


def format_date_key(dt: datetime, session: str) -> str:
    """Return sheet date string like '4.20 월 AM'"""
    suffix = "AM" if session == "morning" else "PM"
    return f"{dt.month}.{dt.day} {_day_name(dt.weekday())} {suffix}"


def _find_col_indices(all_values: list[list]) -> dict[str, int]:
    """Find 0-based column index for each member by scanning header rows."""
    col_map = {}
    for row in all_values:
        for sheet_name in SHEET_NAME_MAP.values():
            if sheet_name in row:
                for discord_key, sname in SHEET_NAME_MAP.items():
                    try:
                        col_map[discord_key] = row.index(sname)
                    except ValueError:
                        pass
                if len(col_map) == len(SHEET_NAME_MAP):
                    return col_map
    return col_map


def _find_date_row(all_values: list[list], date_key: str) -> int | None:
    """Return 0-based row index matching date_key in column B (index 1)."""
    for i, row in enumerate(all_values):
        if len(row) > 1 and row[1].strip() == date_key:
            return i
    return None


def _cell_is_updatable(value: str) -> bool:
    """Cell can be written only if empty, FALSE, or boolean-false."""
    return value.strip().upper() in ("", "FALSE")


def update_attendance(session: str, join_times: dict[str, datetime]):
    """
    session: 'morning' or 'afternoon'
    join_times: {discord_display_name: first_join_datetime}
    """
    now = datetime.now(KST)
    date_key = format_date_key(now, session)

    ws = get_worksheet()
    all_values = ws.get_all_values()

    row_idx = _find_date_row(all_values, date_key)
    if row_idx is None:
        print(f"[sheets] Row not found for '{date_key}'")
        return

    col_map = _find_col_indices(all_values)
    if not col_map:
        print("[sheets] Could not determine column indices from sheet header")
        return

    updates = []
    row_data = all_values[row_idx]

    for discord_name, col_idx in col_map.items():
        current = row_data[col_idx] if col_idx < len(row_data) else ""
        if not _cell_is_updatable(current):
            print(f"[sheets] Skip {SHEET_NAME_MAP[discord_name]}: already '{current}'")
            continue

        join_dt = join_times.get(discord_name)
        status = _calc_status(join_dt, discord_name, session, now)

        # gspread uses 1-based row/col
        updates.append({
            "range": gspread.utils.rowcol_to_a1(row_idx + 1, col_idx + 1),
            "values": [[True if status is True else status]],
        })
        print(f"[sheets] {SHEET_NAME_MAP[discord_name]}: {status}")

    if updates:
        ws.batch_update(updates)


def _calc_status(join_dt: datetime | None, discord_name: str, session: str, now: datetime):
    from config import MEMBERS
    if join_dt is None or join_dt.date() != now.date():
        return "불참"

    if session == "morning":
        start_hour = MEMBERS[discord_name]["morning_start"]
    else:
        start_hour = 14

    today = now.date()
    start = KST.localize(datetime(today.year, today.month, today.day, start_hour, 0))
    diff = (join_dt - start).total_seconds() / 60

    if diff <= 10:
        return True
    elif diff <= 20:
        return "20분 지각"
    elif diff <= 30:
        return "30분 지각"
    else:
        return "불참"
