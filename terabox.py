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
import glob
import shutil
from html import escape
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
    "max-concurrent-downloads": "8",
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

DOWNLOAD_API = os.environ.get('DOWNLOAD_API', '')
if len(DOWNLOAD_API) == 0:
    logging.error("DOWNLOAD_API variable is missing! Exiting now")
    exit(1)
DOWNLOAD_API = DOWNLOAD_API.rstrip('/')

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

# Telegram can temporarily rate-limit rapid folder uploads. Keep media sends
# sequential across jobs, leave a short gap between them, and retry the same
# operation for the full duration requested by Telegram instead of counting
# that file as failed.
TELEGRAM_MEDIA_DELAY = float(os.environ.get("TELEGRAM_MEDIA_DELAY", "1.0"))
telegram_media_lock = asyncio.Lock()
telegram_last_media_send = 0.0


async def telegram_call_with_flood_retry(operation, description, paced=False):
    """Run a Telegram API operation, honoring every FloodWait before retrying."""
    global telegram_last_media_send

    async def run():
        global telegram_last_media_send
        if paced:
            elapsed = time.monotonic() - telegram_last_media_send
            delay = TELEGRAM_MEDIA_DELAY - elapsed
            if delay > 0:
                await asyncio.sleep(delay)

        while True:
            try:
                result = await operation()
                if paced:
                    telegram_last_media_send = time.monotonic()
                return result
            except FloodWait as e:
                wait_seconds = max(1, int(e.value)) + 1
                logger.warning(
                    f"Telegram FloodWait while {description}; "
                    f"waiting {wait_seconds}s before retrying the same operation"
                )
                await asyncio.sleep(wait_seconds)

    if paced:
        async with telegram_media_lock:
            return await run()
    return await run()

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
pending_inputs = {}
PENDING_TTL = 300
user_settings_cache = {}
DEFAULT_FOLDER_MODE = "single"


def folder_mode_label(uid, mode):
    return t(uid, "folder_zip" if mode == "zip" else "folder_single")

def get_user_setting(user_id, key, default=None):
    cache_key = (user_id, key)
    if cache_key in user_settings_cache:
        return user_settings_cache[cache_key]
    value = default
    if users_col is not None:
        try:
            doc = users_col.find_one({"user_id": user_id}, {key: 1})
            if doc and doc.get(key) is not None:
                value = doc[key]
        except Exception as e:
            logger.warning(f"Could not load {key} for user {user_id}: {e}")
    user_settings_cache[cache_key] = value
    return value

def set_user_setting(user_id, **values):
    for key, value in values.items():
        user_settings_cache[(user_id, key)] = value
    if users_col is not None:
        try:
            users_col.update_one(
                {"user_id": user_id},
                {"$set": {**values, "updated_at": datetime.now(timezone.utc)}},
                upsert=True
            )
        except Exception as e:
            logger.warning(f"Could not save settings for user {user_id}: {e}")

async def build_settings_status(client, uid):
    language_name = dict(LANGUAGES).get(get_user_lang(uid), "English")
    thumb_label = "✅" if get_user_setting(uid, "thumbnail_file_id") else "—"
    dest = get_user_setting(uid, "leech_destination")
    if dest:
        dest_label = str(dest)
        try:
            chat = await client.get_chat(int(dest))
            dest_label = chat.title or dest_label
        except Exception as e:
            logger.warning(f"Could not load destination chat title: {e}")
    else:
        dest_label = t(uid, "dest_default")
    folder_mode = get_user_setting(uid, "folder_mode", DEFAULT_FOLDER_MODE)
    folder_label = folder_mode_label(uid, folder_mode)
    return (
        t(uid, "settings_status",
          language=language_name, thumb=thumb_label, dest=dest_label)
        + "\n" + t(uid, "folder_current", mode=folder_label)
    )

def build_settings_menu_keyboard(token):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Language/भाषा", callback_data=f"us:open:{token}")],
        [InlineKeyboardButton("🖼️ Thumbnail", callback_data=f"us:thumb:{token}")],
        [InlineKeyboardButton("📥 Leech Destination", callback_data=f"us:dest:{token}")],
        [InlineKeyboardButton("📁 Folder Settings", callback_data=f"us:folder:{token}")],
        [InlineKeyboardButton("❌ Close", callback_data=f"us:close:{token}")],
    ])

def build_folder_submenu_keyboard(token, mode, uid):
    zip_label = ("✅ " if mode == "zip" else "") + t(uid, "folder_zip")
    single_label = ("✅ " if mode == "single" else "") + t(uid, "folder_single")
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(zip_label, callback_data=f"us:folderset:{token}:zip"),
            InlineKeyboardButton(single_label, callback_data=f"us:folderset:{token}:single"),
        ],
        [InlineKeyboardButton("← Back", callback_data=f"us:back:{token}")],
    ])

def build_thumb_submenu_keyboard(token, has_thumb=False):
    rows = []
    if has_thumb:
        rows.append([
            InlineKeyboardButton("🖼️ Set", callback_data=f"us:thumbset:{token}"),
            InlineKeyboardButton("🗑️ Remove", callback_data=f"us:thumbdel:{token}")
        ])
    else:
        rows.append([
            InlineKeyboardButton("🖼️ Set", callback_data=f"us:thumbset:{token}")
        ])
    rows.append([InlineKeyboardButton("← Back", callback_data=f"us:back:{token}")])
    return InlineKeyboardMarkup(rows)

def build_dest_submenu_keyboard(token, has_dest=False):
    rows = []
    if has_dest:
        rows.append([
            InlineKeyboardButton("📥 Set", callback_data=f"us:destset:{token}"),
            InlineKeyboardButton("🗑️ Remove", callback_data=f"us:destdel:{token}")
        ])
    else:
        rows.append([
            InlineKeyboardButton("📥 Set", callback_data=f"us:destset:{token}")
        ])
    rows.append([InlineKeyboardButton("← Back", callback_data=f"us:back:{token}")])
    return InlineKeyboardMarkup(rows)

def build_settings_back_keyboard(token):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("← Back", callback_data=f"us:back:{token}")],
    ])

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
    rows.append([InlineKeyboardButton(
        "← Back", callback_data=f"us:back:{token}"
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
    uid = message.from_user.id
    join_button = InlineKeyboardButton(
        t(uid, "btn_join"), url="https://t.me/jetmirror"
    )
    developer_button = InlineKeyboardButton(
        t(uid, "btn_developer"), url="https://t.me/rtx5069"
    )
    repo69 = InlineKeyboardButton(
        t(uid, "btn_repo"),
        url="https://github.com/Hrishi2861/Terabox-Downloader-Bot"
    )
    user_mention = message.from_user.mention
    reply_markup = InlineKeyboardMarkup([[join_button, developer_button], [repo69]])
    final_msg = (
        t(uid, "welcome", mention=user_mention)
        + "\n\n"
        + t(uid, "welcome_settings")
    )
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
        "cmd_message": message,
        "last_activity": time.time()
    }

    status_text = await build_settings_status(client, uid)
    settings_message = await message.reply_text(
        status_text,
        reply_markup=build_settings_menu_keyboard(token),
        parse_mode=None
    )
    settings_sessions[token]["message"] = settings_message
    asyncio.create_task(expire_settings_session(token))

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

    if action == "close":
        pending = pending_inputs.get(uid)
        if pending and pending.get("token") == token:
            pending_inputs.pop(uid, None)
        settings_sessions.pop(token, None)
        await callback_query.answer()
        try:
            await callback_query.message.delete()
        except Exception as e:
            logger.warning(f"Could not delete settings menu message: {e}")
        cmd_message = session.get("cmd_message")
        if cmd_message is not None:
            try:
                await cmd_message.delete()
            except Exception as e:
                logger.warning(f"Could not delete /user_settings command message: {e}")
        return

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
        await callback_query.answer()
        language_name = dict(LANGUAGES).get(code, code)
        try:
            await callback_query.message.edit_text(
                t(uid, "language_saved", language=language_name),
                reply_markup=build_settings_back_keyboard(token),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not confirm language: {e}")
        return

    if action == "back":
        pending = pending_inputs.get(uid)
        if pending and pending.get("token") == token:
            pending_inputs.pop(uid, None)
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(
                await build_settings_status(client, uid),
                reply_markup=build_settings_menu_keyboard(token),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not return to settings menu: {e}")
        return

    if action == "thumb":
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(
                await build_settings_status(client, uid),
                reply_markup=build_thumb_submenu_keyboard(
                    token, bool(get_user_setting(uid, "thumbnail_file_id"))
                ),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not open thumbnail sub-menu: {e}")
        return

    if action == "thumbset":
        pending_inputs[uid] = {
            "type": "thumb",
            "token": token,
            "expires": time.time() + PENDING_TTL
        }
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(
                t(uid, "thumb_set_prompt"),
                reply_markup=build_settings_back_keyboard(token),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not show thumbnail prompt: {e}")
        return

    if action == "thumbdel":
        set_user_setting(uid, thumbnail_file_id=None)
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(
                t(uid, "thumb_removed"),
                reply_markup=build_settings_back_keyboard(token),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not remove thumbnail: {e}")
        return

    if action == "dest":
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(
                await build_settings_status(client, uid),
                reply_markup=build_dest_submenu_keyboard(
                    token, bool(get_user_setting(uid, "leech_destination"))
                ),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not open destination sub-menu: {e}")
        return

    if action == "destset":
        pending_inputs[uid] = {
            "type": "dest",
            "token": token,
            "expires": time.time() + PENDING_TTL
        }
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(
                t(uid, "dest_set_prompt"),
                reply_markup=build_settings_back_keyboard(token),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not show destination prompt: {e}")
        return

    if action == "destdel":
        set_user_setting(uid, leech_destination=None, leech_destination_title=None)
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(
                t(uid, "dest_removed"),
                reply_markup=build_settings_back_keyboard(token),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not remove destination: {e}")
        return

    if action == "folder":
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(
                t(uid, "folder_settings"),
                reply_markup=build_folder_submenu_keyboard(
                    token,
                    get_user_setting(uid, "folder_mode", DEFAULT_FOLDER_MODE),
                    uid,
                ),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not open folder sub-menu: {e}")
        return

    if action == "folderset":
        mode = parts[3] if len(parts) == 4 else ""
        if mode not in ("zip", "single"):
            await callback_query.answer("Invalid folder mode.", show_alert=True)
            return
        set_user_setting(uid, folder_mode=mode)
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(
                t(uid, "folder_saved", mode=folder_mode_label(uid, mode)),
                reply_markup=build_settings_back_keyboard(token),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not save folder mode: {e}")
        return

    await callback_query.answer("Invalid settings action.", show_alert=True)

DEST_ID_PATTERN = re.compile(r'^-100\d{6,}$')

ADMIN_STATUSES = (
    ChatMemberStatus.OWNER,
    ChatMemberStatus.ADMINISTRATOR,
)

MEMBER_STATUSES = (
    ChatMemberStatus.OWNER,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.MEMBER,
)

def is_destination_admin(member):
    status = getattr(member, "status", None)
    if status in ADMIN_STATUSES:
        return True
    # Fallback for builds where the enum values differ by string.
    return str(getattr(status, "value", status)).lower() in ("admin", "administrator", "owner", "creator")

def is_destination_member(member):
    status = getattr(member, "status", None)
    if status in MEMBER_STATUSES:
        return True
    return str(getattr(status, "value", status)).lower() in ("member", "admin", "administrator", "owner", "creator")

async def can_bot_post_to_chat(client, dest_id):
    try:
        test = await client.send_message(dest_id, "✅ Destination check")
        try:
            await test.delete()
        except Exception:
            pass
        return True
    except Exception as e:
        logger.error(
            f"Destination {dest_id}: post test failed: "
            f"{type(e).__name__}: {e}"
        )
        return False

async def validate_leech_destination(client, uid, raw_text):
    text = raw_text.strip()
    if not DEST_ID_PATTERN.match(text):
        return None, t(uid, "dest_invalid")
    dest_id = int(text)

    bot_id = client.me.id if getattr(client, "me", None) else None
    if bot_id is None:
        try:
            bot_id = (await client.get_me()).id
        except Exception:
            bot_id = "me"

    try:
        chat = await client.get_chat(dest_id)
    except Exception as e:
        logger.error(
            f"Destination {dest_id}: bot cannot access chat "
            f"(bot id {bot_id}): {type(e).__name__}: {e}"
        )
        return None, t(uid, "dest_no_access")

    bot_can_post = False
    try:
        bot_member = await client.get_chat_member(dest_id, bot_id)
        if is_destination_admin(bot_member):
            bot_can_post = True
        elif is_destination_member(bot_member):
            bot_can_post = await can_bot_post_to_chat(client, dest_id)
        logger.info(
            f"Destination {dest_id}: bot status "
            f"{getattr(bot_member, 'status', None)} → can post: {bot_can_post}"
        )
    except Exception as e:
        logger.error(
            f"Destination {dest_id}: bot membership check failed "
            f"(bot id {bot_id}): {type(e).__name__}: {e}"
        )
        bot_can_post = await can_bot_post_to_chat(client, dest_id)

    if not bot_can_post:
        return None, t(uid, "dest_no_access")

    try:
        user_member = await client.get_chat_member(dest_id, uid)
    except Exception as e:
        logger.error(
            f"Destination {dest_id}: user membership check failed "
            f"(user id {uid}): {type(e).__name__}: {e}"
        )
        return None, t(uid, "dest_not_admin")

    user_is_admin = is_destination_admin(user_member)
    logger.info(
        f"Destination {dest_id}: user {uid} status "
        f"{getattr(user_member, 'status', None)} → admin: {user_is_admin}"
    )
    if not user_is_admin:
        return None, t(uid, "dest_not_admin")

    return chat, None

async def handle_pending_input(client, message, pending):
    uid = message.from_user.id
    token = pending.get("token")
    session = settings_sessions.get(token)

    if pending["type"] == "thumb":
        os.makedirs("downloads", exist_ok=True)
        original_path = None
        thumb_path = f"downloads/{uid}_thumb_norm.jpg"
        try:
            original_path = await message.download(
                file_name=f"downloads/{uid}_thumb_orig"
            )
            proc = await asyncio.create_subprocess_exec(
                'xtra', '-y', '-i', original_path,
                '-vf', 'scale=320:-1', '-q:v', '2',
                thumb_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await proc.communicate()
            if proc.returncode != 0 or not os.path.exists(thumb_path):
                logger.error(f"Thumbnail normalize error: {stderr.decode()}")
                source = original_path
            else:
                source = thumb_path
            sent = await client.send_photo(DUMP_CHAT_ID, source)
            thumb_file_id = sent.photo.file_id
            try:
                await sent.delete()
            except Exception as e:
                logger.warning(f"Could not delete temporary thumbnail copy: {e}")
            set_user_setting(uid, thumbnail_file_id=thumb_file_id)
            pending_inputs.pop(uid, None)
            await message.reply_text(t(uid, "thumb_set_done"))
            try:
                await message.delete()
            except Exception as e:
                logger.warning(f"Could not delete thumbnail photo message: {e}")
            if session:
                session["last_activity"] = time.time()
                try:
                    await session["message"].edit_text(
                        await build_settings_status(client, uid),
                        reply_markup=build_settings_menu_keyboard(token),
                        parse_mode=None
                    )
                except Exception as e:
                    logger.warning(f"Could not refresh settings menu: {e}")
        except Exception as e:
            logger.error(f"Could not set custom thumbnail: {e}")
            await message.reply_text(t(uid, "thumb_invalid"))
        finally:
            for path in (original_path, thumb_path):
                try:
                    if path and os.path.exists(path):
                        os.remove(path)
                except Exception:
                    pass
        return

    if pending["type"] == "dest":
        chat, error = await validate_leech_destination(client, uid, message.text)
        if error:
            await message.reply_text(error)
            return
        if isinstance(chat, int):
            dest_id, dest_title = chat, str(chat)
        else:
            dest_id = chat.id
            dest_title = chat.title or str(chat.id)
        set_user_setting(uid, leech_destination=dest_id,
                         leech_destination_title=dest_title)
        pending_inputs.pop(uid, None)
        confirm = await message.reply_text(t(uid, "dest_set_done", title=dest_title))
        asyncio.create_task(delayed_delete(confirm, 600))
        if session:
            session["last_activity"] = time.time()
            try:
                await session["message"].edit_text(
                    await build_settings_status(client, uid),
                    reply_markup=build_settings_menu_keyboard(token),
                    parse_mode=None
                )
            except Exception as e:
                logger.warning(f"Could not refresh settings menu: {e}")
        return

@app.on_message(filters.photo)
async def custom_thumbnail_photo(client: Client, message: Message):
    if not message.from_user:
        return
    uid = message.from_user.id
    pending = pending_inputs.get(uid)
    if not pending or pending.get("type") != "thumb":
        return
    if time.time() > pending.get("expires", 0):
        pending_inputs.pop(uid, None)
        return
    await handle_pending_input(client, message, pending)

@app.on_message(filters.command("cancel"))
async def cancel_pending_input(client: Client, message: Message):
    if not message.from_user:
        return
    uid = message.from_user.id
    pending = pending_inputs.pop(uid, None)
    if not pending:
        return
    token = pending.get("token")
    session = settings_sessions.get(token)
    if session:
        try:
            await session["message"].edit_text(
                await build_settings_status(client, uid),
                reply_markup=build_settings_menu_keyboard(token),
                parse_mode=None
            )
        except Exception as e:
            logger.warning(f"Could not restore settings menu after /cancel: {e}")
    await message.reply_text(t(uid, "cancel_pending"))

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

VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov", ".webm", ".ts", ".m4v",
    ".flv", ".wmv", ".mpg", ".mpeg", ".3gp", ".vob", ".m2ts", ".mts",
}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
PHOTO_MAX_SIZE = 10 * 1024 * 1024


def is_video_file(path):
    return os.path.splitext(path)[1].lower() in VIDEO_EXTENSIONS


def is_image_file(path):
    return os.path.splitext(path)[1].lower() in IMAGE_EXTENSIONS


def fetch_link_info(url):
    """Ask the download API whether a Terabox link is a file or a folder."""
    try:
        resp = requests.get(
            f"{DOWNLOAD_API}/api", params={"url": url}, timeout=300
        )
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, dict):
            return {"status": "error", "message": "Invalid response from download API."}
        return data
    except Exception as e:
        logger.error(f"Link preflight failed for {url}: {e}")
        return {"status": "error", "message": str(e)}


def safe_relative_parts(name, fallback="file"):
    raw = (name or "").replace("\\", "/")
    parts = []
    for part in raw.split("/"):
        part = part.strip()
        if not part or part in (".", ".."):
            continue
        part = re.sub(r'[\x00-\x1f<>:"|?*]', "_", part)
        parts.append(part)
    return parts or [fallback]


def unique_relative_path(used, name, index):
    parts = safe_relative_parts(name, fallback=f"file_{index}")
    rel = os.path.join(*parts)
    if rel in used:
        base, ext = os.path.splitext(rel)
        counter = index
        while rel in used:
            counter += 1
            rel = f"{base}_{counter}{ext}"
    used.add(rel)
    return rel


def truncate_filename(name, limit=180):
    if len(name) <= limit:
        return name
    base, ext = os.path.splitext(name)
    keep = max(1, limit - len(ext))
    return base[:keep] + ext


def make_status_updater(status_message, interval=15):
    state = {"last": 0.0}

    async def update(text):
        now = time.time()
        if now - state["last"] < interval:
            return
        state["last"] = now
        await update_status_message(status_message, text)

    async def force(text):
        state["last"] = time.time()
        await update_status_message(status_message, text)

    update.force = force
    return update


def build_caption(name, user_id, first_name, extra=None):
    head = f"✨ {escape(str(name))}\n"
    if extra:
        head += f"{escape(str(extra))}\n"
    return (
        head
        + f"👤 ʟᴇᴇᴄʜᴇᴅ ʙʏ : <a href='tg://user?id={user_id}'>{first_name}</a>\n"
        + f"📥 ᴜsᴇʀ ʟɪɴᴋ: tg://user?id={user_id}\n\n"
        + "[ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴊᴇᴛ-ᴍɪʀʀᴏʀ ❤️🚀](https://t.me/JetMirror)"
    )


async def fetch_custom_thumb(client, user_id):
    custom_thumb_id = get_user_setting(user_id, "thumbnail_file_id")
    if not custom_thumb_id:
        return None
    try:
        os.makedirs("downloads", exist_ok=True)
        return await client.download_media(
            custom_thumb_id,
            file_name=f"downloads/{user_id}_thumb_custom.jpg",
        )
    except Exception as e:
        logger.warning(f"Could not download custom thumbnail: {e}")
        return None


def add_aria2_download(url, out_dir=None, out_name=None):
    """Queue one download in aria2 and return its download object."""
    options = {}
    if out_dir:
        options["dir"] = os.path.abspath(out_dir)
    if out_name:
        options["out"] = out_name
    return aria2.add_uris([url], options=options or None)


async def wait_for_aria2(download, url="", poll_interval=5, stuck_timeout=120):
    """Wait for a queued aria2 download without blocking other downloads."""
    stuck_start = None
    while True:
        try:
            download.update()
        except Exception as e:
            logger.error(f"aria2 status check failed for {url}: {e}")
            return False
        if download.is_complete:
            return True

        status = str(getattr(download, "status", "")).lower()
        if status in ("error", "removed") or getattr(download, "has_failed", False):
            logger.error(
                f"aria2 reported failure for {url}: {getattr(download, 'error_message', '')}"
            )
            return False

        # Only flag a stall while aria2 is actually transferring this item;
        # queued (waiting) downloads legitimately report zero bytes.
        if (
            status == "active"
            and download.progress == 0
            and download.completed_length == 0
        ):
            if stuck_start is None:
                stuck_start = time.time()
            elif time.time() - stuck_start > stuck_timeout:
                logger.info(f"Download stuck at 0% for over {stuck_timeout}s, cancelling: {url}")
                try:
                    aria2.remove([download])
                except Exception:
                    pass
                return False
        else:
            stuck_start = None

        await asyncio.sleep(poll_interval)


def resolve_download_path(download, workdir):
    if not getattr(download, "files", None):
        return None
    path = download.files[0].path
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    if not os.path.exists(path):
        fallback = os.path.join(os.path.abspath(workdir), os.path.basename(path))
        if os.path.exists(fallback):
            path = fallback
    return path if os.path.exists(path) else None


async def download_with_aria2(url, status_message, user_id, first_name,
                              out_dir=None, out_name=None, label=None):
    try:
        download = add_aria2_download(url, out_dir=out_dir, out_name=out_name)
    except Exception as e:
        logger.error(f"aria2 could not add download: {e}")
        return None

    start_time = datetime.now()
    stuck_start_time = None
    cancelled = False
    display_name = escape(str(label or download.name))

    while not download.is_complete:
        await asyncio.sleep(15)
        download.update()
        progress = download.progress
        elapsed_time = datetime.now() - start_time
        elapsed_minutes, elapsed_seconds = divmod(elapsed_time.seconds, 60)

        status = str(getattr(download, "status", "")).lower()
        if status in ("error", "removed") or getattr(download, "has_failed", False):
            logger.error(
                f"aria2 reported failure for {url}: {getattr(download, 'error_message', '')}"
            )
            return None

        if progress == 0 and download.completed_length == 0:
            if stuck_start_time is None:
                stuck_start_time = time.time()
            elif time.time() - stuck_start_time > 120:
                logger.info(f"Download stuck at 0% for over 120s, cancelling: {url}")
                try:
                    aria2.remove([download])
                except Exception:
                    pass
                cancelled = True
                break
        else:
            stuck_start_time = None

        status_text = (
            f"┏ ғɪʟᴇɴᴀᴍᴇ: {display_name}\n"
            f"┠ [{'★' * int(progress / 10)}{'☆' * (10 - int(progress / 10))}] {progress:.2f}%\n"
            f"┠ ᴘʀᴏᴄᴇssᴇᴅ: {format_size(download.completed_length)} ᴏғ {format_size(download.total_length)}\n"
            f"┠ sᴛᴀᴛᴜs: 📥 Downloading\n"
            f"┠ ᴇɴɢɪɴᴇ: <b><u>Aria2c v1.37.0</u></b>\n"
            f"┠ sᴘᴇᴇᴅ: {format_size(download.download_speed)}/s\n"
            f"┠ ᴇᴛᴀ: {download.eta} | ᴇʟᴀᴘsᴇᴅ: {elapsed_minutes}m {elapsed_seconds}s\n"
            f"┖ ᴜsᴇʀ: <a href='tg://user?id={user_id}'>{first_name}</a> | ɪᴅ: {user_id}\n"
        )
        await update_status_message(status_message, status_text)

    if cancelled:
        return None
    if getattr(download, "has_failed", False):
        logger.error(
            f"aria2 reported failure for {url}: {getattr(download, 'error_message', '')}"
        )
        return None
    if not download.files:
        return None
    return download


def build_video_kwargs(caption, duration, width, height, thumb, progress_func):
    kwargs = dict(caption=caption, progress=progress_func)
    if duration:
        kwargs["duration"] = duration
    if width and height:
        kwargs["width"] = width
        kwargs["height"] = height
    if thumb:
        kwargs["thumb"] = thumb
    return kwargs


async def split_video_with_ffmpeg(input_path, output_prefix, split_size,
                                  status_message, update_status):
    try:
        original_ext = os.path.splitext(input_path)[1].lower() or ".mp4"
        proc = await asyncio.create_subprocess_exec(
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", input_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
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
            await update_status.force(
                f"✂️ Splitting {os.path.basename(input_path)}\nPart {i + 1}/{parts}"
            )
            output_path = f"{output_prefix}.{i + 1:03d}{original_ext}"
            cmd = [
                "xtra", "-y", "-ss", str(i * duration_per_part),
                "-i", input_path, "-t", str(duration_per_part),
                "-c", "copy", "-map", "0",
                "-avoid_negative_ts", "make_zero",
                output_path,
            ]
            proc = await asyncio.create_subprocess_exec(*cmd)
            await proc.wait()
            split_files.append(output_path)
        return split_files
    except Exception as e:
        logger.error(f"Split error: {e}")
        raise


def split_raw_file(path, part_size, chunk_size=8 * 1024 * 1024):
    base, ext = os.path.splitext(path)
    parts = []
    out = None
    written = 0
    try:
        with open(path, "rb") as src:
            while True:
                chunk = src.read(chunk_size)
                if not chunk:
                    break
                if out is None or written >= part_size:
                    if out:
                        out.close()
                    part_path = f"{base}.part{len(parts) + 1:03d}{ext}"
                    out = open(part_path, "wb")
                    parts.append(part_path)
                    written = 0
                out.write(chunk)
                written += len(chunk)
    finally:
        if out:
            out.close()
    return parts


async def upload_local_file(client, message, user_id, file_path, display_name,
                            caption, status_message, custom_thumb_path=None,
                            notify=True):
    start_time = datetime.now()
    update_status = make_status_updater(status_message)
    display_name = escape(str(display_name))
    file_size = os.path.getsize(file_path)
    user_msgs = []
    delivered_to_custom = False
    dest_copy_failed = False
    custom_dest = get_user_setting(user_id, "leech_destination")
    first_name = message.from_user.first_name or "User"

    async def upload_progress(current, total):
        progress = (current / total) * 100 if total else 0
        elapsed_time = datetime.now() - start_time
        elapsed_minutes, elapsed_seconds = divmod(elapsed_time.seconds, 60)
        await update_status(
            f"┏ ғɪʟᴇɴᴀᴍᴇ: {display_name}\n"
            f"┠ [{'★' * int(progress / 10)}{'☆' * (10 - int(progress / 10))}] {progress:.2f}%\n"
            f"┠ ᴘʀᴏᴄᴇssᴇᴅ: {format_size(current)} ᴏғ {format_size(total)}\n"
            f"┠ sᴛᴀᴛᴜs: 📤 Uploading to Telegram\n"
            f"┠ ᴇɴɢɪɴᴇ: <b><u>PyroFork v2.2.11</u></b>\n"
            f"┠ sᴘᴇᴇᴅ: {format_size(current / elapsed_time.seconds if elapsed_time.seconds > 0 else 0)}/s\n"
            f"┠ ᴇʟᴀᴘsᴇᴅ: {elapsed_minutes}m {elapsed_seconds}s\n"
            f"┖ ᴜsᴇʀ: <a href='tg://user?id={user_id}'>{first_name}</a> | ɪᴅ: {user_id}\n"
        )

    async def deliver(sent):
        nonlocal delivered_to_custom, dest_copy_failed
        if custom_dest:
            try:
                msg = await telegram_call_with_flood_retry(
                    lambda: client.copy_message(int(custom_dest), DUMP_CHAT_ID, sent.id),
                    f"copying {display_name} to the custom destination",
                    paced=True,
                )
                delivered_to_custom = True
                return msg
            except Exception as e:
                logger.error(f"Could not copy to custom destination {custom_dest}: {e}")
                msg = await telegram_call_with_flood_retry(
                    lambda: client.copy_message(message.chat.id, DUMP_CHAT_ID, sent.id),
                    f"copying {display_name} to the user chat",
                    paced=True,
                )
                dest_copy_failed = True
                return msg
        return await telegram_call_with_flood_retry(
            lambda: client.copy_message(message.chat.id, DUMP_CHAT_ID, sent.id),
            f"copying {display_name} to the user chat",
            paced=True,
        )

    async def send_video_file(path, part_caption):
        duration, width, height = await get_video_metadata(path)
        thumb = custom_thumb_path or await generate_thumbnail(path, duration)
        kwargs = build_video_kwargs(part_caption, duration, width, height, thumb, upload_progress)
        if USER_SESSION_STRING:
            return await telegram_call_with_flood_retry(
                lambda: user.send_video(DUMP_CHAT_ID, path, **kwargs),
                f"uploading video {display_name}",
                paced=True,
            )
        return await telegram_call_with_flood_retry(
            lambda: client.send_video(DUMP_CHAT_ID, path, **kwargs),
            f"uploading video {display_name}",
            paced=True,
        )

    async def send_document_file(path, part_caption):
        kwargs = dict(caption=part_caption, progress=upload_progress)
        if custom_thumb_path:
            kwargs["thumb"] = custom_thumb_path
        if USER_SESSION_STRING:
            return await telegram_call_with_flood_retry(
                lambda: user.send_document(DUMP_CHAT_ID, path, **kwargs),
                f"uploading document {display_name}",
                paced=True,
            )
        return await telegram_call_with_flood_retry(
            lambda: client.send_document(DUMP_CHAT_ID, path, **kwargs),
            f"uploading document {display_name}",
            paced=True,
        )

    async def send_photo_file(path, part_caption):
        kwargs = dict(caption=part_caption, progress=upload_progress)
        try:
            if USER_SESSION_STRING:
                return await telegram_call_with_flood_retry(
                    lambda: user.send_photo(DUMP_CHAT_ID, path, **kwargs),
                    f"uploading photo {display_name}",
                    paced=True,
                )
            return await telegram_call_with_flood_retry(
                lambda: client.send_photo(DUMP_CHAT_ID, path, **kwargs),
                f"uploading photo {display_name}",
                paced=True,
            )
        except Exception as e:
            logger.warning(f"Could not send {path} as photo, falling back to document: {e}")
            return await send_document_file(path, part_caption)

    if is_video_file(file_path) and file_size > SPLIT_SIZE:
        await update_status.force(f"✂️ Splitting {display_name} ({format_size(file_size)})")
        split_files = await split_video_with_ffmpeg(
            file_path, os.path.splitext(file_path)[0], SPLIT_SIZE,
            status_message, update_status,
        )
        try:
            for i, part in enumerate(split_files):
                part_caption = f"{caption}\n\nPart {i + 1}/{len(split_files)}"
                await update_status.force(
                    f"📤 Uploading part {i + 1}/{len(split_files)}\n{os.path.basename(part)}"
                )
                sent = await send_video_file(part, part_caption)
                msg = await deliver(sent)
                if msg:
                    user_msgs.append(msg)
                try:
                    os.remove(part)
                except Exception:
                    pass
        finally:
            for part in split_files:
                if part == file_path:
                    continue
                try:
                    os.remove(part)
                except Exception:
                    pass
    elif is_video_file(file_path):
        await update_status.force(f"📤 Uploading {display_name}\nSize: {format_size(file_size)}")
        sent = await send_video_file(file_path, caption)
        msg = await deliver(sent)
        if msg:
            user_msgs.append(msg)
    elif is_image_file(file_path) and file_size <= PHOTO_MAX_SIZE:
        await update_status.force(f"🖼️ Uploading {display_name}\nSize: {format_size(file_size)}")
        sent = await send_photo_file(file_path, caption)
        msg = await deliver(sent)
        if msg:
            user_msgs.append(msg)
    else:
        if file_size > SPLIT_SIZE:
            parts = split_raw_file(file_path, SPLIT_SIZE)
            try:
                for i, part in enumerate(parts):
                    part_caption = f"{caption}\n\nPart {i + 1}/{len(parts)}"
                    await update_status.force(
                        f"📤 Uploading part {i + 1}/{len(parts)}\n{os.path.basename(part)}"
                    )
                    sent = await send_document_file(part, part_caption)
                    msg = await deliver(sent)
                    if msg:
                        user_msgs.append(msg)
            finally:
                for part in parts:
                    try:
                        os.remove(part)
                    except Exception:
                        pass
        else:
            await update_status.force(f"📤 Uploading {display_name}\nSize: {format_size(file_size)}")
            sent = await send_document_file(file_path, caption)
            msg = await deliver(sent)
            if msg:
                user_msgs.append(msg)

    if notify:
        if delivered_to_custom:
            dest_title = str(custom_dest)
            try:
                dest_chat = await client.get_chat(int(custom_dest))
                dest_title = dest_chat.title or dest_title
            except Exception as e:
                logger.warning(f"Could not load destination chat title: {e}")
            delivered = await telegram_call_with_flood_retry(
                lambda: client.send_message(
                    message.chat.id,
                    t(user_id, "dest_delivered", title=dest_title),
                ),
                "sending the destination confirmation",
            )
            asyncio.create_task(delayed_delete(delivered, 600))
            if dest_copy_failed:
                await telegram_call_with_flood_retry(
                    lambda: client.send_message(message.chat.id, t(user_id, "dest_send_failed")),
                    "sending the destination failure note",
                )
        else:
            for msg in user_msgs:
                asyncio.create_task(delayed_delete(msg, 600))
            warn = await telegram_call_with_flood_retry(
                lambda: client.send_message(message.chat.id, t(user_id, "file_deleted_warning")),
                "sending the auto-delete notice",
            )
            asyncio.create_task(delayed_delete(warn, 600))

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass

    return {
        "user_msgs": user_msgs,
        "delivered_to_custom": delivered_to_custom,
        "dest_copy_failed": dest_copy_failed,
    }


async def process_single_url(client, message, user_id, download_url,
                             status_message, display_name=None,
                             caption_extra=None, custom_thumb_path=None,
                             own_thumb=True, notify=True,
                             out_dir=None, out_name=None):
    first_name = message.from_user.first_name or "User"
    download = await download_with_aria2(
        download_url, status_message, user_id, first_name,
        out_dir=out_dir, out_name=out_name, label=display_name
    )
    if download is None:
        return {
            "ok": False,
            "user_msgs": [],
            "delivered_to_custom": False,
            "dest_copy_failed": False,
        }
    if not download.files:
        logger.error(f"aria2 returned no files for {download_url}")
        return {
            "ok": False,
            "user_msgs": [],
            "delivered_to_custom": False,
            "dest_copy_failed": False,
        }

    file_path = download.files[0].path
    name = display_name or download.name
    caption = build_caption(name, user_id, first_name, caption_extra)

    thumb_path = custom_thumb_path
    if own_thumb and not thumb_path:
        thumb_path = await fetch_custom_thumb(client, user_id)

    try:
        result = await upload_local_file(
            client, message, user_id, file_path, name, caption,
            status_message, custom_thumb_path=thumb_path, notify=notify,
        )
    finally:
        if own_thumb and thumb_path and os.path.exists(thumb_path):
            try:
                os.remove(thumb_path)
            except Exception:
                pass

    result["ok"] = True
    return result


def _split_folder_files(info):
    downloadable = []
    skipped = 0
    for f in info.get("files") or []:
        if f.get("downloadable") and f.get("download_link"):
            downloadable.append(f)
        else:
            skipped += 1
    return downloadable, skipped


async def _finish_folder_notifications(client, message, user_id, user_msgs,
                                        delivered_to_custom, dest_copy_failed):
    custom_dest = get_user_setting(user_id, "leech_destination")
    if delivered_to_custom:
        dest_title = str(custom_dest)
        try:
            dest_chat = await client.get_chat(int(custom_dest))
            dest_title = dest_chat.title or dest_title
        except Exception as e:
            logger.warning(f"Could not load destination chat title: {e}")
        delivered = await telegram_call_with_flood_retry(
            lambda: client.send_message(
                message.chat.id, t(user_id, "dest_delivered", title=dest_title)
            ),
            "sending the destination confirmation",
        )
        asyncio.create_task(delayed_delete(delivered, 600))
        if dest_copy_failed:
            await telegram_call_with_flood_retry(
                lambda: client.send_message(message.chat.id, t(user_id, "dest_send_failed")),
                "sending the destination failure note",
            )
    elif user_msgs:
        for msg in user_msgs:
            asyncio.create_task(delayed_delete(msg, 600))
        warn = await telegram_call_with_flood_retry(
            lambda: client.send_message(message.chat.id, t(user_id, "file_deleted_warning")),
            "sending the auto-delete notice",
        )
        asyncio.create_task(delayed_delete(warn, 600))


async def process_folder_single(client, message, user_id, info, status_message):
    files, skipped = _split_folder_files(info)
    if not files:
        await message.reply_text(t(user_id, "folder_empty"))
        return

    total = len(files)
    first_name = message.from_user.first_name or "User"
    stamp = int(time.time())
    workdir = os.path.abspath(os.path.join("downloads", f"folder_{user_id}_{stamp}"))
    os.makedirs(workdir, exist_ok=True)
    thumb_path = await fetch_custom_thumb(client, user_id)
    sent = failed = 0
    user_msgs = []
    delivered = False
    dest_failed = False
    used_paths = set()
    tasks = []

    async def wait_entry(entry):
        ok = await wait_for_aria2(entry["download"], entry["rel"])
        return ok, entry

    try:
        # Queue every file at once so aria2 downloads them in parallel.
        for i, f in enumerate(files, 1):
            rel = unique_relative_path(used_paths, f.get("filename"), i)
            rel_caption = rel if len(rel) <= 200 else rel[:197] + "..."
            base_name = safe_relative_parts(rel, fallback=f"file_{i}")[-1]
            out_name = truncate_filename(f"folder_{user_id}_{stamp}_{i:04d}_{base_name}")
            try:
                download = add_aria2_download(
                    f"{DOWNLOAD_API}{f['download_link']}",
                    out_dir=workdir,
                    out_name=out_name,
                )
            except Exception as e:
                logger.exception(f"Could not queue folder file {i}/{total}: {e}")
                failed += 1
                continue
            entry = {
                "index": i,
                "rel": rel,
                "caption": rel_caption,
                "download": download,
            }
            tasks.append(asyncio.create_task(wait_entry(entry)))

        if not tasks:
            await message.reply_text(t(user_id, "download_failed"))
            return

        await update_status_message(
            status_message,
            f"📥 Downloading {len(tasks)} files in parallel",
        )

        # Upload each file as soon as its own download finishes.
        done = 0
        for future in asyncio.as_completed(tasks):
            try:
                ok, entry = await future
            except Exception as e:
                logger.exception(f"Folder download task failed: {e}")
                failed += 1
                continue
            done += 1
            if not ok:
                failed += 1
                continue

            path = resolve_download_path(entry["download"], workdir)
            if not path:
                logger.error(f"Downloaded file missing on disk: {entry['rel']}")
                failed += 1
                continue

            caption = build_caption(
                entry["caption"], user_id, first_name,
                f"📁 {entry['index']}/{total} • {entry['caption']}",
            )
            try:
                result = await upload_local_file(
                    client, message, user_id, path, entry["caption"], caption,
                    status_message, custom_thumb_path=thumb_path, notify=False,
                )
            except Exception as e:
                logger.exception(f"Folder upload failed for {entry['rel']}: {e}")
                failed += 1
                continue

            sent += 1
            user_msgs.extend(result.get("user_msgs") or [])
            delivered = delivered or result.get("delivered_to_custom", False)
            dest_failed = dest_failed or result.get("dest_copy_failed", False)
            await update_status_message(
                status_message,
                f"📥 Downloaded {done}/{len(tasks)} • 📤 Sent {sent}",
            )
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        if thumb_path and os.path.exists(thumb_path):
            try:
                os.remove(thumb_path)
            except Exception:
                pass
        shutil.rmtree(workdir, ignore_errors=True)

    await _finish_folder_notifications(
        client, message, user_id, user_msgs, delivered, dest_failed
    )
    summary = await telegram_call_with_flood_retry(
        lambda: client.send_message(
            message.chat.id,
            t(user_id, "folder_done", sent=sent, skipped=skipped, failed=failed),
        ),
        "sending the folder summary",
    )
    asyncio.create_task(delayed_delete(summary, 600))


async def process_folder_zip(client, message, user_id, info, status_message):
    files, skipped = _split_folder_files(info)
    if not files:
        await message.reply_text(t(user_id, "folder_empty"))
        return

    total = len(files)
    first_name = message.from_user.first_name or "User"
    stamp = int(time.time())
    workdir = os.path.abspath(os.path.join("downloads", f"folder_{user_id}_{stamp}"))
    os.makedirs(workdir, exist_ok=True)

    folder_name = info.get("filename") or "folder"
    safe_name = re.sub(r"[^\w\-. ]+", "_", folder_name).strip(" .") or "folder"
    safe_name = truncate_filename(safe_name, limit=100)
    archive_base = os.path.join(os.path.abspath("downloads"), f"{safe_name}_{user_id}_{stamp}")
    archive_path = archive_base + ".zip"
    downloaded = []
    total_bytes = 0
    failed = 0
    used_paths = set()
    parts = []
    user_msgs = []
    delivered = False
    dest_failed = False
    tasks = []

    async def wait_entry(entry):
        ok = await wait_for_aria2(entry["download"], entry["rel"])
        return ok, entry

    try:
        # Queue every file at once so aria2 downloads them in parallel.
        for i, f in enumerate(files, 1):
            rel = unique_relative_path(used_paths, f.get("filename"), i)
            rel = os.path.normpath(rel)
            rel_caption = rel if len(rel) <= 200 else rel[:197] + "..."
            flat_name = truncate_filename(f"{i:04d}_{os.path.basename(rel)}")
            try:
                download = add_aria2_download(
                    f"{DOWNLOAD_API}{f['download_link']}",
                    out_dir=workdir,
                    out_name=flat_name,
                )
            except Exception as e:
                logger.exception(f"Could not queue folder file {i}/{total}: {e}")
                failed += 1
                continue
            entry = {"rel": rel, "download": download}
            tasks.append(asyncio.create_task(wait_entry(entry)))

        if not tasks:
            await message.reply_text(t(user_id, "download_failed"))
            return

        await update_status_message(
            status_message,
            f"📥 Downloading {len(tasks)} files in parallel",
        )

        done = 0
        for future in asyncio.as_completed(tasks):
            try:
                ok, entry = await future
            except Exception as e:
                logger.exception(f"Folder download task failed: {e}")
                failed += 1
                continue
            done += 1
            if not ok:
                failed += 1
                continue

            src = resolve_download_path(entry["download"], workdir)
            if not src:
                logger.error(f"Downloaded file missing on disk: {entry['rel']}")
                failed += 1
                continue

            target = os.path.join(workdir, entry["rel"])
            os.makedirs(os.path.dirname(target), exist_ok=True)
            try:
                try:
                    os.replace(src, target)
                except Exception:
                    shutil.move(src, target)
            except Exception as e:
                logger.exception(f"Could not store folder file {entry['rel']}: {e}")
                failed += 1
                continue
            downloaded.append((target, entry["rel"]))
            total_bytes += os.path.getsize(target)
            await update_status_message(
                status_message,
                f"📥 Downloaded {done}/{len(tasks)}",
            )

        if not downloaded:
            await message.reply_text(t(user_id, "folder_empty"))
            return

        await update_status_message(
            status_message,
            f"🗜️ Creating archive\n{len(downloaded)} files • {format_size(total_bytes)}",
        )
        cmd = ["zip", "-r", "-q"]
        split = total_bytes > (SPLIT_SIZE - 50 * 1024 * 1024)
        if split:
            part_mb = max(1, int((SPLIT_SIZE - 50 * 1024 * 1024) // (1024 * 1024)))
            cmd += ["-s", f"{part_mb}m"]
        cmd += [archive_path, "."]
        proc = await asyncio.create_subprocess_exec(*cmd, cwd=workdir)
        await proc.wait()
        if proc.returncode != 0:
            logger.error(f"zip failed with code {proc.returncode}")
            await message.reply_text(t(user_id, "download_failed"))
            return

        parts = sorted(
            glob.glob(archive_base + ".*"),
            key=lambda p: (p.endswith(".zip"), p),
        )
        if not parts:
            await message.reply_text(t(user_id, "download_failed"))
            return

        caption_extra = f"🗜️ {len(downloaded)} files • {format_size(total_bytes)}"
        caption = build_caption(safe_name + ".zip", user_id, first_name, caption_extra)
        thumb_path = await fetch_custom_thumb(client, user_id)
        try:
            for i, part in enumerate(parts, 1):
                part_caption = caption
                if len(parts) > 1:
                    part_caption = f"{caption}\n\nPart {i}/{len(parts)}"
                await update_status_message(
                    status_message,
                    f"📤 Uploading archive {i}/{len(parts)}\n{os.path.basename(part)}",
                )
                result = await upload_local_file(
                    client, message, user_id, part,
                    os.path.basename(part), part_caption, status_message,
                    custom_thumb_path=thumb_path, notify=False,
                )
                user_msgs.extend(result.get("user_msgs") or [])
                delivered = delivered or result.get("delivered_to_custom", False)
                dest_failed = dest_failed or result.get("dest_copy_failed", False)
        finally:
            if thumb_path and os.path.exists(thumb_path):
                try:
                    os.remove(thumb_path)
                except Exception:
                    pass

        await _finish_folder_notifications(
            client, message, user_id, user_msgs, delivered, dest_failed
        )
        summary = await telegram_call_with_flood_retry(
            lambda: client.send_message(
                message.chat.id,
                t(user_id, "folder_done", sent=len(downloaded), skipped=skipped, failed=failed),
            ),
            "sending the folder summary",
        )
        asyncio.create_task(delayed_delete(summary, 600))
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        shutil.rmtree(workdir, ignore_errors=True)
        for part in parts:
            try:
                os.remove(part)
            except Exception:
                pass
        try:
            os.remove(archive_path)
        except Exception:
            pass


@app.on_message(filters.text)
async def handle_message(client: Client, message: Message):
    if message.text.startswith('/'):
        return
    if not message.from_user:
        return

    user_id = message.from_user.id

    pending = pending_inputs.get(user_id)
    if pending:
        if time.time() > pending.get("expires", 0):
            pending_inputs.pop(user_id, None)
        elif pending.get("type") == "dest":
            await handle_pending_input(client, message, pending)
            return

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

    status_message = await message.reply_text(t(user_id, "sending_media"))

    try:
        info = await asyncio.to_thread(fetch_link_info, url)
    except Exception as e:
        logger.error(f"Link preflight crashed: {e}")
        info = {"status": "error", "message": str(e)}

    if info.get("status") != "success":
        try:
            await status_message.delete()
        except Exception:
            pass
        reason = str(info.get("message") or t(user_id, "download_failed"))
        await message.reply_text(reason[:3500], parse_mode=None)
        return

    if info.get("isdir") is True:
        mode = get_user_setting(user_id, "folder_mode", DEFAULT_FOLDER_MODE)
        try:
            if mode == "zip":
                await process_folder_zip(client, message, user_id, info, status_message)
            else:
                await process_folder_single(client, message, user_id, info, status_message)
        except Exception as e:
            logger.exception(f"Folder processing failed: {e}")
            await message.reply_text(t(user_id, "download_failed"))
    else:
        try:
            result = await process_single_url(
                client, message, user_id,
                f"{DOWNLOAD_API}/download?url={urllib.parse.quote(url, safe='')}",
                status_message,
                display_name=info.get("filename") or None,
            )
        except Exception as e:
            logger.exception(f"Single-file processing failed: {e}")
            result = {"ok": False}
        if not result.get("ok"):
            await message.reply_text(t(user_id, "download_failed"))

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
