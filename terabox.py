from aria2p import API as Aria2API, Client as Aria2Client
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import os
import logging
import math
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pymongo import MongoClient
from pyrogram.enums import MessagesFilter
import time
import urllib.parse
from urllib.parse import urlparse
import json
import io
import requests
import re
import secrets
from flask import Flask, render_template
from threading import Thread
from translations import TRANSLATIONS, LANGUAGES, LANGUAGE_CODES

load_dotenv('config.env', override=True)
logging.basicConfig(
    level=logging.INFO,  
    format="[%(asctime)s - %(name)s - %(levelname)s] %(message)s - %(filename)s:%(lineno)d"
)

logger = logging.getLogger(__name__)

logging.getLogger("pyrogram.session").setLevel(logging.ERROR)
logging.getLogger("pyrogram.connection").setLevel(logging.ERROR)
logging.getLogger("pyrogram.dispatcher").setLevel(logging.ERROR)

aria2 = Aria2API(
    Aria2Client(
        host="http://localhost",
        port=6800,
        secret=""
    )
)
options = {
    "max-tries": "50",
    "retry-wait": "3",
    "continue": "true",
    "allow-overwrite": "true",
    "min-split-size": "4M",
    "split": "10",
    "connect-timeout": "30",
    "timeout": "120"
}

aria2.set_global_options(options)

API_ID = os.environ.get('TELEGRAM_API', '')
if len(API_ID) == 0:
    logging.error("TELEGRAM_API variable is missing! Exiting now")
    exit(1)

API_HASH = os.environ.get('TELEGRAM_HASH', '')
if len(API_HASH) == 0:
    logging.error("TELEGRAM_HASH variable is missing! Exiting now")
    exit(1)
    
BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    logging.error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

DUMP_CHAT_ID = os.environ.get('DUMP_CHAT_ID', '')
if len(DUMP_CHAT_ID) == 0:
    logging.error("DUMP_CHAT_ID variable is missing! Exiting now")
    exit(1)
else:
    DUMP_CHAT_ID = int(DUMP_CHAT_ID)

FSUB_ID = os.environ.get('FSUB_ID', '')
if len(FSUB_ID) == 0:
    logging.error("FSUB_ID variable is missing! Exiting now")
    exit(1)
else:
    FSUB_ID = int(FSUB_ID)

USER_SESSION_STRING = os.environ.get('USER_SESSION_STRING', '')
if len(USER_SESSION_STRING) == 0:
    logging.info("USER_SESSION_STRING variable is missing! Bot will split Files in 2Gb...")
    USER_SESSION_STRING = None

OWNER_ID = os.environ.get('OWNER_ID', '0')
if len(OWNER_ID) == 0:
    OWNER_ID = '0'
else:
    OWNER_ID = int(OWNER_ID)

MONGO_URI = os.environ.get('MONGO_URI', '')
INDEX_CHAT_ID = os.environ.get('INDEX_CHAT_ID', '')

if MONGO_URI and INDEX_CHAT_ID:
    INDEX_CHAT_ID = int(INDEX_CHAT_ID)
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.get_database("terabox_bot")
    videos_col = db["videos"]
    videos_col.create_index("message_id", unique=True)
    premium_col = db["premium"]
    premium_col.create_index("user_id", unique=True)
    users_col = db["users"]
    users_col.create_index("user_id", unique=True)
    logger.info("MongoDB connected")
else:
    mongo_client = None
    db = None
    videos_col = None
    premium_col = None
    users_col = None
    INDEX_CHAT_ID = None

app = Client("jetbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user = None
SPLIT_SIZE = 2093796556
if USER_SESSION_STRING:
    user = Client("jetu", api_id=API_ID, api_hash=API_HASH, session_string=USER_SESSION_STRING)
    SPLIT_SIZE = 4241280205

USER_SESSION_INDEXING = os.environ.get('USER_SESSION_INDEXING', '')
if len(USER_SESSION_INDEXING) == 0:
    USER_SESSION_INDEXING = None

user_index = None

user_cooldowns = {}
COOLDOWN_SECONDS = 90

search_sessions = {}
SEARCH_PAGE_SIZE = 5
SEARCH_SESSION_TTL = 60

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DUMP_DONATION_IMAGE = os.path.join(BASE_DIR, "Pay-QR", "Donation.jpg")
DUMP_QR_FILES = {
    "binance": os.path.join(BASE_DIR, "Pay-QR", "Binance.jpg"),
    "upi": os.path.join(BASE_DIR, "Pay-QR", "upi.jpg")
}

DUMP_OFFER_CAPTION = (
    "💾 Permanent Dump Channel Access\n\n"
    "Buy permanent access to the whole dump channel.\n\n"
    "• Binance: 1.5 USDT only\n"
    "• UPI: ₹200 only\n\n"
    "Choose your payment method below. After paying, send the payment "
    "screenshot to @rtx5069 for verification."
)

DUMP_METHOD_LABELS = {
    "binance": "Binance • 1.5 USDT",
    "upi": "UPI • ₹200"
}

def build_dump_offer_media():
    return InputMediaPhoto(
        media=DUMP_DONATION_IMAGE,
        caption=DUMP_OFFER_CAPTION,
        parse_mode=None
    )

def build_dump_payment_keyboard(user_id):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            DUMP_METHOD_LABELS["binance"],
            callback_data=f"dump:binance:{user_id}"
        ),
        InlineKeyboardButton(
            DUMP_METHOD_LABELS["upi"],
            callback_data=f"dump:upi:{user_id}"
        )
    ]])

def build_dump_qr_keyboard(payment_method, user_id):
    other_method = "upi" if payment_method == "binance" else "binance"
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "← Back",
            callback_data=f"dump:back:{user_id}"
        ),
        InlineKeyboardButton(
            DUMP_METHOD_LABELS[other_method],
            callback_data=f"dump:{other_method}:{user_id}"
        )
    ]])

VALID_DOMAINS = [
    'terabox.com', 'nephobox.com', '4funbox.com', 'mirrobox.com', 
    'momerybox.com', 'teraboxapp.com', '1024tera.com', 
    'terabox.app', 'gibibox.com', 'goaibox.com', 'terasharelink.com', 
    'teraboxlink.com', 'terafileshare.com', 'teraboxshare.com'
]
last_update_time = 0

async def is_user_member(client, user_id):
    try:
        member = await client.get_chat_member(FSUB_ID, user_id)
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error checking membership status for user {user_id}: {e}")
        return False
    
def is_valid_url(url):
    parsed_url = urlparse(url)
    return any(parsed_url.netloc.endswith(domain) for domain in VALID_DOMAINS)

def format_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    else:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"

def parse_size(size_str):
    try:
        size_str = size_str.strip()
        if size_str.endswith('TB'):
            return float(size_str[:-2]) * 1024 * 1024 * 1024 * 1024
        elif size_str.endswith('GB'):
            return float(size_str[:-2]) * 1024 * 1024 * 1024
        elif size_str.endswith('MB'):
            return float(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('KB'):
            return float(size_str[:-2]) * 1024
        elif size_str.endswith('B'):
            return float(size_str[:-1])
        return float(size_str)
    except:
        return 0

def is_premium(user_id):
    if db is None:
        return False
    return premium_col.find_one({"user_id": user_id}) is not None

async def delayed_delete(msg, delay):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except:
        pass

def build_search_query(keywords):
    return {
        "$and": [
            {"file_name": {"$type": "string"}},
            *[
                {"file_name": {"$regex": re.escape(keyword), "$options": "i"}}
                for keyword in keywords
            ]
        ]
    }

def get_search_session(token):
    return search_sessions.get(token)

async def expire_search_session(token):
    while True:
        session = search_sessions.get(token)
        if not session:
            return

        remaining = SEARCH_SESSION_TTL - (time.time() - session["last_activity"])
        if remaining > 0:
            await asyncio.sleep(remaining)
            continue

        search_sessions.pop(token, None)
        try:
            await session["message"].delete()
        except Exception as e:
            logger.warning(f"Could not delete expired search results message: {e}")
        return

user_lang_cache = {}

def get_user_lang(user_id):
    if user_id in user_lang_cache:
        return user_lang_cache[user_id]
    code = "en"
    if users_col is not None:
        try:
            doc = users_col.find_one({"user_id": user_id}, {"language_code": 1})
            if doc and doc.get("language_code") in LANGUAGE_CODES:
                code = doc["language_code"]
        except Exception as e:
            logger.warning(f"Could not load language for user {user_id}: {e}")
    user_lang_cache[user_id] = code
    return code

def set_user_lang(user_id, code):
    if code not in LANGUAGE_CODES:
        return
    user_lang_cache[user_id] = code
    if users_col is not None:
        try:
            users_col.update_one(
                {"user_id": user_id},
                {"$set": {
                    "language_code": code,
                    "updated_at": datetime.now(timezone.utc)
                }},
                upsert=True
            )
        except Exception as e:
            logger.warning(f"Could not save language for user {user_id}: {e}")

def t(user_id, key, **kwargs):
    code = get_user_lang(user_id)
    template = TRANSLATIONS.get(code, {}).get(key)
    if template is None:
        template = TRANSLATIONS["en"].get(key, key)
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception as e:
            logger.warning(f"Translation format error for {key}: {e}")
            return template
    return template

settings_sessions = {}
SETTINGS_TTL = 300

def build_settings_menu_keyboard(token):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("Language/भाषा", callback_data=f"us:open:{token}")
    ]])

def build_language_grid_keyboard(token, selected):
    rows = []
    row = []
    for code, name in LANGUAGES:
        label = ("✅ " + name) if code == selected else name
        row.append(InlineKeyboardButton(
            label, callback_data=f"us:lang:{token}:{code}"
        ))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    if selected:
        confirm_label = (
            TRANSLATIONS.get(selected, {}).get("confirm")
            or TRANSLATIONS["en"]["confirm"]
        )
        rows.append([InlineKeyboardButton(
            confirm_label, callback_data=f"us:confirm:{token}"
        )])
    return InlineKeyboardMarkup(rows)

async def expire_settings_session(token):
    while True:
        session = settings_sessions.get(token)
        if not session:
            return

        remaining = SETTINGS_TTL - (time.time() - session["last_activity"])
        if remaining > 0:
            await asyncio.sleep(remaining)
            continue

        settings_sessions.pop(token, None)
        try:
            await session["message"].delete()
        except Exception as e:
            logger.warning(f"Could not delete expired settings message: {e}")
        return

def fetch_search_page(keywords, page):
    query = build_search_query(keywords)
    total = videos_col.count_documents(query)
    total_pages = max(1, math.ceil(total / SEARCH_PAGE_SIZE))
    page = min(max(page, 0), total_pages - 1)
    results = list(
        videos_col.find(
            query,
            {"message_id": 1, "file_name": 1, "chat_id": 1}
        )
        .sort([("file_name", 1), ("message_id", 1)])
        .skip(page * SEARCH_PAGE_SIZE)
        .limit(SEARCH_PAGE_SIZE)
    )
    return results, total, total_pages, page

def filename_button_text(file_name):
    if len(file_name) <= 64:
        return file_name
    return f"{file_name[:61]}..."

def build_search_keyboard(token, results, page, total_pages):
    rows = []
    for doc in results:
        file_name = doc.get("file_name") or f"File {doc['message_id']}"
        rows.append([
            InlineKeyboardButton(
                filename_button_text(file_name),
                callback_data=f"search:file:{token}:{doc['message_id']}"
            )
        ])

    previous_callback = (
        f"search:page:{token}:{page - 1}"
        if page > 0 else f"search:noop:{token}"
    )
    next_callback = (
        f"search:page:{token}:{page + 1}"
        if page < total_pages - 1 else f"search:noop:{token}"
    )
    rows.append([
        InlineKeyboardButton("←", callback_data=previous_callback),
        InlineKeyboardButton(
            f"{page + 1}/{total_pages}",
            callback_data=f"search:noop:{token}"
        ),
        InlineKeyboardButton("→", callback_data=next_callback)
    ])
    return InlineKeyboardMarkup(rows)

IST = timezone(timedelta(hours=5, minutes=30))

async def get_video_metadata(file_path):
    try:
        proc = await asyncio.create_subprocess_exec(
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration:stream=width,height',
            '-of', 'json',
            file_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        data = json.loads(stdout.decode())
        duration = int(float(data.get('format', {}).get('duration', 0)))
        streams = data.get('streams', [])
        width = 0
        height = 0
        for s in streams:
            if s.get('width') and s.get('height'):
                width = s['width']
                height = s['height']
                break
        return duration, width, height
    except Exception as e:
        logger.error(f"Metadata error: {e}")
        return 0, 0, 0

async def generate_thumbnail(file_path, duration=0):
    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) < 1024:
            logger.error(f"Thumbnail skipped: file missing or too small ({file_path})")
            return None
        thumb_path = f"{file_path}.jpg"
        ss_time = min(duration * 0.25, 30) if duration > 0 else 5
        proc = await asyncio.create_subprocess_exec(
            'xtra', '-y', '-ss', str(ss_time),
            '-i', file_path, '-vframes', '1',
            '-vf', 'scale=320:-1', '-q:v', '2',
            thumb_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            logger.error(f"Thumbnail ffmpeg error: {stderr.decode()}")
            return None
        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
            with open(thumb_path, 'rb') as f:
                thumb_bytes = f.read()
            os.remove(thumb_path)
            return io.BytesIO(thumb_bytes)
    except Exception as e:
        logger.error(f"Thumbnail error: {e}")
    return None

async def index_all_videos():
    if not user_index:
        logger.warning("Indexing user client not available, skipping index")
        return
    start = time.time()
    total = await user_index.search_messages_count(INDEX_CHAT_ID, filter=MessagesFilter.VIDEO)
    logger.info(f"Indexing started — {total} videos total to scan")

    indexed = 0
    for offset in range(0, total, 100):
        async for msg in user_index.search_messages(INDEX_CHAT_ID, filter=MessagesFilter.VIDEO, limit=100, offset=offset):
            try:
                videos_col.update_one(
                    {"message_id": msg.id},
                    {"$set": {
                        "message_id": msg.id,
                        "chat_id": INDEX_CHAT_ID,
                        "file_name": msg.video.file_name if msg.video and msg.video.file_name else None,
                        "file_size": msg.video.file_size if msg.video else 0,
                        "duration": msg.video.duration if msg.video else 0,
                        "date": msg.date
                    }},
                    upsert=True
                )
                indexed += 1
            except:
                pass

    elapsed = time.time() - start
    logger.info(f"Indexing finished — {indexed} videos indexed ({elapsed:.2f}s)")

async def index_new_videos():
    if not user_index:
        return
    last = videos_col.find_one(sort=[("message_id", -1)])
    last_id = last["message_id"] if last else 0

    start = time.time()
    count = 0
    async for msg in user_index.search_messages(INDEX_CHAT_ID, filter=MessagesFilter.VIDEO, limit=100):
        if msg.id <= last_id:
            break
        videos_col.update_one(
            {"message_id": msg.id},
            {"$set": {
                "message_id": msg.id,
                "chat_id": INDEX_CHAT_ID,
                "file_name": msg.video.file_name if msg.video and msg.video.file_name else None,
                "file_size": msg.video.file_size if msg.video else 0,
                "duration": msg.video.duration if msg.video else 0,
                "date": msg.date
            }},
            upsert=True
        )
        count += 1

    if count:
        elapsed = time.time() - start
        logger.info(f"Indexed {count} new videos ({elapsed:.2f}s)")

async def periodic_reindex():
    while True:
        await asyncio.sleep(86400)
        await index_new_videos()

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    join_button = InlineKeyboardButton("ᴊᴏɪɴ ❤️🚀", url="https://t.me/jetmirror")
    developer_button = InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ ⚡️", url="https://t.me/rtx5069")
    repo69 = InlineKeyboardButton("ʀᴇᴘᴏ 🌐", url="https://github.com/Hrishi2861/Terabox-Downloader-Bot")
    user_mention = message.from_user.mention
    reply_markup = InlineKeyboardMarkup([[join_button, developer_button], [repo69]])
    final_msg = t(message.from_user.id, "welcome", mention=user_mention)
    video_file_id = "/app/Jet-Mirror.mp4"
    if os.path.exists(video_file_id):
        await client.send_video(
            chat_id=message.chat.id,
            video=video_file_id,
            caption=final_msg,
            reply_markup=reply_markup
            )
    else:
        await message.reply_text(final_msg, reply_markup=reply_markup)

@app.on_message(filters.command("dump"))
async def dump_access(client: Client, message: Message):
    if not message.from_user:
        return

    if not os.path.exists(DUMP_DONATION_IMAGE):
        logger.error(f"Donation image not found: {DUMP_DONATION_IMAGE}")
        await message.reply_text(
            t(message.from_user.id, "dump_unavailable")
        )
        return

    caption = t(message.from_user.id, "dump_caption")
    await client.send_photo(
        message.chat.id,
        DUMP_DONATION_IMAGE,
        caption=caption,
        reply_markup=build_dump_payment_keyboard(message.from_user.id),
        parse_mode=None,
        reply_to_message_id=message.id
    )

@app.on_callback_query(filters.regex(r"^dump:"))
async def dump_payment_callback(client: Client, callback_query):
    parts = callback_query.data.split(":")
    if len(parts) != 3 or (parts[1] not in DUMP_QR_FILES and parts[1] != "back"):
        await callback_query.answer("Invalid payment method.", show_alert=True)
        return

    try:
        requesting_user_id = int(parts[2])
    except ValueError:
        await callback_query.answer("Invalid payment request.", show_alert=True)
        return

    if callback_query.from_user.id != requesting_user_id:
        await callback_query.answer(
            "These payment buttons belong to another user.",
            show_alert=True
        )
        return

    payment_method = parts[1]

    if payment_method == "back":
        if not os.path.exists(DUMP_DONATION_IMAGE):
            logger.error(f"Donation image not found: {DUMP_DONATION_IMAGE}")
            await callback_query.answer(
                t(requesting_user_id, "dump_menu_unavailable"),
                show_alert=True
            )
            return
        await callback_query.answer()
        try:
            await callback_query.message.edit_media(
                build_dump_offer_media(),
                reply_markup=build_dump_payment_keyboard(requesting_user_id)
            )
        except Exception as e:
            logger.error(f"Could not restore dump payment menu: {e}")
        return

    qr_path = DUMP_QR_FILES[payment_method]
    if not os.path.exists(qr_path):
        logger.error(f"Payment QR not found: {qr_path}")
        await callback_query.answer(
            "Payment QR is temporarily unavailable.",
            show_alert=True
        )
        return

    if payment_method == "binance":
        caption = t(requesting_user_id, "dump_qr_binance")
    else:
        caption = t(requesting_user_id, "dump_qr_upi")

    await callback_query.answer("Opening payment QR...")
    try:
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media=qr_path,
                caption=caption,
                parse_mode=None
            ),
            reply_markup=build_dump_qr_keyboard(
                payment_method, requesting_user_id
            )
        )
    except Exception as e:
        logger.error(f"Could not display {payment_method} QR: {e}")
        try:
            await callback_query.message.edit_text(
                t(requesting_user_id, "dump_qr_error")
            )
        except Exception as edit_error:
            logger.error(f"Could not update failed payment message: {edit_error}")

@app.on_message(filters.command("user_settings"))
async def user_settings_cmd(client: Client, message: Message):
    if not message.from_user:
        return
    uid = message.from_user.id

    token = secrets.token_urlsafe(6)
    while token in settings_sessions:
        token = secrets.token_urlsafe(6)
    settings_sessions[token] = {
        "user_id": uid,
        "selected": get_user_lang(uid),
        "message": None,
        "last_activity": time.time()
    }

    settings_message = await message.reply_text(
        t(uid, "settings_title"),
        reply_markup=build_settings_menu_keyboard(token),
        parse_mode=None
    )
    settings_sessions[token]["message"] = settings_message
    asyncio.create_task(expire_settings_session(token))
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f"Could not delete user_settings command message: {e}")

@app.on_callback_query(filters.regex(r"^us:"))
async def user_settings_callback(client: Client, callback_query):
    parts = callback_query.data.split(":")
    if len(parts) < 3:
        await callback_query.answer("Invalid settings action.", show_alert=True)
        return

    action, token = parts[1], parts[2]
    session = settings_sessions.get(token)
    if not session:
        await callback_query.answer(
            "This settings menu has expired. Send /user_settings again.",
            show_alert=True
        )
        return

    if callback_query.from_user.id != session["user_id"]:
        await callback_query.answer(
            "This settings menu belongs to another user.",
            show_alert=True
        )
        return

    uid = session["user_id"]
    session["last_activity"] = time.time()

    if action == "open":
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(
                t(uid, "select_language"),
                reply_markup=build_language_grid_keyboard(
                    token, session["selected"]
                ),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not open language grid: {e}")
        return

    if action == "lang":
        code = parts[3] if len(parts) == 4 else ""
        if code not in LANGUAGE_CODES:
            await callback_query.answer("Invalid language.", show_alert=True)
            return
        session["selected"] = code
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(
                t(uid, "select_language"),
                reply_markup=build_language_grid_keyboard(token, code),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not update language selection: {e}")
        return

    if action == "confirm":
        code = session.get("selected") or "en"
        set_user_lang(uid, code)
        settings_sessions.pop(token, None)
        await callback_query.answer()
        language_name = dict(LANGUAGES).get(code, code)
        try:
            await callback_query.message.edit_text(
                t(uid, "language_saved", language=language_name),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not confirm language: {e}")
        return

    await callback_query.answer("Invalid settings action.", show_alert=True)

@app.on_message(filters.command("random"))
async def random_video(client: Client, message: Message):
    if videos_col is None:
        await message.reply_text(t(message.from_user.id, "mongo_missing"))
        return
    pipeline = [{"$sample": {"size": 1}}]
    result = list(videos_col.aggregate(pipeline))
    if not result:
        await message.reply_text(t(message.from_user.id, "no_videos"))
        return
    doc = result[0]
    user_msg = await client.copy_message(message.chat.id, doc["chat_id"], doc["message_id"], caption="")

    warn = await client.send_message(
        message.chat.id,
        t(message.from_user.id, "file_deleted_warning")
    )
    asyncio.create_task(delayed_delete(user_msg, 600))
    asyncio.create_task(delayed_delete(warn, 600))
    await message.delete()

@app.on_message(filters.command("search"))
async def search_files(client: Client, message: Message):
    if videos_col is None:
        await message.reply_text(t(message.from_user.id, "mongo_missing"))
        return

    keywords = [keyword.strip() for keyword in message.command[1:] if keyword.strip()]
    if not 1 <= len(keywords) <= 3:
        await message.reply_text(t(message.from_user.id, "search_usage"))
        return

    try:
        results, total, total_pages, page = await asyncio.to_thread(
            fetch_search_page, keywords, 0
        )
    except Exception as e:
        logger.error(f"Search failed for {keywords}: {e}")
        await message.reply_text(t(message.from_user.id, "search_unavailable"))
        return

    if total == 0:
        await message.reply_text(t(message.from_user.id, "search_no_results"))
        return

    token = secrets.token_urlsafe(6)
    while token in search_sessions:
        token = secrets.token_urlsafe(6)
    search_sessions[token] = {
        "user_id": message.from_user.id,
        "keywords": keywords,
        "last_activity": time.time(),
        "message": None
    }

    search_message = await message.reply_text(
        t(message.from_user.id, "search_header",
          keywords=" ".join(keywords), count=total),
        reply_markup=build_search_keyboard(token, results, page, total_pages),
        parse_mode=None
    )
    search_sessions[token]["message"] = search_message
    asyncio.create_task(expire_search_session(token))
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f"Could not delete search command message: {e}")

@app.on_callback_query(filters.regex(r"^search:"))
async def search_callback(client: Client, callback_query):
    parts = callback_query.data.split(":")
    if len(parts) < 3:
        await callback_query.answer("Invalid search action.", show_alert=True)
        return

    action = parts[1]
    token = parts[2]
    session = get_search_session(token)
    if not session:
        await callback_query.answer(
            t(callback_query.from_user.id, "search_expired"),
            show_alert=True
        )
        return

    if time.time() - session["last_activity"] >= SEARCH_SESSION_TTL:
        search_sessions.pop(token, None)
        await callback_query.answer(
            t(callback_query.from_user.id, "search_expired"),
            show_alert=True
        )
        try:
            await callback_query.message.delete()
        except Exception as e:
            logger.warning(f"Could not delete expired search results message: {e}")
        return

    if callback_query.from_user.id != session["user_id"]:
        await callback_query.answer(
            t(callback_query.from_user.id, "search_not_yours"),
            show_alert=True
        )
        return

    session["last_activity"] = time.time()

    if action == "noop":
        await callback_query.answer()
        return

    if action == "page":
        if len(parts) != 4:
            await callback_query.answer("Invalid page.", show_alert=True)
            return
        try:
            requested_page = int(parts[3])
            results, total, total_pages, page = await asyncio.to_thread(
                fetch_search_page, session["keywords"], requested_page
            )
        except Exception as e:
            logger.error(f"Search pagination failed: {e}")
            await callback_query.answer(
                "Could not load this page. Please try again.",
                show_alert=True
            )
            return

        if total == 0:
            search_sessions.pop(token, None)
            await callback_query.message.edit_text(
                t(session["user_id"], "search_none_left"),
                parse_mode=None
            )
            await callback_query.answer()
            return

        await callback_query.message.edit_text(
            t(session["user_id"], "search_header",
              keywords=" ".join(session["keywords"]), count=total),
            reply_markup=build_search_keyboard(
                token, results, page, total_pages
            ),
            parse_mode=None
        )
        await callback_query.answer()
        return

    if action == "file":
        if len(parts) != 4:
            await callback_query.answer("Invalid file.", show_alert=True)
            return
        try:
            message_id = int(parts[3])
        except ValueError:
            await callback_query.answer("Invalid file.", show_alert=True)
            return

        query = build_search_query(session["keywords"])
        query["$and"].append({"message_id": message_id})
        try:
            doc = await asyncio.to_thread(videos_col.find_one, query)
        except Exception as e:
            logger.error(f"Search file lookup failed: {e}")
            await callback_query.answer(
                "Could not find this file. Please try again.",
                show_alert=True
            )
            return

        if not doc:
            await callback_query.answer(
                t(callback_query.from_user.id, "search_file_unavailable"),
                show_alert=True
            )
            return

        await callback_query.answer(
            t(callback_query.from_user.id, "search_sending")
        )
        try:
            user_msg = await client.copy_message(
                callback_query.message.chat.id,
                doc["chat_id"],
                doc["message_id"],
                caption=""
            )
        except Exception as e:
            logger.error(f"Failed to send searched file {message_id}: {e}")
            await callback_query.message.reply_text(
                t(callback_query.from_user.id, "search_send_failed")
            )
            return

        asyncio.create_task(delayed_delete(user_msg, 600))
        try:
            warn = await client.send_message(
                callback_query.message.chat.id,
                t(callback_query.from_user.id, "file_deleted_warning")
            )
            asyncio.create_task(delayed_delete(warn, 600))
        except Exception as e:
            logger.warning(f"Could not send auto-delete warning: {e}")

        search_sessions.pop(token, None)
        try:
            await callback_query.message.delete()
        except Exception as e:
            logger.warning(f"Could not delete search results message: {e}")
        return

    await callback_query.answer("Invalid search action.", show_alert=True)

@app.on_message(filters.command("refresh"))
async def refresh_index(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return
    if videos_col is None:
        await message.reply_text("MongoDB not configured.")
        return
    if not user_index:
        await message.reply_text("Indexing user not available. Set USER_SESSION_INDEXING.")
        return
    await message.reply_text("Refreshing video index...")
    await index_all_videos()
    await message.reply_text("Index refreshed.")

@app.on_message(filters.command("add"))
async def add_premium(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return
    if db is None:
        await message.reply_text("MongoDB not configured.")
        return
    if len(message.command) < 2:
        await message.reply_text("Usage: /add user_id")
        return
    try:
        target_id = int(message.command[1])
    except:
        await message.reply_text("Invalid user ID.")
        return
    try:
        user = await client.get_users(target_id)
    except:
        await message.reply_text("User not found.")
        return
    if premium_col.find_one({"user_id": target_id}):
        await message.reply_text("User is already premium.")
        return
    premium_col.insert_one({"user_id": target_id, "added_by": OWNER_ID, "added_at": datetime.now(timezone.utc)})
    await message.reply_text(f"<a href='tg://user?id={target_id}'>{user.first_name}</a> added successfully ✅🚀")

@app.on_message(filters.command("remove"))
async def remove_premium(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return
    if db is None:
        await message.reply_text("MongoDB not configured.")
        return
    if len(message.command) < 2:
        await message.reply_text("Usage: /remove user_id")
        return
    try:
        target_id = int(message.command[1])
    except:
        await message.reply_text("Invalid user ID.")
        return
    try:
        user = await client.get_users(target_id)
        name = user.first_name
    except:
        name = str(target_id)
    result = premium_col.delete_one({"user_id": target_id})
    if result.deleted_count == 0:
        await message.reply_text("User is not in premium list.")
        return
    await message.reply_text(f"<a href='tg://user?id={target_id}'>{name}</a> deleted successfully ✅🚀")

@app.on_message(filters.command("list"))
async def list_premium(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return
    if db is None:
        await message.reply_text("MongoDB not configured.")
        return
    premium_users = list(premium_col.find())
    if not premium_users:
        await message.reply_text("No premium users.")
        return
    lines = ["**Premium Users:**\n"]
    for doc in premium_users:
        uid = doc["user_id"]
        date = doc.get("added_at", "")
        if isinstance(date, datetime):
            if date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)
            date = date.astimezone(IST).strftime("%Y-%m-%d %I:%M %p")
        try:
            u = await client.get_users(uid)
            name = u.first_name
        except:
            name = str(uid)
        lines.append(f"• <a href='tg://user?id={uid}'>{name}</a> (ID: tg://user?id={uid} ) - {date}")
    lines.append(f"\nTotal: {len(premium_users)} users")
    await message.reply_text("\n".join(lines))

async def update_status_message(status_message, text):
    try:
        await status_message.edit_text(text)
    except Exception as e:
        logger.error(f"Failed to update status message: {e}")

@app.on_message(filters.text)
async def handle_message(client: Client, message: Message):
    if message.text.startswith('/'):
        return
    if not message.from_user:
        return

    user_id = message.from_user.id

    if user_id == OWNER_ID:
        pass
    else:
        is_member = await is_user_member(client, user_id)
        if not is_member:
            join_button = InlineKeyboardButton("ᴊᴏɪɴ ❤️🚀", url="https://t.me/jetmirror")
            reply_markup = InlineKeyboardMarkup([[join_button]])
            await message.reply_text(
                t(user_id, "must_join"), reply_markup=reply_markup
            )
            return
    
    url = None
    for word in message.text.split():
        if is_valid_url(word):
            url = word
            break

    if not url:
        await message.reply_text(t(user_id, "invalid_link"))
        return

    if user_id != OWNER_ID and not is_premium(user_id):
        now = time.time()
        last_request = user_cooldowns.get(user_id, 0)
        if now - last_request < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - (now - last_request))
            reply = await message.reply_text(
                t(user_id, "cooldown", remaining=remaining)
            )
            await message.delete()
            asyncio.create_task(delayed_delete(reply, remaining))
            return
    encoded_url = urllib.parse.quote(url)

    status_message = await message.reply_text(t(user_id, "sending_media"))

    final_url = f"http://localhost:8000/download?url={encoded_url}"
    download = aria2.add_uris([final_url])

    start_time = datetime.now()
    stuck_start_time = None
    cancelled = False

    while not download.is_complete:
        await asyncio.sleep(15)
        download.update()
        progress = download.progress

        elapsed_time = datetime.now() - start_time
        elapsed_minutes, elapsed_seconds = divmod(elapsed_time.seconds, 60)

        if progress == 0 and download.completed_length == 0:
            if stuck_start_time is None:
                stuck_start_time = time.time()
            elif time.time() - stuck_start_time > 120:
                logger.info(f"Download stuck at 0% for over 120s, cancelling: {final_url}")
                aria2.remove([download])
                cancelled = True
                break
        else:
            stuck_start_time = None

        status_text = (
            f"┏ ғɪʟᴇɴᴀᴍᴇ: {download.name}\n"
            f"┠ [{'★' * int(progress / 10)}{'☆' * (10 - int(progress / 10))}] {progress:.2f}%\n"
            f"┠ ᴘʀᴏᴄᴇssᴇᴅ: {format_size(download.completed_length)} ᴏғ {format_size(download.total_length)}\n"
            f"┠ sᴛᴀᴛᴜs: 📥 Downloading\n"
            f"┠ ᴇɴɢɪɴᴇ: <b><u>Aria2c v1.37.0</u></b>\n"
            f"┠ sᴘᴇᴇᴅ: {format_size(download.download_speed)}/s\n"
            f"┠ ᴇᴛᴀ: {download.eta} | ᴇʟᴀᴘsᴇᴅ: {elapsed_minutes}m {elapsed_seconds}s\n"
            f"┖ ᴜsᴇʀ: <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a> | ɪᴅ: {user_id}\n"
            )
        while True:
            try:
                await update_status_message(status_message, status_text)
                break
            except FloodWait as e:
                logger.error(f"Flood wait detected! Sleeping for {e.value} seconds")
                await asyncio.sleep(e.value)

    if cancelled:
        try:
            await status_message.delete()
            await message.delete()
        except:
            pass
        await message.reply_text(t(user_id, "download_failed"))
        return

    file_path = download.files[0].path
    caption = (
        f"✨ {download.name}\n"
        f"👤 ʟᴇᴇᴄʜᴇᴅ ʙʏ : <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>\n"
        f"📥 ᴜsᴇʀ ʟɪɴᴋ: tg://user?id={user_id}\n\n"
        "[ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴊᴇᴛ-ᴍɪʀʀᴏʀ ❤️🚀](https://t.me/JetMirror)"
    )

    last_update_time = time.time()
    UPDATE_INTERVAL = 15

    async def update_status(message, text):
        nonlocal last_update_time
        current_time = time.time()
        if current_time - last_update_time >= UPDATE_INTERVAL:
            try:
                await message.edit_text(text)
                last_update_time = current_time
            except FloodWait as e:
                logger.warning(f"FloodWait: Sleeping for {e.value}s")
                await asyncio.sleep(e.value)
                await update_status(message, text)
            except Exception as e:
                logger.error(f"Error updating status: {e}")

    async def upload_progress(current, total):
        progress = (current / total) * 100
        elapsed_time = datetime.now() - start_time
        elapsed_minutes, elapsed_seconds = divmod(elapsed_time.seconds, 60)

        status_text = (
            f"┏ ғɪʟᴇɴᴀᴍᴇ: {download.name}\n"
            f"┠ [{'★' * int(progress / 10)}{'☆' * (10 - int(progress / 10))}] {progress:.2f}%\n"
            f"┠ ᴘʀᴏᴄᴇssᴇᴅ: {format_size(current)} ᴏғ {format_size(total)}\n"
            f"┠ sᴛᴀᴛᴜs: 📤 Uploading to Telegram\n"
            f"┠ ᴇɴɢɪɴᴇ: <b><u>PyroFork v2.2.11</u></b>\n"
            f"┠ sᴘᴇᴇᴅ: {format_size(current / elapsed_time.seconds if elapsed_time.seconds > 0 else 0)}/s\n"
            f"┠ ᴇʟᴀᴘsᴇᴅ: {elapsed_minutes}m {elapsed_seconds}s\n"
            f"┖ ᴜsᴇʀ: <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a> | ɪᴅ: {user_id}\n"
        )
        await update_status(status_message, status_text)

    async def split_video_with_ffmpeg(input_path, output_prefix, split_size):
        try:
            original_ext = os.path.splitext(input_path)[1].lower() or '.mp4'
            start_time = datetime.now()
            last_progress_update = time.time()
            
            proc = await asyncio.create_subprocess_exec(
                'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', input_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            total_duration = float(stdout.decode().strip())
            
            file_size = os.path.getsize(input_path)
            parts = math.ceil(file_size / split_size)
            
            if parts == 1:
                return [input_path]
            
            duration_per_part = total_duration / parts
            split_files = []
            
            for i in range(parts):
                current_time = time.time()
                if current_time - last_progress_update >= UPDATE_INTERVAL:
                    elapsed = datetime.now() - start_time
                    status_text = (
                        f"✂️ Splitting {os.path.basename(input_path)}\n"
                        f"Part {i+1}/{parts}\n"
                        f"Elapsed: {elapsed.seconds // 60}m {elapsed.seconds % 60}s"
                    )
                    await update_status(status_message, status_text)
                    last_progress_update = current_time
                
                output_path = f"{output_prefix}.{i+1:03d}{original_ext}"
                cmd = [
                    'xtra', '-y', '-ss', str(i * duration_per_part),
                    '-i', input_path, '-t', str(duration_per_part),
                    '-c', 'copy', '-map', '0',
                    '-avoid_negative_ts', 'make_zero',
                    output_path
                ]
                
                proc = await asyncio.create_subprocess_exec(*cmd)
                await proc.wait()
                split_files.append(output_path)
            
            return split_files
        except Exception as e:
            logger.error(f"Split error: {e}")
            raise

    def build_video_kwargs(caption, duration, width, height, thumb, progress_func):
        kwargs = dict(caption=caption, progress=progress_func)
        if duration:
            kwargs['duration'] = duration
        if width and height:
            kwargs['width'] = width
            kwargs['height'] = height
        if thumb:
            kwargs['thumb'] = thumb
        return kwargs

    async def handle_upload():
        file_size = os.path.getsize(file_path)
        thumb_bytes = None
        user_msgs = []
        
        if file_size > SPLIT_SIZE:
            await update_status(
                status_message,
                f"✂️ Splitting {download.name} ({format_size(file_size)})"
            )
            
            split_files = await split_video_with_ffmpeg(
                file_path,
                os.path.splitext(file_path)[0],
                SPLIT_SIZE
            )
            
            try:
                for i, part in enumerate(split_files):
                    part_caption = f"{caption}\n\nPart {i+1}/{len(split_files)}"
                    await update_status(
                        status_message,
                        f"📤 Uploading part {i+1}/{len(split_files)}\n"
                        f"{os.path.basename(part)}"
                    )
                    
                    part_duration, part_width, part_height = await get_video_metadata(part)
                    part_thumb = await generate_thumbnail(part, part_duration)
                    vkwargs = build_video_kwargs(part_caption, part_duration, part_width, part_height, part_thumb, upload_progress)
                    
                    if USER_SESSION_STRING:
                        sent = await user.send_video(DUMP_CHAT_ID, part, **vkwargs)
                    else:
                        sent = await client.send_video(DUMP_CHAT_ID, part, **vkwargs)
                    user_msg = await client.copy_message(message.chat.id, DUMP_CHAT_ID, sent.id)
                    if user_msg:
                        user_msgs.append(user_msg)
                    os.remove(part)
                    if part_thumb:
                        part_thumb = None
            finally:
                for part in split_files:
                    try: os.remove(part)
                    except: pass
        else:
            await update_status(
                status_message,
                f"📤 Uploading {download.name}\n"
                f"Size: {format_size(file_size)}"
            )
            
            duration, width, height = await get_video_metadata(file_path)
            thumb_bytes = await generate_thumbnail(file_path, duration)
            vkwargs = build_video_kwargs(caption, duration, width, height, thumb_bytes, upload_progress)
            
            if USER_SESSION_STRING:
                sent = await user.send_video(DUMP_CHAT_ID, file_path, **vkwargs)
            else:
                sent = await client.send_video(DUMP_CHAT_ID, file_path, **vkwargs)
            user_msg = await client.copy_message(message.chat.id, DUMP_CHAT_ID, sent.id)
            if user_msg:
                user_msgs.append(user_msg)
        
        for msg in user_msgs:
            asyncio.create_task(delayed_delete(msg, 600))
        warn = await client.send_message(
            message.chat.id,
            t(user_id, "file_deleted_warning")
        )
        asyncio.create_task(delayed_delete(warn, 600))

        if os.path.exists(file_path):
            os.remove(file_path)
        if thumb_bytes:
            thumb_bytes = None

    start_time = datetime.now()
    await handle_upload()

    try:
        await status_message.delete()
        await message.delete()
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return render_template("index.html")

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

def keep_alive():
    Thread(target=run_flask).start()

async def start_user_client():
    if user:
        await user.start()
        logger.info("User client started.")

def run_user():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_user_client())

async def start_indexing():
    if USER_SESSION_INDEXING:
        global user_index
        user_index = Client("jetidx", api_id=API_ID, api_hash=API_HASH, session_string=USER_SESSION_INDEXING)
        await user_index.start()
        logger.info("Indexing user client started.")

        if videos_col is not None:
            if videos_col.estimated_document_count() == 0:
                asyncio.create_task(index_all_videos())
            else:
                asyncio.create_task(index_new_videos())
            asyncio.create_task(periodic_reindex())

if __name__ == "__main__":
    keep_alive()

    if user:
        logger.info("Starting user client...")
        Thread(target=run_user).start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_indexing())

    logger.info("Bot client started!")
    app.run()
