import asyncio
import os
from datetime import datetime

import discord
from discord.ext import tasks

from config import (
    KST, MEMBERS, VOICE_CHANNEL_NAME,
    MORNING_CHECK, AFTERNOON_CHECK, SKIP_AFTERNOON_WEEKDAYS,
)
from sheets import update_attendance

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

client = discord.Client(intents=intents)

# {discord_display_name: first_join_datetime (KST)}
first_join_times: dict[str, datetime] = {}
_today = None  # date object, reset at midnight


def _kst_now() -> datetime:
    return datetime.now(KST)


def _reset_daily():
    global first_join_times, _today
    first_join_times = {}
    _today = _kst_now().date()
    print(f"[bot] Daily reset — tracking for {_today}")


@client.event
async def on_ready():
    print(f"[bot] Logged in as {client.user}")
    _reset_daily()
    scheduler.start()


@client.event
async def on_voice_state_update(member: discord.Member, before, after):
    global _today
    now = _kst_now()

    # New day → reset
    if now.date() != _today:
        _reset_daily()

    display = member.display_name
    if display not in MEMBERS:
        return

    # Joined 모각공 channel
    if after.channel and VOICE_CHANNEL_NAME in after.channel.name:
        if display not in first_join_times:
            first_join_times[display] = now
            print(f"[bot] {display} joined '{after.channel.name}' at {now.strftime('%H:%M:%S')}")


@tasks.loop(minutes=1)
async def scheduler():
    now = _kst_now()

    # Midnight reset
    if now.hour == 0 and now.minute == 0:
        _reset_daily()
        return

    h, m = now.hour, now.minute

    if (h, m) == MORNING_CHECK:
        print("[bot] Running morning attendance check…")
        await asyncio.get_event_loop().run_in_executor(
            None, update_attendance, "morning", dict(first_join_times)
        )

    elif (h, m) == AFTERNOON_CHECK:
        if now.weekday() in SKIP_AFTERNOON_WEEKDAYS:
            print(f"[bot] Skipping afternoon check (weekday={now.weekday()})")
        else:
            print("[bot] Running afternoon attendance check…")
            await asyncio.get_event_loop().run_in_executor(
                None, update_attendance, "afternoon", dict(first_join_times)
            )


if __name__ == "__main__":
    token = os.environ["DISCORD_TOKEN"]
    client.run(token)
