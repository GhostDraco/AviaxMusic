import requests
import re
import json
from urllib3 import disable_warnings
from pyrogram import filters
from AviaxMusic import app

# Disable SSL warnings
disable_warnings()

__HELP__ = """
**ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅᴇʀ**

ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛᴇʀᴀʙᴏx ғɪʟᴇs:

- `/tera` <link>: ғᴇᴛᴄʜ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ғʀᴏᴍ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ

**ᴜsᴀɢᴇ:**
- `/tera https://terabox.com/s/...`
- `/tera https://www.terabox.com/s/...`

**ɴᴏᴛᴇ:**
ᴛʜɪs ᴛᴏᴏʟ ғᴇᴛᴄʜᴇs ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋs ғʀᴏᴍ ᴛᴇʀᴀʙᴏx ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴡᴀᴛᴇʀᴍᴀʀᴋ.
"""

__MODULE__ = "Tᴇʀᴀʙᴏx"

@app.on_message(filters.command("tera"))
def tera_downloader(client, message):
    # Check if link is provided
    if len(message.command) < 2:
        message.reply_text("**ᴜsᴀɢᴇ:** `/tera <terabox_link>`\n\nᴇxᴀᴍᴘʟᴇ: `/tera https://terabox.com/s/example`")
        return
    
    url_input = message.command[1]
    
    # Send initial processing message
    processing_msg = message.reply_text("🔍 **ғᴇᴛᴄʜɪɴɢ ɴᴏɴᴄᴇ...**")
    
    try:
        # Headers for the initial request
        headers_event = {
            "accept": "*/*",
            "content-type": "text/plain",
            "origin": "https://teradownloadr.com",
            "referer": "https://teradownloadr.com/",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        }

        data_event = {
            "n": "pageview",
            "u": "https://teradownloadr.com/",
            "l": ["en-GB", "en-US", "en"],
            "k": "EdmacAlcfkfDwEmll2DHPQ",
            "r": "https://www.google.com/",
            "sw": 360,
            "sh": 800,
            "sr": 3,
            "t": "TeraBox Downloader - Download TeraBox Video + Files (2025)"
        }

        # Get nonce
        processing_msg.edit_text("🔍 **ғᴇᴛᴄʜɪɴɢ ɴᴏɴᴄᴇ...**")
        res = requests.post("https://teradownloadr.com/api/event", 
                          headers=headers_event, 
                          data=json.dumps(data_event), 
                          verify=False)
        
        nonce_match = re.search(r'"nonce":"([a-zA-Z0-9]+)"', res.text)
        
        if nonce_match:
            nonce = nonce_match.group(1)
        else:
            processing_msg.edit_text("⚠️ **ғᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ɴᴏɴᴄᴇ. ᴛʀʏɪɴɢ ᴀʟᴛᴇʀɴᴀᴛᴇ ᴍᴇᴛʜᴏᴅ...**")
            # Try alternative nonce extraction
            nonce_patterns = [r'nonce[=:]"([a-f0-9]+)"', r'"nonce":"([^"]+)"']
            for pattern in nonce_patterns:
                match = re.search(pattern, res.text)
                if match:
                    nonce = match.group(1)
                    break
            else:
                raise Exception("Could not extract nonce")
        
        processing_msg.edit_text("📥 **ғᴇᴛᴄʜɪɴɢ ғɪʟᴇ ɪɴғᴏ...**")
        
        # Prepare final request
        payload = f"action=terabox_fetch&url={requests.utils.quote(url_input)}&nonce={nonce}"
        
        headers_final = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://teradownloadr.com",
            "referer": "https://teradownloadr.com/",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        }

        # Fetch file information
        final_response = requests.post("https://teradownloadr.com/wp-admin/admin-ajax.php", 
                                     headers=headers_final, 
                                     data=payload, 
                                     verify=False)
        
        if final_response.status_code != 200:
            processing_msg.edit_text(f"❌ **ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴅᴀᴛᴀ. sᴛᴀᴛᴜs ᴄᴏᴅᴇ:** {final_response.status_code}")
            return
        
        response_data = final_response.text
        
        # Parse the response
        try:
            # Try to parse as JSON
            data = json.loads(response_data)
            
            if data.get("success"):
                file_info = data.get("data", {})
                
                # Format response message
                response_text = "✅ **ᴛᴇʀᴀʙᴏx ғɪʟᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ**\n\n"
                
                if file_info.get("filename"):
                    response_text += f"📄 **ғɪʟᴇɴᴀᴍᴇ:** `{file_info['filename']}`\n"
                
                if file_info.get("size"):
                    response_text += f"💾 **sɪᴢᴇ:** {file_info['size']}\n"
                
                if file_info.get("duration"):
                    response_text += f"⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** {file_info['duration']}\n"
                
                if file_info.get("download_url"):
                    response_text += f"\n🔗 **ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ:**\n`{file_info['download_url']}`\n"
                
                if file_info.get("direct_url"):
                    response_text += f"\n⚡ **ᴅɪʀᴇᴄᴛ ʟɪɴᴋ:**\n`{file_info['direct_url']}`\n"
                
                # Add original link
                response_text += f"\n🌐 **ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ:**\n`{url_input}`"
                
                processing_msg.edit_text(response_text)
                
                # If there's a download URL, you might want to send it as a separate message
                if file_info.get("download_url"):
                    message.reply_text(f"📥 **ᴅᴏᴡɴʟᴏᴀᴅ:**\n{file_info['download_url']}")
                    
            else:
                error_msg = data.get("data", "Unknown error")
                processing_msg.edit_text(f"❌ **ᴇʀʀᴏʀ:** {error_msg}")
                
        except json.JSONDecodeError:
            # If not JSON, check for direct links in the response
            processing_msg.edit_text("📊 **ᴘᴀʀsɪɴɢ ʀᴇsᴘᴏɴsᴇ...**")
            
            # Look for direct download links
            direct_links = re.findall(r'(https?://[^\s<>"\']+\.(?:mp4|mkv|avi|mov|flv|wmv|m4a|mp3|pdf|zip|rar|7z|docx?|xlsx?|pptx?|txt))', response_data)
            
            if direct_links:
                response_text = "✅ **ғᴏᴜɴᴅ ᴅɪʀᴇᴄᴛ ʟɪɴᴋs:**\n\n"
                for i, link in enumerate(direct_links[:5], 1):  # Show first 5 links
                    response_text += f"{i}. `{link}`\n"
                
                if len(direct_links) > 5:
                    response_text += f"\n... ᴀɴᴅ {len(direct_links) - 5} ᴍᴏʀᴇ"
                
                processing_msg.edit_text(response_text)
            else:
                # Try to extract any useful information
                file_info_match = re.search(r'filename[=:]"([^"]+)"', response_data)
                size_match = re.search(r'size[=:]"?([0-9.]+[KMG]?B)"?', response_data, re.IGNORECASE)
                
                if file_info_match or size_match:
                    response_text = "📄 **ғɪʟᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ:**\n\n"
                    
                    if file_info_match:
                        response_text += f"📄 **ɴᴀᴍᴇ:** `{file_info_match.group(1)}`\n"
                    
                    if size_match:
                        response_text += f"💾 **sɪᴢᴇ:** {size_match.group(1)}\n"
                    
                    processing_msg.edit_text(response_text + f"\n🌐 **ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ:**\n`{url_input}`")
                else:
                    processing_msg.edit_text("📋 **ʀᴀᴡ ʀᴇsᴘᴏɴsᴇ:**\n\n" + response_data[:4000])
    
    except requests.exceptions.RequestException as e:
        processing_msg.edit_text(f"❌ **ɴᴇᴛᴡᴏʀᴋ ᴇʀʀᴏʀ:** {str(e)}")
    
    except Exception as e:
        processing_msg.edit_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}\n\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴡɪᴛʜ ᴀ ᴠᴀʟɪᴅ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ.")
