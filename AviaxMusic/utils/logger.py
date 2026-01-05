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
        
        # Automatic group link creation
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
        
        # Bot ko kisne add kiya (group ke liye)
        added_by = "ᴜɴᴋɴᴏᴡɴ"
        if message.chat.type in ["group", "supergroup"]:
            try:
                bot_info = await app.get_me()
                added_by = "sʏsᴛᴇᴍ"
                
                # Bot ke chat history check karo
                try:
                    async for msg in app.search_messages(
                        chat_id=message.chat.id,
                        query="start",
                        limit=10
                    ):
                        if msg.from_user and msg.from_user.id != bot_info.id:
                            added_by = f"{msg.from_user.mention}"
                            break
                except:
                    pass
                    
            except Exception as e:
                added_by = f"sʏsᴛᴇᴍ - {str(e)[:20]}"
        
        # Other bots in group detection
        other_bots = []
        bot_count = 0
        try:
            async for member in app.get_chat_members(message.chat.id):
                if member.user.is_bot and member.user.id != (await app.get_me()).id:
                    bot_count += 1
                    bot_info = f"{member.user.first_name}"
                    if member.user.username:
                        bot_info += f" (@{member.user.username})"
                    other_bots.append(bot_info)
        except:
            pass
        
        # Inline keyboard buttons
        keyboard_buttons = []
        
        # Group link button
        if group_link and group_link != "ʟɪɴᴋ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ":
            keyboard_buttons.append(
                [InlineKeyboardButton("📌 ɢʀᴏᴜᴘ ʟɪɴᴋ", url=group_link)]
            )
        
        # User profile button
        if user_id != "ɴ/ᴀ":
            keyboard_buttons.append(
                [InlineKeyboardButton("👤 ᴜsᴇʀ ᴘʀᴏғɪʟᴇ", url=f"tg://user?id={user_id}")]
            )
        
        # Chat button
        keyboard_buttons.append(
            [InlineKeyboardButton("💬 ᴏᴘᴇɴ ᴄʜᴀᴛ", url=f"tg://openmessage?chat_id={message.chat.id}")]
        )
        
        keyboard = InlineKeyboardMarkup(keyboard_buttons) if keyboard_buttons else None
        
        # Main logger text with original formatting style
        logger_text = f"""
<b>{app.mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴀᴛ ɴᴀᴍᴇ :</b> {chat_title}
<b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> {chat_username}
<b>ᴄʜᴀᴛ ᴛʏᴘᴇ :</b> {message.chat.type}
<b>ʙᴏᴛ ᴀᴅᴅᴇᴅ ʙʏ :</b> {added_by}

<b>ᴜsᴇʀ ɪᴅ :</b> <code>{user_id}</code>
<b>ɴᴀᴍᴇ :</b> {user_mention}
<b>ᴜsᴇʀɴᴀᴍᴇ :</b> {user_username}

<b>ǫᴜᴇʀʏ :</b> {message.text.split(None, 1)[1] if len(message.text.split(None, 1)) > 1 else 'ɴᴏ ǫᴜᴇʀʏ'}
<b>sᴛʀᴇᴀᴍᴛʏᴘᴇ :</b> {streamtype}

<b>ᴏᴛʜᴇʀ ʙᴏᴛs ɪɴ ɢʀᴏᴜᴘ :</b> {bot_count}
"""
        
        # Agar other bots hain to unki list add karo
        if other_bots:
            bots_list = "\n".join([f"├ 🤖 {bot}" for bot in other_bots[:5]])
            if len(other_bots) > 5:
                bots_list += f"\n└ ➕ {len(other_bots) - 5} ᴍᴏʀᴇ ʙᴏᴛs..."
            logger_text += f"\n<b>ʙᴏᴛs ʟɪsᴛ :</b>\n{bots_list}"
        
        logger_text += f"\n<b>ɢʀᴏᴜᴘ ʟɪɴᴋ :</b> {group_link}"
        
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


# Bot Added Logger - Jab bhi bot ko group mein add kare
@app.on_message(filters.new_chat_members)
async def bot_added_to_group(client, message):
    try:
        bot_info = await app.get_me()
        
        # Check if our bot was added
        for member in message.new_chat_members:
            if member.id == bot_info.id:
                chat = message.chat
                adder = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ"
                
                # Automatic group link creation for new group
                group_link = ""
                try:
                    # Pehle create invite link
                    invite = await app.create_chat_invite_link(
                        chat_id=chat.id,
                        member_limit=1,
                        name=f"Log_Link_{chat.id}"
                    )
                    group_link = invite.invite_link
                except:
                    try:
                        # Phir export existing
                        invite = await app.export_chat_invite_link(chat.id)
                        group_link = invite
                    except:
                        try:
                            # Last option - username se
                            if chat.username:
                                group_link = f"https://t.me/{chat.username}"
                            else:
                                group_link = f"tg://openmessage?chat_id={chat.id}"
                        except:
                            group_link = "ʟɪɴᴋ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ"
                
                # Check other bots in the group
                other_bots = []
                bot_count = 0
                try:
                    async for member in app.get_chat_members(chat.id):
                        if member.user.is_bot and member.user.id != bot_info.id:
                            bot_count += 1
                            bot_info_text = f"{member.user.first_name}"
                            if member.user.username:
                                bot_info_text += f" (@{member.user.username})"
                            other_bots.append(bot_info_text)
                except:
                    pass
                
                # Inline buttons
                keyboard_buttons = []
                
                if group_link and group_link != "ʟɪɴᴋ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ":
                    keyboard_buttons.append(
                        [InlineKeyboardButton("📌 ɢʀᴏᴜᴘ ʟɪɴᴋ", url=group_link)]
                    )
                
                if message.from_user:
                    keyboard_buttons.append(
                        [InlineKeyboardButton("👤 ᴀᴅᴅᴇᴅ ʙʏ", url=f"tg://user?id={message.from_user.id}")]
                    )
                
                keyboard_buttons.append(
                    [InlineKeyboardButton("💬 ᴏᴘᴇɴ ᴄʜᴀᴛ", url=f"tg://openmessage?chat_id={chat.id}")]
                )
                
                keyboard = InlineKeyboardMarkup(keyboard_buttons)
                
                # Bot added log message with same font style
                added_log_text = f"""
<b>{app.mention} ʙᴏᴛ ᴀᴅᴅᴇᴅ ʟᴏɢ</b>

<b>ɢʀᴏᴜᴘ ɪᴅ :</b> <code>{chat.id}</code>
<b>ɢʀᴏᴜᴘ ɴᴀᴍᴇ :</b> {chat.title}
<b>ɢʀᴏᴜᴘ ᴜsᴇʀɴᴀᴍᴇ :</b> @{chat.username if chat.username else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"}
<b>ɢʀᴏᴜᴘ ᴛʏᴘᴇ :</b> {chat.type}

<b>ᴀᴅᴅᴇᴅ ʙʏ :</b> {adder}
<b>ᴀᴅᴅᴇʀ ɪᴅ :</b> <code>{message.from_user.id if message.from_user else 'ɴ/ᴀ'}</code>
<b>ᴀᴅᴅᴇʀ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username if message.from_user and message.from_user.username else 'ɴᴏ ᴜsᴇʀɴᴀᴍᴇ'}

<b>ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs :</b> {await app.get_chat_members_count(chat.id)}
<b>ᴏᴛʜᴇʀ ʙᴏᴛs :</b> {bot_count}
<b>ɢʀᴏᴜᴘ ʟɪɴᴋ :</b> {group_link}
"""
                
                # Agar other bots hain to unki list add karo
                if other_bots:
                    bots_list = "\n".join([f"├ 🤖 {bot}" for bot in other_bots[:5]])
                    if len(other_bots) > 5:
                        bots_list += f"\n└ ➕ {len(other_bots) - 5} ᴍᴏʀᴇ ʙᴏᴛs..."
                    added_log_text += f"\n<b>ʙᴏᴛs ʟɪsᴛ :</b>\n{bots_list}"
                
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


# Bot Removed Logger - Jab bhi bot ko group se nikale
@app.on_message(filters.left_chat_member)
async def bot_removed_from_group(client, message):
    try:
        bot_info = await app.get_me()
        
        # Check if our bot was removed
        if message.left_chat_member and message.left_chat_member.id == bot_info.id:
            chat = message.chat
            remover = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ"
            
            # Inline buttons
            keyboard_buttons = []
            
            # Chat button
            keyboard_buttons.append(
                [InlineKeyboardButton("💬 ᴏᴘᴇɴ ᴄʜᴀᴛ", url=f"tg://openmessage?chat_id={chat.id}")]
            )
            
            if message.from_user:
                keyboard_buttons.append(
                    [InlineKeyboardButton("👤 ʀᴇᴍᴏᴠᴇᴅ ʙʏ", url=f"tg://user?id={message.from_user.id}")]
                )
            
            keyboard = InlineKeyboardMarkup(keyboard_buttons)
            
            # Bot removed log message
            removed_log_text = f"""
<b>{app.mention} ʙᴏᴛ ʀᴇᴍᴏᴠᴇᴅ ʟᴏɢ</b>

<b>ɢʀᴏᴜᴘ ɪᴅ :</b> <code>{chat.id}</code>
<b>ɢʀᴏᴜᴘ ɴᴀᴍᴇ :</b> {chat.title}
<b>ɢʀᴏᴜᴘ ᴜsᴇʀɴᴀᴍᴇ :</b> @{chat.username if chat.username else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"}
<b>ɢʀᴏᴜᴘ ᴛʏᴘᴇ :</b> {chat.type}

<b>ʀᴇᴍᴏᴠᴇᴅ ʙʏ :</b> {remover}
<b>ʀᴇᴍᴏᴠᴇʀ ɪᴅ :</b> <code>{message.from_user.id if message.from_user else 'ɴ/ᴀ'}</code>
<b>ʀᴇᴍᴏᴠᴇʀ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username if message.from_user and message.from_user.username else 'ɴᴏ ᴜsᴇʀɴᴀᴍᴇ'}

<b>ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs :</b> {await app.get_chat_members_count(chat.id)}
<b>ᴅᴀᴛᴇ :</b> {message.date}

<b>⚠️ ʙᴏᴛ ᴡᴀs ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴛʜɪs ɢʀᴏᴜᴘ</b>
"""
            
            await app.send_message(
                chat_id=LOG_GROUP_ID,
                text=removed_log_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=keyboard
            )
                
    except Exception as e:
        print(f"ʙᴏᴛ ʀᴇᴍᴏᴠᴇᴅ ʟᴏɢ ᴇʀʀᴏʀ: {e}")


# Group chat member updates logger
@app.on_chat_member_updated()
async def chat_member_updates(client, chat_member_updated):
    try:
        bot_info = await app.get_me()
        chat = chat_member_updated.chat
        
        # Check if bot's status changed
        if chat_member_updated.old_chat_member and chat_member_updated.new_chat_member:
            if chat_member_updated.old_chat_member.user.id == bot_info.id:
                old_status = chat_member_updated.old_chat_member.status
                new_status = chat_member_updated.new_chat_member.status
                
                # Agar bot ko kick/ban kiya gaya ho
                if old_status == "member" and new_status in ["kicked", "left"]:
                    remover = chat_member_updated.from_user.mention if chat_member_updated.from_user else "ᴜɴᴋɴᴏᴡɴ"
                    
                    log_text = f"""
<b>{app.mention} ʙᴏᴛ ᴋɪᴄᴋᴇᴅ/ʟᴇғᴛ ʟᴏɢ</b>

<b>ɢʀᴏᴜᴘ ɪᴅ :</b> <code>{chat.id}</code>
<b>ɢʀᴏᴜᴘ ɴᴀᴍᴇ :</b> {chat.title}
<b>ɢʀᴏᴜᴘ ᴜsᴇʀɴᴀᴍᴇ :</b> @{chat.username if chat.username else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"}

<b>ᴘʀᴇᴠɪᴏᴜs sᴛᴀᴛᴜs :</b> {old_status}
<b>ɴᴇᴡ sᴛᴀᴛᴜs :</b> {new_status}
<b>ᴀᴄᴛɪᴏɴ ʙʏ :</b> {remover}
<b>ᴀᴄᴛɪᴏɴ ʙʏ ɪᴅ :</b> <code>{chat_member_updated.from_user.id if chat_member_updated.from_user else 'ɴ/ᴀ'}</code>

<b>ᴅᴀᴛᴇ :</b> {chat_member_updated.date}

<b>🚫 ʙᴏᴛ ᴡᴀs {new_status.upper()} ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ</b>
"""
                    
                    await app.send_message(
                        chat_id=LOG_GROUP_ID,
                        text=log_text,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True
                    )
                    
    except Exception as e:
        print(f"ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀ ᴜᴘᴅᴀᴛᴇ ʟᴏɢ ᴇʀʀᴏʀ: {e}")
