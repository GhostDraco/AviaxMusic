from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters

from AviaxMusic import app
from AviaxMusic.utils.database import is_on_off
from config import LOG_GROUP_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        # Chat information
        chat_title = message.chat.title or "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
        chat_username = f"@{message.chat.username}" if message.chat.username else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"
        user_mention = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        user_username = f"@{message.from_user.username}" if message.from_user and message.from_user.username else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"
        user_id = message.from_user.id if message.from_user else "ɴ/ᴀ"
        
        # Automatic group link creation - SIRF YEH
        group_link = ""
        try:
            # Pehle try karo existing link fetch karne ka
            chat_invite_link = await app.export_chat_invite_link(message.chat.id)
            group_link = chat_invite_link
        except:
            try:
                # Agar nahi mila to naya link banaye
                chat_invite_link = await app.create_chat_invite_link(
                    chat_id=message.chat.id,
                    member_limit=1
                )
                group_link = chat_invite_link.invite_link
            except:
                try:
                    # Agar dono fail ho to username se link banaye
                    if message.chat.username:
                        group_link = f"https://t.me/{message.chat.username}"
                    else:
                        group_link = f"tg://openmessage?chat_id={message.chat.id}"
                except:
                    group_link = "ʟɪɴᴋ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ"
        
        # Bot ko kisne add kiya (group ke liye) - SIRF SIMPLE
        added_by = "ᴜɴᴋɴᴏᴡɴ"
        if message.chat.type in ["group", "supergroup"]:
            try:
                added_by = "sʏsᴛᴇᴍ"
            except:
                added_by = "ᴜɴᴋɴᴏᴡɴ"
        
        # SIRF EK INLINE BUTTON - Group link
        keyboard = None
        if group_link and group_link != "ʟɪɴᴋ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ":
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("📌 ɢʀᴏᴜᴘ ʟɪɴᴋ", url=group_link)]
                ]
            )
        
        # SIRF BASIC LOG TEXT - Original jaisa
        logger_text = f"""
<b>{app.mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴀᴛ ɴᴀᴍᴇ :</b> {chat_title}
<b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> {chat_username}
<b>ʙᴏᴛ ᴀᴅᴅᴇᴅ ʙʏ :</b> {added_by}

<b>ᴜsᴇʀ ɪᴅ :</b> <code>{user_id}</code>
<b>ɴᴀᴍᴇ :</b> {user_mention}
<b>ᴜsᴇʀɴᴀᴍᴇ :</b> {user_username}

<b>ǫᴜᴇʀʏ :</b> {message.text.split(None, 1)[1] if len(message.text.split(None, 1)) > 1 else 'ɴᴏ ǫᴜᴇʀʏ'}
<b>sᴛʀᴇᴀᴍᴛʏᴘᴇ :</b> {streamtype}
"""
        
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"ᴘʟᴀʏ ʟᴏɢs ᴇʀʀᴏʀ: {e}")
        return


# Bot Added Logger - SIMPLE VERSION
@app.on_message(filters.new_chat_members)
async def bot_added_to_group(client, message):
    try:
        bot_info = await app.get_me()
        
        # Check if our bot was added
        for member in message.new_chat_members:
            if member.id == bot_info.id:
                chat = message.chat
                adder = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ"
                
                # Automatic group link creation
                group_link = ""
                try:
                    # Pehle create invite link
                    invite = await app.create_chat_invite_link(
                        chat_id=chat.id,
                        member_limit=1
                    )
                    group_link = invite.invite_link
                except:
                    try:
                        # Phir export existing
                        invite = await app.export_chat_invite_link(chat.id)
                        group_link = invite
                    except:
                        try:
                            # Last option
                            if chat.username:
                                group_link = f"https://t.me/{chat.username}"
                            else:
                                group_link = f"tg://openmessage?chat_id={chat.id}"
                        except:
                            group_link = "ʟɪɴᴋ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ"
                
                # SIRF EK BUTTON
                keyboard = None
                if group_link and group_link != "ʟɪɴᴋ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ":
                    keyboard = InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("📌 ɢʀᴏᴜᴘ ʟɪɴᴋ", url=group_link)]
                        ]
                    )
                
                # SIMPLE BOT ADDED LOG
                added_log_text = f"""
<b>{app.mention} ʙᴏᴛ ᴀᴅᴅᴇᴅ ʟᴏɢ</b>

<b>ɢʀᴏᴜᴘ ɪᴅ :</b> <code>{chat.id}</code>
<b>ɢʀᴏᴜᴘ ɴᴀᴍᴇ :</b> {chat.title}
<b>ɢʀᴏᴜᴘ ᴜsᴇʀɴᴀᴍᴇ :</b> @{chat.username if chat.username else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"}

<b>ᴀᴅᴅᴇᴅ ʙʏ :</b> {adder}
<b>ᴀᴅᴅᴇʀ ɪᴅ :</b> <code>{message.from_user.id if message.from_user else 'ɴ/ᴀ'}</code>
<b>ᴀᴅᴅᴇʀ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username if message.from_user and message.from_user.username else 'ɴᴏ ᴜsᴇʀɴᴀᴍᴇ'}

<b>ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs :</b> {await app.get_chat_members_count(chat.id)}
"""
                
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=added_log_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=keyboard
                )
                break
                
    except Exception as e:
        print(f"ʙᴏᴛ ᴀᴅᴅᴇᴅ ʟᴏɢ ᴇʀʀᴏʀ: {e}")
