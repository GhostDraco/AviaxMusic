import requests
import re
from urllib.parse import urljoin, urlparse
from pyrogram import filters
from AviaxMusic import app
from bs4 import BeautifulSoup
import json

__HELP__ = """
**ʟɪɴᴋ ᴇxᴛʀᴀᴄᴛᴏʀ ᴍᴏᴅᴜʟᴇ**

ᴇxᴛʀᴀᴄᴛ ᴀʟʟ ʟɪɴᴋs ᴀɴᴅ ᴀᴘɪ ᴇɴᴅᴘᴏɪɴᴛs ғʀᴏᴍ ᴀ ᴡᴇʙsɪᴛᴇ.

**ᴄᴏᴍᴍᴀɴᴅs:**
- `/extract <url>` - ᴇxᴛʀᴀᴄᴛ ᴀʟʟ ʟɪɴᴋs ᴀɴᴅ ᴀᴘɪ ᴇɴᴅᴘᴏɪɴᴛs
- `/extract <url> link` - ᴇxᴛʀᴀᴄᴛ ᴏɴʟʏ ʀᴇɢᴜʟᴀʀ ʟɪɴᴋs
- `/extract <url> api` - ᴇxᴛʀᴀᴄᴛ ᴏɴʟʏ ᴀᴘɪ ᴇɴᴅᴘᴏɪɴᴛs

**ᴇxᴀᴍᴘʟᴇs:**
- `/extract https://example.com`
- `/extract example.com api`
- `/extract https://api.example.com both`

**ᴘᴀʀᴀᴍᴇᴛᴇʀs:**
- `url`: ᴡᴇʙsɪᴛᴇ URL (ᴡɪᴛʜ ᴏʀ ᴡɪᴛʜᴏᴜᴛ https://)
- `type` (ᴏᴘᴛɪᴏɴᴀʟ): `link`, `api`, ᴏʀ `both` (ᴅᴇғᴀᴜʟᴛ)
"""

__MODULE__ = "LɪɴᴋExᴛʀᴀᴄᴛ"

class LinkExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def normalize_url(self, url):
        """Add https:// if not present"""
        if not re.match(r'^https?://', url, re.IGNORECASE):
            url = 'https://' + url
        return url
    
    def is_valid_url(self, url):
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def is_api_endpoint(self, url):
        """Check if URL looks like an API endpoint"""
        api_patterns = [
            r'/api/', r'\.php$', r'\.json$', r'\.xml$', 
            r'\.aspx$', r'/v[0-9]+/', r'/endpoint', r'/graphql',
            r'/rest/', r'/soap/', r'/rpc/', r'api\.', r'\.ashx$',
            r'/ajax/', r'/fetch', r'/data', r'/query'
        ]
        
        url_lower = url.lower()
        for pattern in api_patterns:
            if re.search(pattern, url_lower):
                return True
        
        # Check for common API parameter patterns
        api_params = ['api_key=', 'token=', 'access_token=', 'apikey=', 'auth=']
        if any(param in url_lower for param in api_params):
            return True
            
        return False
    
    def extract_links(self, url, extract_type="both"):
        """Main extraction function"""
        try:
            # Normalize URL
            url = self.normalize_url(url)
            
            if not self.is_valid_url(url):
                return {"status": False, "error": "Invalid URL format"}
            
            # Fetch HTML content
            response = self.session.get(url, timeout=10, verify=False)
            response.raise_for_status()
            
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            all_links = set()
            api_links = set()
            
            # Extract all links
            for tag in soup.find_all(['a', 'link', 'script', 'img', 'iframe', 'form']):
                href = None
                
                if tag.name == 'a' and tag.get('href'):
                    href = tag.get('href')
                elif tag.name == 'link' and tag.get('href'):
                    href = tag.get('href')
                elif tag.name == 'script' and tag.get('src'):
                    href = tag.get('src')
                elif tag.name == 'img' and tag.get('src'):
                    href = tag.get('src')
                elif tag.name == 'iframe' and tag.get('src'):
                    href = tag.get('src')
                elif tag.name == 'form' and tag.get('action'):
                    href = tag.get('action')
                
                if href:
                    # Skip invalid links
                    if href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                        continue
                    
                    # Make absolute URL
                    absolute_url = urljoin(url, href)
                    
                    # Clean URL
                    absolute_url = absolute_url.split('#')[0].split('?')[0]
                    
                    if self.is_valid_url(absolute_url):
                        all_links.add(absolute_url)
                        
                        # Check if it's an API endpoint
                        if self.is_api_endpoint(absolute_url):
                            api_links.add(absolute_url)
            
            # Also extract from JavaScript and CSS
            js_pattern = r'["\'](https?://[^"\'\s]+)["\']'
            js_links = re.findall(js_pattern, response.text)
            
            for js_link in js_links:
                if self.is_valid_url(js_link):
                    all_links.add(js_link)
                    if self.is_api_endpoint(js_link):
                        api_links.add(js_link)
            
            # Convert sets to sorted lists
            all_links = sorted(list(all_links))
            api_links = sorted(list(api_links))
            
            # Prepare response based on extract_type
            if extract_type == "link":
                data = all_links
            elif extract_type == "api":
                data = api_links
            else:  # both
                data = {
                    "all_links": all_links,
                    "api_links": api_links
                }
            
            return {
                "status": True,
                "host": urlparse(url).netloc,
                "mode": extract_type,
                "total_links": len(all_links),
                "api_links_count": len(api_links),
                "data": data,
                "developer": "@xFlexyy",
                "telegram": "@ScriptFlix_Bots"
            }
            
        except requests.exceptions.RequestException as e:
            return {"status": False, "error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"status": False, "error": f"Extraction error: {str(e)}"}

# Initialize extractor
extractor = LinkExtractor()

@app.on_message(filters.command("extract"))
def extract_links_command(client, message):
    """Handle /extract command"""
    try:
        args = message.text.split()[1:]  # Skip command
        
        if not args:
            message.reply_text(
                "**ᴜsᴀɢᴇ:**\n"
                "`/extract <url>` - ᴇxᴛʀᴀᴄᴛ ᴀʟʟ ʟɪɴᴋs\n"
                "`/extract <url> link` - ᴏɴʟʏ ʟɪɴᴋs\n"
                "`/extract <url> api` - ᴏɴʟʏ ᴀᴘɪ ᴇɴᴅᴘᴏɪɴᴛs\n"
                "`/extract <url> both` - ʙᴏᴛʜ ʟɪɴᴋs & ᴀᴘɪs\n\n"
                "**ᴇxᴀᴍᴘʟᴇ:** `/extract https://example.com api`"
            )
            return
        
        url = args[0]
        extract_type = args[1] if len(args) > 1 else "both"
        
        # Validate extract_type
        if extract_type not in ["link", "api", "both"]:
            extract_type = "both"
        
        # Send processing message
        processing_msg = message.reply_text(f"🔍 **ᴇxᴛʀᴀᴄᴛɪɴɢ ʟɪɴᴋs ғʀᴏᴍ:** `{url}`\n**ᴍᴏᴅᴇ:** `{extract_type}`")
        
        # Extract links
        result = extractor.extract_links(url, extract_type)
        
        if not result["status"]:
            processing_msg.edit_text(f"❌ **ᴇʀʀᴏʀ:** {result.get('error', 'Unknown error')}")
            return
        
        # Format response
        response_text = f"""
✅ **ʟɪɴᴋ ᴇxᴛʀᴀᴄᴛɪᴏɴ ᴄᴏᴍᴘʟᴇᴛᴇ**

🌐 **ʜᴏsᴛ:** `{result['host']}`
📊 **ᴍᴏᴅᴇ:** `{result['mode']}`
🔗 **ᴛᴏᴛᴀʟ ʟɪɴᴋs:** `{result['total_links']}`
⚡ **ᴀᴘɪ ʟɪɴᴋs:** `{result['api_links_count']}`
👨‍💻 **ᴅᴇᴠᴇʟᴏᴘᴇʀ:** {result['developer']}
📱 **ᴛᴇʟᴇɢʀᴀᴍ:** {result['telegram']}
"""
        
        # Send the summary
        processing_msg.edit_text(response_text)
        
        # Send extracted data in chunks
        if extract_type == "link":
            links = result["data"]
            if links:
                # Send links in batches
                batch_size = 20
                for i in range(0, len(links), batch_size):
                    batch = links[i:i + batch_size]
                    links_text = "**📄 ᴇxᴛʀᴀᴄᴛᴇᴅ ʟɪɴᴋs:**\n\n" + "\n".join([f"{j+1}. `{link}`" for j, link in enumerate(batch, i+1)])
                    if i + batch_size < len(links):
                        links_text += f"\n\n... ᴀɴᴅ {len(links) - (i + batch_size)} ᴍᴏʀᴇ"
                    
                    # Split if message is too long
                    if len(links_text) > 4000:
                        chunks = [links_text[j:j+4000] for j in range(0, len(links_text), 4000)]
                        for chunk in chunks:
                            message.reply_text(chunk)
                    else:
                        message.reply_text(links_text)
            else:
                message.reply_text("❌ **ɴᴏ ʟɪɴᴋs ғᴏᴜɴᴅ**")
        
        elif extract_type == "api":
            apis = result["data"]
            if apis:
                # Send API links in batches
                batch_size = 15
                for i in range(0, len(apis), batch_size):
                    batch = apis[i:i + batch_size]
                    apis_text = "**⚡ ᴀᴘɪ ᴇɴᴅᴘᴏɪɴᴛs:**\n\n" + "\n".join([f"{j+1}. `{api}`" for j, api in enumerate(batch, i+1)])
                    if i + batch_size < len(apis):
                        apis_text += f"\n\n... ᴀɴᴅ {len(apis) - (i + batch_size)} ᴍᴏʀᴇ"
                    
                    # Split if message is too long
                    if len(apis_text) > 4000:
                        chunks = [apis_text[j:j+4000] for j in range(0, len(apis_text), 4000)]
                        for chunk in chunks:
                            message.reply_text(chunk)
                    else:
                        message.reply_text(apis_text)
            else:
                message.reply_text("❌ **ɴᴏ ᴀᴘɪ ᴇɴᴅᴘᴏɪɴᴛs ғᴏᴜɴᴅ**")
        
        else:  # both
            # Send all links
            all_links = result["data"]["all_links"]
            api_links = result["data"]["api_links"]
            
            if all_links:
                message.reply_text(f"**🔗 ᴀʟʟ ʟɪɴᴋs ({len(all_links)}):**\n`{all_links[0]}`\n\n... ᴀɴᴅ {len(all_links)-1} ᴍᴏʀᴇ")
            
            if api_links:
                message.reply_text(f"**⚡ ᴀᴘɪ ʟɪɴᴋs ({len(api_links)}):**\n`{api_links[0]}`\n\n... ᴀɴᴅ {len(api_links)-1} ᴍᴏʀᴇ")
            
            if not all_links and not api_links:
                message.reply_text("❌ **ɴᴏ ʟɪɴᴋs ғᴏᴜɴᴅ**")
        
        # Send JSON data as file if there are many links
        if result["total_links"] > 30:
            json_data = json.dumps(result, indent=2, ensure_ascii=False)
            message.reply_document(
                document=json_data.encode(),
                file_name=f"extracted_links_{result['host']}.json",
                caption=f"📁 **ғᴜʟʟ ᴇxᴛʀᴀᴄᴛᴇᴅ ᴅᴀᴛᴀ**\n\n🌐 {result['host']}\n🔗 {result['total_links']} ʟɪɴᴋs\n⚡ {result['api_links_count']} ᴀᴘɪs"
            )
    
    except Exception as e:
        message.reply_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}\n\nᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ URL ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.")

@app.on_message(filters.command("extractjson"))
def extract_json_command(client, message):
    """Handle /extractjson command to get only JSON output"""
    try:
        args = message.text.split()[1:]
        
        if not args:
            message.reply_text("**ᴜsᴀɢᴇ:** `/extractjson <url>`")
            return
        
        url = args[0]
        extract_type = args[1] if len(args) > 1 else "both"
        
        processing_msg = message.reply_text(f"🔍 **ᴇxᴛʀᴀᴄᴛɪɴɢ ᴊsᴏɴ ᴅᴀᴛᴀ ғʀᴏᴍ:** `{url}`")
        
        result = extractor.extract_links(url, extract_type)
        
        if not result["status"]:
            processing_msg.edit_text(f"❌ **ᴇʀʀᴏʀ:** {result.get('error', 'Unknown error')}")
            return
        
        # Send as JSON file
        json_data = json.dumps(result, indent=2, ensure_ascii=False)
        
        processing_msg.delete()
        
        message.reply_document(
            document=json_data.encode(),
            file_name=f"extracted_{result['host']}.json",
            caption=f"📁 **ʟɪɴᴋ ᴇxᴛʀᴀᴄᴛɪᴏɴ ʀᴇsᴜʟᴛs**\n\n"
                   f"🌐 **ʜᴏsᴛ:** {result['host']}\n"
                   f"📊 **ᴍᴏᴅᴇ:** {result['mode']}\n"
                   f"🔗 **ᴛᴏᴛᴀʟ ʟɪɴᴋs:** {result['total_links']}\n"
                   f"⚡ **ᴀᴘɪ ʟɪɴᴋs:** {result['api_links_count']}\n"
                   f"👨‍💻 **ʙʏ:** {result['developer']}"
        )
    
    except Exception as e:
        message.reply_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}")
