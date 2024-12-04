from pyrogram import __version__
from bot import Bot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from config import PRICE1, PRICE2, PRICE3, PRICE4, PRICE5, UPI_ID, UPI_IMAGE_URL, SCREENSHOT_URL

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b> ⟦⟧ Hi There Vro!💫\n┏━━━━━━━❪❂❫━━━━━━━━\n◈ ᴄʀᴇᴀᴛᴏʀ: <a href=https://t.me/LUFFY1JOYBOY>Ŧrαfͥαlͣgͫαrαw</a>\n◈ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://t.me/Anime_Madness>ᴀɴɪᴍᴇ ᴍᴀᴅɴᴇss</a>\n◈ ᴏɴɢᴏɪɴɢ ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/Ongoing_Madness>ᴏɴɢᴏɪɴɢ ᴍᴀᴅɴᴇss</a>\n◈ ᴀᴅᴜʟᴛ ᴄʜᴀɴɴᴇʟ: <a href=https://t.me/Cultured_Madness>ᴄᴜʟᴛᴜʀᴇᴅ ᴍᴀᴅɴᴇss</a>\n◈ ᴍᴏᴠɪᴇ : <a href=https://dashboard.heroku.com>ᴍᴀᴅɴᴇss ᴍᴏᴠɪᴇ</a>\n◈ ᴡᴇʙ sᴇʀɪᴇs: <a href=https://t.me/Series_Madness>sᴇʀɪᴇs ᴍᴀᴅɴᴇss</a>\n┗━━━━━━━❪❂❫━━━━━━━━</b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
    elif data == "buy_prem":
        await query.message.edit_text(
            text=f"ᴘʀᴇᴍɪᴜᴍ ʙᴇɴᴇғɪᴛs & ᴘᴇʀᴋs\nᴅɪʀᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ʟɪɴᴋs, ɴᴏ ᴀᴅ ʟɪɴᴋs\nsᴘᴇᴄɪᴀʟ ᴀᴄᴄᴇss ɪɴ ᴇᴠᴇɴᴛs\n🎖️ ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs :\n\n● {PRICE1} rs ғᴏʀ 7 ᴅᴀʏs ᴘʀɪᴍᴇ ᴍᴇᴍʙᴇʀsʜɪᴘ\n\n● {PRICE2} rs ғᴏʀ 1 ᴍᴏɴᴛʜ ᴘʀɪᴍᴇ ᴍᴇᴍʙᴇʀsʜɪᴘ\n\n● {PRICE3} rs For 3 ᴍᴏɴᴛʜs ᴘʀɪᴍᴇ ᴍᴇᴍʙᴇʀsʜɪᴘ\n\n● {PRICE4} rs For 6 ᴍᴏɴᴛʜs ᴘʀɪᴍᴇ ᴍᴇᴍʙᴇʀsʜɪᴘ\n\n● {PRICE5} rs For 1 ʏᴇᴀʀ ᴘʀɪᴍᴇ ᴍᴇᴍʙᴇʀsʜɪᴘ\n\n\n💵 UPI ID -  <code>{UPI_ID}</code>\n\n\n📸 QR - ᴅᴍ ʜᴇʀᴇ ᴛᴏ ꜱᴄᴀɴ ǫʀ ({UPI_IMAGE_URL})\n\n♻️ ʜᴇ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ǫʀ ᴄᴏᴅᴇ ᴀɴᴛ ᴛʜᴇɴ ᴅᴏ ᴘᴀʏᴍᴇɴᴛ💰\n\n\n‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ",
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup(
                [   
                    [
                        InlineKeyboardButton("sᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ sᴄʀᴇᴇɴsʜᴏᴛ(ADMIN) 📸", url=(SCREENSHOT_URL))
                    ],
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
            )
