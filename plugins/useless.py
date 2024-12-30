from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import OWNER_ID, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import *
from pytz import timezone

@Bot.on_message(filters.command('stats') & filters.user(OWNER_ID))
async def stats(bot: Bot, message: Message):
    # Make 'now' timezone-aware (IST)
    ist = timezone("Asia/Kolkata")
    now = datetime.now(ist)

    # Calculate delta
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)

    await message.reply(BOT_STATS_TEXT.format(uptime=time))


@Bot.on_message(filters.private & is_admin & filters.incoming)
async def useless(_,message: Message):
    if USER_REPLY_TEXT:
        await message.reply(USER_REPLY_TEXT)