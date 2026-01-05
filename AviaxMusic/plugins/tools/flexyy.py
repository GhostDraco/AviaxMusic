import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from AviaxMusic import app
from config import SUPPORT_GROUP

BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ", url=SUPPORT_GROUP)]]
)

MEDIA = {
    "cutie": "https://graph.org/file/24375c6e54609c0e4621c.mp4",
    "horny": "https://graph.org/file/eaa834a1cbfad29bd1fe4.mp4",
    "hot": "https://graph.org/file/745ba3ff07c1270958588.mp4",
    "sexy": "https://graph.org/file/58da22eb737af2f8963e6.mp4",
    "gay": "https://graph.org/file/850290f1f974c5421ce54.mp4",
    "lesbian": "https://graph.org/file/ff258085cf31f5385db8a.mp4",
    "boob": "https://i.gifer.com/8ZUg.gif",
    "cock": "https://telegra.ph/file/423414459345bf18310f5.gif",
}

TEMPLATES = {
    "cutie": "🍑 {mention} ɪꜱ **{percent}%** ᴄᴜᴛᴇ ʙᴀʙʏ 🥀",
    "horny": "🔥 {mention} ɪꜱ **{percent}%** ʜᴏʀɴʏ!",
    "hot": "🔥 {mention} ɪꜱ **{percent}%** ʜᴏᴛ!",
    "sexy": "💋 {mention} ɪꜱ **{percent}%** ꜱᴇxʏ!",
    "gay": "🍷 {mention} ɪꜱ **{percent}%** ɢᴀʏ!",
    "lesbian": "💜 {mention} ɪꜱ **{percent}%** ʟᴇꜱʙɪᴀɴ!",
    "boob": "🍒 {mention} ʙᴏᴏʙ ꜱɪᴢᴇ **{percent}%**!",
    "cock": "🍆 {mention} ᴄᴏᴄᴋ ꜱɪᴢᴇ **{percent}ᴄᴍ**!",
}


def user_mention(user) -> str:
    return f"[{user.first_name}](tg://user?id={user.id})"


async def rate_user(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "❌ **Kisi user ko reply karke command use karo!**",
            quote=True,
        )

    command = message.command[0].lower()
    if command not in MEDIA:
        return

    target = message.reply_to_message.from_user
    mention = user_mention(target)
    percent = random.randint(1, 100)

    caption = TEMPLATES[command].format(
        mention=mention,
        percent=percent,
    )

    media = MEDIA[command]

    if media.endswith(".gif"):
        await message.reply_animation(
            animation=media,
            caption=caption,
            reply_markup=BUTTON,
        )
    else:
        await message.reply_video(
            video=media,
            caption=caption,
            reply_markup=BUTTON,
        )


for cmd in MEDIA.keys():
    app.on_message(filters.command(cmd))(rate_user)
