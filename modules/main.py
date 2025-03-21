import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess
import datetime
import io
import logging
import speedtest

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, User
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyromod import listen

from PIL import Image, ImageDraw, ImageFont
import tgcrypto
import cloudscraper

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode

from aiohttp import ClientSession, web

from subprocess import getstatusoutput

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN


# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)



TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDE0MzQzMTMuMTkyLCJkYXRhIjp7Il9pZCI6IjY1NzY4MGFiYWMxYmVkMDAxOGVhN2FjNSIsInVzZXJuYW1lIjoiODg1MTk1MDE5NyIsImZpcnN0TmFtZSI6IkFuc2hpdCIsImxhc3ROYW1lIjoiU2luZ2giLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwicm9sZXMiOlsiNWIyN2JkOTY1ODQyZjk1MGE3NzhjNmVmIl0sImNvdW50cnlHcm91cCI6IklOIiwidHlwZSI6IlVTRVIifSwiaWF0IjoxNzQwODI5NTEzfQ.7iArCe3AwpnZm1Hl9rNkaPn0PY-EUv-bptHJuZEaTfM"

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://text-leech-bot-for-render.onrender.com/")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

# 🔹 Super Admin (Only this ID can manage users)
SUPER_ADMIN = 123456789  # Replace with your Telegram ID

# 🔹 File to store authorized users
AUTH_FILE = "authorized_users.json"

# ✅ Load authorized users
if os.path.exists(AUTH_FILE):
    with open(AUTH_FILE, "r") as f:
        AUTH_USERS = json.load(f)
else:
    AUTH_USERS = [SUPER_ADMIN]

# ✅ Save authorized users
def save_auth_users():
    with open(AUTH_FILE, "w") as f:
        json.dump(AUTH_USERS, f)

# ✅ Authentication Check (Except /start)
def is_authorized(user_id):
    return user_id in AUTH_USERS

# 

# ✅ Handle /auth (Manage Authorized Users)
@bot.on_message(filters.command("auth") & filters.user(SUPER_ADMIN))
async def manage_auth(client, message):
    args = message.text.split()
    
    if len(args) < 3:
        await message.reply_text("Usage:\n/auth add user_id\n/auth remove user_id\n/auth list")
        return
    
    command, action, user_id = args[0], args[1], args[2]

    try:
        user_id = int(user_id)
        if action == "add":
            if user_id not in AUTH_USERS:
                AUTH_USERS.append(user_id)
                save_auth_users()
                await message.reply_text(f"✅ User {user_id} added to authorized list.")
            else:
                await message.reply_text("⚠️ User is already authorized.")
        elif action == "remove":
            if user_id in AUTH_USERS:
                AUTH_USERS.remove(user_id)
                save_auth_users()
                await message.reply_text(f"❌ User {user_id} removed from authorized list.")
            else:
                await message.reply_text("⚠️ User is not authorized.")
        else:
            await message.reply_text("⚠️ Invalid action. Use 'add' or 'remove'.")
    except ValueError:
        await message.reply_text("⚠️ Invalid user ID.")


# ✅ Authentication Wrapper for Commands
def auth_required(func):
    async def wrapper(client, message):
        if not is_authorized(message.from_user.id):
            await message.reply_text("🚫 You are not authorized to use this command.")
            return
        await func(client, message)
    return wrapper

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    if WEBHOOK:
        # Start the web server
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    # Start the bot
    await start_bot()

    # Keep the program running
    try:
        while True:
            await asyncio.sleep(3600)  # Run forever, or until interrupted
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()
    
@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
       f"𝐇𝐞𝐥𝐥𝐨 ❤️\n\n◆〓◆ ❖ Hello I Am  InvisiblexTxT . I will Download urls from your .txt file", reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✜ 𝐉𝐨𝐢𝐧 𝐔𝐩𝐃𝐚𝐭𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 ✜" ,url=f"https://t.me/invisiblebots") ],
                    [
                    InlineKeyboardButton("✜ Nothing ✜" ,url="https://t.me/invisiblebots") ],
                    [
                    InlineKeyboardButton("🦋 𝐅𝐨𝐥𝐥𝐨𝐰 𝐌𝐞 🦋" ,url="https://t.me/invisiblebots") ]                               
            ]))


@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("♦ 𝐒𝐭𝐨𝐩𝐩𝐞𝐭 ♦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("settoken"))
@auth_required
async def set_token(bot: Client, m: Message):
    global TOKEN
    await m.reply_text("🔑 Send the new token")

    input_token: Message = await bot.listen(m.chat.id)
    new_token = input_token.text
    await input_token.delete()

    TOKEN = new_token  # Update the token globally
    await m.reply_text(f"✅ Token updated successfully!")

@bot.on_message(filters.command(["pw"]))
@auth_required
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
        "Send **Auth code** in this manner otherwise bot will not respond.\n\nSend like this:-  **AUTH CODE**"
    )  
    hi1: Message = await bot.listen(editable.chat.id)
    test_txt1 = hi1.text  # Auth Code

    headers = {
        'Host': 'api.penpencil.xyz',
        'authorization': f"Bearer {test_txt1}",
        'client-id': '5eb393ee95fab7468a79d189',
        'client-version': '12.84',
        'user-agent': 'Android',
        'randomid': 'e4307177362e86f1',
        'client-type': 'MOBILE',
        'device-meta': '{APP_VERSION:12.84,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.physicswalb}',
        'content-type': 'application/json; charset=UTF-8',
    }

    await editable.edit("**You have these Batches :-\n\nBatch ID : Batch Name**")
    response = requests.get('https://api.penpencil.xyz/v3/batches/my-batches', headers=headers).json()["data"]
    
    for data in response:
        batch = data["name"]
        aa = f"```{data['name']}```  :  ```{data['_id']}\n```"
        await m.reply_text(aa)

    editable1 = await m.reply_text("**Now send the Batch ID to Download**")
    hi3 = await bot.listen(editable.chat.id)
    test_txt2 = hi3.text  # Batch ID

    response2 = requests.get(f'https://api.penpencil.xyz/v3/batches/{test_txt2}/details', headers=headers).json()["data"]["subjects"]
    await editable1.edit("subject : subjectId")

    vj = ""
    for data in response2:
        tids = data['_id']
        idid = f"{tids}&"
        vj += idid

    editable2 = await m.reply_text(f"**Enter this to download full batch :-**\n```{vj}```")
    hi4 = await bot.listen(editable.chat.id)
    test_txt3 = hi4.text  # Subject IDs

    await m.reply_text("**Enter resolution**")
    hi5: Message = await bot.listen(editable.chat.id)
    test_txt4 = hi5.text  # Resolution

    editable4 = await m.reply_text("Now send the **Thumb URL** Eg : ```https://telegra.ph/file/d9e24878bd4aba05049a1.jpg```\n\nor Send **no**")
    hi6 = await bot.listen(editable.chat.id)
    test_txt5 = hi6.text  # Thumb URL
    thumb = test_txt5

    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = "no"

    try:
        xv = test_txt3.split('&')
        for t in xv:
            params = {'page': '1', 'tag': '', 'contentType': 'exercises-notes-videos', 'ut': ''}
            response3 = requests.get(f'https://api.penpencil.xyz/v2/batches/{test_txt2}/subject/{t}/contents', params=params, headers=headers).json()["data"]

            try:
                for data in response3:
                    class_title = data["topic"]
                    class_url = data["url"].replace("d1d34p8vz63oiq", "d3nzo6itypaz07").replace("mpd", "m3u8").strip()
                    with open(f"{batch}.txt", 'a') as f:
                        f.write(f"{class_title}:{class_url}\n")
            except Exception as e:
                await m.reply_text(str(e))

        await m.reply_document(f"{batch}.txt")
    except Exception as e:
        await m.reply_text(str(e))
                



@bot.on_message(filters.command("speedtest"))
@auth_required
async def speedtest_command(client, message):
    msg = await message.reply_text("⏳ Running speed test... Please wait.")

    try:
        # Run Speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        ping = st.results.ping
        server = st.get_best_server()

        # Speedtest Results in Text
        result_text = f"""
🚀 **Speedtest Results** 🚀
--------------------------------
📥 **Download Speed:** {download_speed:.2f} Mbps  
📤 **Upload Speed:** {upload_speed:.2f} Mbps  
📶 **Ping:** {ping} ms  
🌍 **Server:** {server['name']}, {server['country']}  
🏢 **ISP:** {server['sponsor']}
        """

        # Run Speedtest CLI and Extract Image URL
        os.system("speedtest-cli --share > speedtest.txt")
        image_url = None
        with open("speedtest.txt", "r") as file:
            for line in file:
                if "http" in line:
                    image_url = line.strip()
                    break  # Stop after finding the first URL

        # Download Image and Send
        if image_url:
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                image_path = "speedtest_result.png"
                with open(image_path, "wb") as img_file:
                    img_file.write(img_response.content)
                
                await message.reply_photo(photo=image_path, caption=result_text)
                os.remove(image_path)  # Cleanup downloaded image
            else:
                await message.reply_text("⚠️ Failed to download speedtest image.\n\n" + result_text)
        else:
            await message.reply_text(result_text)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"⚠️ Speedtest failed: {e}")





# 🔹 Dictionary to track users waiting for a .sh file
waiting_for_sh = {}

# ✅ Handle /start (No Auth Required)


# ✅ Handle /sh (Ask for .sh file) - Requires Auth
@bot.on_message(filters.command("sh"))
@auth_required
async def ask_for_sh(client, message):
    """When user types /sh, ask them to send a .sh file."""
    user_id = message.from_user.id
    waiting_for_sh[user_id] = True
    await message.reply_text("📂 Please send a `.sh` file to process.")

# ✅ Handle .sh file upload and process it
@bot.on_message(filters.document)
async def handle_sh_file(client, message):
    """Handle the received .sh file if the user requested processing."""
    user_id = message.from_user.id

    if user_id not in waiting_for_sh or not waiting_for_sh[user_id]:
        await message.reply_text("❌ Please use `/sh` first before sending a `.sh` file.")
        return

    doc = message.document
    if not doc.file_name.endswith(".sh"):
        await message.reply_text("❌ Please send a valid `.sh` file.")
        return

    # Download file
    sh_path = await client.download_media(doc)
    output_path = sh_path.replace(".sh", ".txt")

    # Extract data using regex
    title_pattern = r'(?<=-f ")([^"]+)'  # Matches both .mp4 and .pdf titles
    url_pattern = r'(https?://[^\s"]+)'  # Matches URLs

    titles, urls = [], []

    with open(sh_path, "r", encoding="utf-8") as file:
        for line in file:
            title_match = re.search(title_pattern, line)
            url_match = re.search(url_pattern, line)

            if title_match:
                title = re.sub(r'\.mp4|\.pdf|pdf', '', title_match.group(0), flags=re.IGNORECASE).strip()
                titles.append(title)  
            if url_match:
                urls.append(url_match.group(0))

    with open(output_path, "w", encoding="utf-8") as file:
        for title, url in zip(titles, urls):
            file.write(f"{title} {url}\n")

    await message.reply_document(output_path, caption="📄 Processed output file Extracted By Invisible.")

    # Cleanup
    os.remove(sh_path)
    os.remove(output_path)
    del waiting_for_sh[user_id]
    






@bot.on_message(filters.command(["upload"]))
@auth_required
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text('𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀 𝐓𝐱𝐭 𝐅𝐢𝐥𝐞 𝐒𝐞𝐧𝐝 𝐇𝐞𝐫𝐞 ⏍')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
       with open(x, "r") as f:
           content = f.read()
       content = content.split("\n")
       links = []
       for i in content:
           links.append(i.split("://", 1))
       os.remove(x)
            # print(len(links)
    except:
           await m.reply_text("∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.")
           os.remove(x)
           return
    
   
    await editable.edit(f"∝ 𝐓𝐨𝐭𝐚𝐥 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 𝐀𝐫𝐞 🔗** **{len(links)}**\n\n𝐒𝐞𝐧𝐝 𝐅𝐫𝐨𝐦 𝐖𝐡𝐞𝐫𝐞 𝐘𝐨𝐮 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐈𝐧𝐢𝐭𝐚𝐥 𝐢𝐬 **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("∝ 𝐍𝐨𝐰 𝐏𝐥𝐞𝐚𝐬𝐞 𝐒𝐞𝐧𝐝 𝐌𝐞 𝐘𝐨𝐮𝐫 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    await editable.edit("∝ Now Please Send You App Name ")
    input15: Message = await bot.listen(editable.chat.id)
    hi_text0 = input15.text
    await input15.delete(True)
    

    await editable.edit("∝ 𝐄𝐧𝐭𝐞𝐫 𝐄𝐞𝐬𝐨𝐥𝐮𝐭𝐢𝐨𝐧 🎬\n☞ 144,240,360,480,720,1080\nPlease Choose Quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    

    await editable.edit("✏️ Now Enter A Caption to add caption on your uploaded file")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'Robin':
        MR = highlighter 
    else:
        MR = raw_text3
   
    await editable.edit("🌄 Now send the Thumb url\nEg »\n\n Or if don't want thumbnail send = no")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url']

            elif '/master.mpd' in url:
             id =  url.split("/")[-2]
             url = f"https://madxapi-d0cbf6ac738c.herokuapp.com/{id}/master.m3u8?token={TOKEN}"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                
                cc = f'**[ 🎥 ] Vid_ID:** {str(count).zfill(3)}.** {𝗻𝗮𝗺𝗲𝟭}.mkv\n\n✉️ 𝐁𝐚𝐭𝐜𝐡 » {raw_text0}\n\n App Name » {hi_text0} \n\n Downloaded By -{MR}**'
                cc1 = f'**[ 📁 ] Pdf_ID:** {str(count).zfill(3)}. {𝗻𝗮𝗺𝗲𝟭}.pdf\n\n✉️ 𝐁𝐚𝐭𝐜𝐡 » {raw_text0}\n\n App Name » {hi_text0} \n\n  Downloaded By -{MR}**'
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                
                elif ".pdf" in url:
                    try:
                        Show = f"❊⟱ ⥥ 🄳🄾🅆🄽🄻🄾🄰🄳🄸🄽🄶⬇️⬇️... »⟱❊ »\n\n📝 𝐍𝐚𝐦𝐞 » `{name}\n`\n\n**🔗 𝐔𝐑𝐋 »** `@invisiblebots`"
                        prog = await m.reply_text(Show)
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        await prog.delete(True)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    Show = f"❊⟱ ⥥ 🄳🄾🅆🄽🄻🄾🄰🄳🄸🄽🄶⬇️⬇️... »⟱❊ »\n\n📝 𝐍𝐚𝐦𝐞 » `{name}\n⌨ Quality » {raw_text2}`\n\n**🔗 𝐔𝐑𝐋 »** `@Invisiblebots`"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"⌘ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n{str(e)}\n⌘ 𝐍𝐚𝐦𝐞 » {name}\n⌘ "
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞")

print("""
█░█░█ █▀█ █▀█ █▀▄ █▀▀ █▀█ ▄▀█ █▀▀ ▀█▀     ▄▀█ █▀ █░█ █░█ ▀█▀ █▀█ █▀ █░█   ░ █▀▀
▀▄▀▄▀ █▄█ █▄█ █▄▀ █▄▄ █▀▄ █▀█ █▀░ ░█░     █▀█ ▄█ █▀█ █▄█ ░█░ █▄█ ▄█ █▀█   ▄ █▄█""")
print("""✅ 𝐃𝐞𝐩𝐥𝐨𝐲 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 ✅""")
print("""✅ 𝐁𝐨𝐭 𝐖𝐨𝐫𝐤𝐢𝐧𝐠 ✅""")

bot.run()
if __name__ == "__main__":
    asyncio.run(main())
