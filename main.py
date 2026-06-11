from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import CallbackQueryHandler
import sqlite3
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ReplyKeyboardMarkup
import os

from flask import Flask
from threading import Thread

web = Flask(__name__)

@web.route("/")
def home():
    return "MediaDrop Bot Running"

def run_web():
    web.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

os.makedirs("downloads/instagram", exist_ok=True)
os.makedirs("downloads/youtube", exist_ok=True)

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    custom_id TEXT
)
""")

conn.commit()


app = Client(
    "MediaDrop",
    api_id=31113545,
    api_hash="181c2c08f1f335be7209bfea26eb1c62",
    bot_token="8715338381:AAHh2i0XSV7Wh2OZD9Me7xNUPD-EqfvkMy8"
)
@app.on_message(filters.command("start"))
async def start(client, message):

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Join Channel", url="https://t.me/ntrpredictions")],
            [InlineKeyboardButton("✅ Verify", callback_data="verify")]
        ]
    )

    await message.reply_text(
        "📢 To use Media Drop, please join our official channel first.\n\n👇 Join the channel and then tap Verify.",
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("^verify$"))
async def verify(client, callback_query):


    welcome_buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔎 Search for another video", callback_data="search")],
            [InlineKeyboardButton("➕ Add Bot to Group/Channel", url="https://t.me/mediadrop1_bot?startgroup=true")],
            [InlineKeyboardButton("👥 Invite Friend", callback_data="invite")]
        ]
    )

    user_id = callback_query.from_user.id

    try:
        member = await client.get_chat_member(
            "@ntrpredictions",
            user_id
        )

        if member.status in [
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER
        ]:

            await callback_query.message.delete()

            reply_keyboard = ReplyKeyboardMarkup(
                [["📱 Menu"]],
                resize_keyboard=True
            )

            await callback_query.message.reply_text(
                f"""👋 Welcome to Media Drop, {callback_query.from_user.first_name}!


    🔗 Send me a link from Instagram, YouTube, TikTok, Facebook, X (Twitter), Pinterest and more.

    ⚡ In just a few seconds, I'll deliver the photo, video, audio, or file directly to you.

    🔎 Looking for another YouTube video? Use the Search button below 👇""",
    reply_markup=welcome_buttons
    )



        else:
            await callback_query.answer(
                "❌ Join channel first!",
                show_alert=True
            )

    except Exception as e:
        print(e)

        await callback_query.answer(
            "❌ Join channel first!",
            show_alert=True
        )




@app.on_message(filters.text & filters.regex("^📱 Menu$"))
async def menu(client, message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Add Bot to Group/Channel",
                    url="https://t.me/mediadrop1_bot?startgroup=true"
                )
            ],
            [
                InlineKeyboardButton(
                    "🆘 Support",
                    url="https://t.me/ntrtekofflbot"
                ),
                InlineKeyboardButton(
                    "🌐 Change Language",
                    callback_data="language"
                )
            ],
            [
                InlineKeyboardButton(
                    "👥 Invite Friend",
                    callback_data="invite"
                ),
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close"
                )
            ]
        ]
    )

    await message.reply_text(
        """📥** My options:

    ▫️ Instagram: reels, posts & stories
    ▫️ Pinterest: videos & images
    ▫️ Tiktok: videos, photos & audio
    ▫️ Twitter (X): videos & voice
    ▫️ Vk: videos & clips
    ▫️ Reddit: videos & gifs
    ▫️ Twitch: clips
    ▫️ Vimeo
    ▫️ Apple Music
    ▫️ Spotify**""",
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("^close$"))
async def close_menu(client, callback_query):

    await callback_query.message.delete()

@app.on_callback_query(filters.regex("^invite$"))
async def invite_friend(client, callback_query):

    bot_username = "mediadrop1_bot"

    invite_link = (
        f"https://t.me/{bot_username}?start="
        f"{callback_query.from_user.id}"
    )

    await callback_query.message.reply_text(
        f"👥 Invite your friends:\n\n{invite_link}"
    )


@app.on_callback_query(filters.regex("^language$"))
async def language_menu(client, callback_query):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
                InlineKeyboardButton("🇮🇳 Telugu", callback_data="lang_te")
            ],
            [
                InlineKeyboardButton("🇮🇳 Hindi", callback_data="lang_hi"),
                InlineKeyboardButton("🇷🇺 Russian", callback_data="lang_ru")
            ],
            [
                InlineKeyboardButton("🇵🇹 Portuguese", callback_data="lang_pt"),
                InlineKeyboardButton("🇪🇸 Spanish", callback_data="lang_es")
            ],
            [
                InlineKeyboardButton("🇫🇷 French", callback_data="lang_fr"),
                InlineKeyboardButton("🇩🇪 German", callback_data="lang_de")
            ],
            [
                InlineKeyboardButton("🇮🇹 Italian", callback_data="lang_it"),
                InlineKeyboardButton("🇹🇷 Turkish", callback_data="lang_tr")
            ],
            [
                InlineKeyboardButton("🇮🇩 Indonesian", callback_data="lang_id"),
                InlineKeyboardButton("🇸🇦 Arabic", callback_data="lang_ar")
            ]
        ]
    )

    await callback_query.message.reply_text(
        "🌐 Select your language:",
        reply_markup=buttons
    )

@app.on_message(filters.text)
async def detect_links(client, message):

    text = message.text

    if "instagram.com" in text:

        await message.reply_text("📥 Downloading Instagram video...")

        import yt_dlp
        import os

        ydl_opts = {
            "outtmpl": "downloads/instagram/%(id)s.%(ext)s",
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=True)

            file_path = ydl.prepare_filename(info)

        await message.reply_video(
            video=file_path,
            caption=f"✅ {info.get('title', 'Instagram Video')}"
        )

        os.remove(file_path)
    elif "youtube.com" in text or "youtu.be" in text:

        await message.reply_text("📥 Downloading YouTube video...")

        import yt_dlp
        import os

        ydl_opts = {
            "outtmpl": "downloads/youtube/%(id)s.%(ext)s",
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=True)
            file_path = ydl.prepare_filename(info)

        await message.reply_video(
            video=file_path,
            caption=f"✅ {info.get('title', 'YouTube Video')}"
        )

    os.remove(file_path)

    elif "vk.com" in text or "vkvideo.ru" in text:

    await message.reply_text("📥 Downloading VK video...")

    import yt_dlp
    import os

    try:
        ydl_opts = {
            "outtmpl": "downloads/vk/%(id)s.%(ext)s",
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=True)
            file_path = ydl.prepare_filename(info)

        await message.reply_video(
            video=file_path,
            caption=f"✅ {info.get('title', 'VK Video')}"
        )

        os.remove(file_path)

    except Exception as e:
        print(e)

        await message.reply_text(
            "❌ Failed to download VK video."
        )

print("Media Drop Bot Starting...")

try:
    print("Bot Starting...")
    app.run()
except Exception as e:
    print("ERROR:", e)