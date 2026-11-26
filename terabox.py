from aria2p import API as Aria2API, Client as Aria2Client
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import os
import logging
import math
from pyrogram import Client, filters, idle, StopPropagation
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import FloodWait
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
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
import subprocess
import zipfile
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

PREMIUM_INFO_RAW = os.environ.get('PREMIUM_INFO_ID', '').strip()
try:
    PREMIUM_INFO_ID = int(PREMIUM_INFO_RAW) if PREMIUM_INFO_RAW else None
except ValueError:
    PREMIUM_INFO_ID = None
    logging.error("PREMIUM_INFO_ID must be a numeric chat id such as -1001234567890; premium logs disabled")
if PREMIUM_INFO_ID is None and PREMIUM_INFO_RAW == '':
    logging.warning("PREMIUM_INFO_ID is not set; premium audit logging and log-chat commands are disabled")

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
    usage_col = db["usage_daily"]
    usage_col.create_index([("user_id", 1), ("date", 1)])
    users_col = db["users"]
    users_col.create_index("user_id", unique=True)
    logger.info("MongoDB connected")
else:
    mongo_client = None
    db = None
    videos_col = None
    premium_col = None
    usage_col = None
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

FREE_DAILY_TERABOX = 10
FREE_DAILY_RANDOM = 10
FREE_DAILY_SEARCH = 10
FREE_DAILY_FOLDERS = 1
FREE_FOLDER_MAX_FILES = 20
SUBSCRIPTION_DAYS = 30

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
    "💾 Permanent Dump Access — ₹250 / 2.75 USDT\n\n"
    "One payment unlocks:\n"
    "• Permanent access to the whole dump channel\n"
    "• Unlimited TeraBox downloads\n"
    "• Folder downloads\n"
    "• Unlimited /random and /search\n\n"
    "Choose your payment method below. After paying, send the payment "
    "screenshot to @rtx5069 for verification."
)

DUMP_METHOD_LABELS = {
    "binance": "Binance • 2.75 USDT",
    "upi": "UPI • ₹250"
}

MONTHLY_CAPTION = (
    "⭐ Jet Premium — 1 Month\n\n"
    "₹59 via UPI only\n\n"
    "For 30 days you get:\n"
    "• Unlimited TeraBox downloads\n"
    "• Folder downloads\n"
    "• Unlimited /random and /search\n\n"
    "This plan does not include the dump channel.\n"
    "After paying, send the payment screenshot to @rtx5069 for verification."
)

PLANS_CAPTION = (
    "⭐ Jet Premium Plans\n\n"
    "Free tier:\n"
    "• 10 TeraBox files per day\n"
    "• 10 /random uses per day\n"
    "• 10 /search uses per day\n"
    "• Folder downloads locked\n\n"
    "Unlock everything with either plan:\n\n"
    "💾 Permanent Dump Access — ₹250 / 2.75 USDT\n"
    "• Permanent dump channel access\n"
    "• Unlimited downloads, folders, /random and /search\n\n"
    "⭐ 1 Month Subscription — ₹59 UPI only\n"
    "• 30 days of unlimited downloads, folders, /random and /search\n"
    "• Does not include the dump channel\n\n"
    "Pick a plan below. After paying, send the screenshot to @rtx5069."
)


def build_upgrade_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "💾 Permanent — ₹250 / 2.75 USDT",
            callback_data="plans:dump"
        )],
        [InlineKeyboardButton(
            "⭐ 1 Month — ₹59 UPI",
            callback_data="plans:sub"
        )]
    ])


def build_plan_back_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("← Back to plans", callback_data="plans:menu")
    ]])


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
    # Keep in sync with BASE_DOMAINS in Terabox-API/terabox.py.
    '1024-terabox.com', '1024box.com', '1024tera.co', '1024tera.com',
    '1024terabox.com', '4funbox.co', '4funbox.com', '4funbox.in',
    'bestclouddrive.com', 'dubox.com', 'fancybox.in', 'freeterabox.com',
    'gibibox.com', 'goaibox.com', 'mirrorbox.com', 'mirrobox.com',
    'momerybox.com', 'nephobox.com', 'pebibox.com', 'terabox.app',
    'terabox.click', 'terabox.club', 'terabox.com', 'terabox.fun',
    'terabox.link', 'teraboxapp.com', 'teraboxcdn.app', 'teraboxcdn.com',
    'teraboxfree.com', 'teraboxlink.com', 'teraboxlite.com',
    'teraboxshare.com', 'teraboxsharefile.com', 'teraboxurl.com',
    'terafileshare.com', 'tera1024box.com', 'terasharefile.com',
    'terasharelink.com', 'terashareus.com', 'tibibox.com',
    'tttturbonet.com',
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
    if parsed_url.scheme not in ('http', 'https'):
        return False
    host = (parsed_url.hostname or '').lower().rstrip('.')
    return any(host == domain or host.endswith('.' + domain) for domain in VALID_DOMAINS)

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

def utcnow():
    return datetime.now(timezone.utc)


def to_utc(value):
    if value is None:
        return None
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def ist_today():
    return datetime.now(IST).strftime("%Y-%m-%d")


def format_ist(value):
    dt = to_utc(value)
    if dt is None:
        return "N/A"
    return dt.astimezone(IST).strftime("%d %b %Y, %I:%M %p IST")


def time_until_reset():
    now = datetime.now(IST)
    tomorrow = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    total_minutes = max(0, int((tomorrow - now).total_seconds() // 60))
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}h {minutes}m"


def format_remaining(expires_at):
    expiry = to_utc(expires_at)
    if expiry is None:
        return "Never"
    delta = expiry - utcnow()
    total_minutes = int(delta.total_seconds() // 60)
    if total_minutes <= 0:
        return "Expired"
    days, rem_minutes = divmod(total_minutes, 1440)
    hours, minutes = divmod(rem_minutes, 60)
    if days:
        return f"{days}d {hours}h"
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def get_premium_record(user_id):
    if premium_col is None:
        return None
    try:
        return premium_col.find_one({"user_id": user_id})
    except Exception as e:
        logger.warning(f"Could not load premium record for {user_id}: {e}")
        return None


def record_is_permanent(record):
    if not record:
        return False
    return record.get("plan") == "dump_permanent" or record.get("expires_at") is None


def premium_state(user_id):
    record = get_premium_record(user_id)
    if not record:
        return {
            "record": None, "active": False, "permanent": False,
            "plan": "free", "expires_at": None,
        }
    permanent = record_is_permanent(record)
    expires_at = to_utc(record.get("expires_at"))
    active = permanent or (expires_at is not None and expires_at > utcnow())
    return {
        "record": record,
        "active": active,
        "permanent": permanent,
        "plan": "dump_permanent" if permanent else (record.get("plan") or "bot_monthly"),
        "expires_at": expires_at,
    }


def is_premium(user_id):
    return premium_state(user_id)["active"]


def get_user_usage(user_id, day=None):
    day = day or ist_today()
    result = {"terabox": 0, "random": 0, "search": 0, "folder": 0}
    if usage_col is None:
        return result
    try:
        doc = usage_col.find_one({"_id": f"{user_id}:{day}"})
        if doc:
            for kind in result:
                result[kind] = int(doc.get(kind, 0))
    except Exception as e:
        logger.warning(f"Could not load usage for {user_id}: {e}")
    return result


def reserve_daily_usage(user_id, kind, limit):
    """Atomically reserve one daily use. Returns (ok, ist_date)."""
    day = ist_today()
    if usage_col is None:
        return None, day
    key = f"{user_id}:{day}"
    try:
        try:
            usage_col.update_one(
                {"_id": key},
                {"$setOnInsert": {
                    "user_id": user_id,
                    "date": day,
                    "terabox": 0,
                    "random": 0,
                    "search": 0,
                    "folder": 0,
                }},
                upsert=True,
            )
        except DuplicateKeyError:
            pass
        # Today's document may have been created before the folder counter
        # existed. Initialise it so the atomic $lt reservation can match.
        usage_col.update_one(
            {"_id": key, kind: {"$exists": False}},
            {"$set": {kind: 0}},
        )
        result = usage_col.update_one(
            {"_id": key, kind: {"$lt": limit}},
            {"$inc": {kind: 1}},
        )
        return result.modified_count == 1, day
    except Exception as e:
        logger.error(f"Could not reserve {kind} usage for {user_id}: {e}")
        return None, day


def refund_daily_usage(user_id, kind, day):
    if usage_col is None or not day:
        return
    try:
        usage_col.update_one(
            {"_id": f"{user_id}:{day}", kind: {"$gt": 0}},
            {"$inc": {kind: -1}},
        )
    except Exception as e:
        logger.warning(f"Could not refund {kind} usage for {user_id}: {e}")


def remaining_daily_usage(user_id):
    used = get_user_usage(user_id)
    return {
        "terabox": max(0, FREE_DAILY_TERABOX - used["terabox"]),
        "random": max(0, FREE_DAILY_RANDOM - used["random"]),
        "search": max(0, FREE_DAILY_SEARCH - used["search"]),
        "folder": max(0, FREE_DAILY_FOLDERS - used["folder"]),
        "used": used,
    }


def daily_limit_text(user_id, kind):
    key = {
        "terabox": "limit_terabox",
        "random": "limit_random",
        "search": "limit_search",
        "folder": "limit_folder",
    }[kind]
    limit = {
        "terabox": FREE_DAILY_TERABOX,
        "random": FREE_DAILY_RANDOM,
        "search": FREE_DAILY_SEARCH,
        "folder": FREE_DAILY_FOLDERS,
    }[kind]
    return t(
        user_id, key, limit=limit, reset=time_until_reset(),
        max=FREE_FOLDER_MAX_FILES,
    )


def days_remaining(expires_at):
    expiry = to_utc(expires_at)
    if expiry is None:
        return 0
    seconds = (expiry - utcnow()).total_seconds()
    if seconds <= 0:
        return 0
    return max(1, math.ceil(seconds / 86400))


def plan_summary(user_id):
    if user_id == OWNER_ID:
        return t(user_id, "plan_owner")
    state = premium_state(user_id)
    if state["permanent"]:
        return t(user_id, "plan_dump")
    if state["active"]:
        return t(
            user_id, "plan_paid",
            days=days_remaining(state["expires_at"]),
        )
    return t(user_id, "plan_free")


async def send_daily_limit(client, message, user_id, kind):
    await client.send_message(
        message.chat.id,
        daily_limit_text(user_id, kind),
        reply_markup=build_upgrade_keyboard(),
        parse_mode=None,
    )


async def send_quota_note(client, message, user_id, kind):
    remaining = remaining_daily_usage(user_id)[kind]
    note = await client.send_message(
        message.chat.id,
        t(user_id, "quota_left", remaining=remaining, reset=time_until_reset())
    )
    asyncio.create_task(delayed_delete(note, 30))


def user_snapshot_from_record(record):
    snapshot = (record or {}).get("user_snapshot") or {}
    return {
        "name": snapshot.get("name") or "Unknown",
        "username": snapshot.get("username"),
        "dc_id": snapshot.get("dc_id"),
    }


async def fetch_user_snapshot(client, user_id):
    try:
        user = await client.get_users(user_id)
        return {
            "name": user.first_name or "Unknown",
            "username": user.username,
            "dc_id": getattr(user, "dc_id", None),
        }
    except Exception as e:
        logger.warning(f"Could not resolve user {user_id}: {e}")
        return None


async def send_premium_log(client, text):
    if PREMIUM_INFO_ID is None:
        return False
    try:
        await client.send_message(
            PREMIUM_INFO_ID, text, parse_mode="html",
            disable_web_page_preview=True,
        )
        return True
    except Exception as e:
        logger.warning(f"Could not send premium log message: {e}")
        return False


async def send_long_html(client, chat_id, text, chunk_size=3800):
    lines = text.splitlines()
    chunk = []
    length = 0
    for line in lines:
        if length + len(line) + 1 > chunk_size and chunk:
            await client.send_message(
                chat_id, "\n".join(chunk), parse_mode="html",
                disable_web_page_preview=True,
            )
            chunk = []
            length = 0
        chunk.append(line)
        length += len(line) + 1
    if chunk:
        await client.send_message(
            chat_id, "\n".join(chunk), parse_mode="html",
            disable_web_page_preview=True,
        )


def parse_addressed_command(text, bot_username):
    """Return (command, args) for /command and /command@ThisBot.

    A command addressed to a different bot is ignored.
    """
    parts = (text or "").split()
    if not parts:
        return None
    token = parts[0]
    if not token.startswith("/"):
        return None
    command, sep, target = token[1:].partition("@")
    if sep and target:
        if not bot_username or target.lower() != bot_username.lower():
            return None
    return command.lower(), parts[1:]

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
        + "\n" + t(uid, "settings_plan", plan=plan_summary(uid))
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
    plans_button = InlineKeyboardButton(
        "⭐ Plans / Subscribe", callback_data="plans:menu"
    )
    reply_markup = InlineKeyboardMarkup([
        [join_button, developer_button],
        [repo69],
        [plans_button],
    ])
    final_msg = (
        t(uid, "welcome", mention=user_mention)
        + "\n\n"
        + t(uid, "welcome_plans")
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

    user_id = message.from_user.id
    privileged = user_id == OWNER_ID or premium_state(user_id)["active"]
    reserved_day = None

    pipeline = [{"$sample": {"size": 1}}]
    result = list(videos_col.aggregate(pipeline))
    if not result:
        await message.reply_text(t(user_id, "no_videos"))
        return

    if not privileged:
        reserved, reserved_day = reserve_daily_usage(
            user_id, "random", FREE_DAILY_RANDOM
        )
        if reserved is None:
            await message.reply_text(t(user_id, "mongo_missing"))
            return
        if not reserved:
            await send_daily_limit(client, message, user_id, "random")
            return

    doc = result[0]
    try:
        user_msg = await client.copy_message(message.chat.id, doc["chat_id"], doc["message_id"], caption="")
    except Exception as e:
        logger.error(f"Random delivery failed for {user_id}: {e}")
        if reserved_day:
            refund_daily_usage(user_id, "random", reserved_day)
        await message.reply_text(t(user_id, "search_send_failed"))
        return

    warn = await client.send_message(
        message.chat.id,
        t(user_id, "file_deleted_warning")
    )
    asyncio.create_task(delayed_delete(user_msg, 600))
    asyncio.create_task(delayed_delete(warn, 600))
    await message.delete()
    if reserved_day:
        await send_quota_note(client, message, user_id, "random")

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

    user_id = message.from_user.id
    privileged = user_id == OWNER_ID or premium_state(user_id)["active"]
    reserved_day = None
    if not privileged:
        reserved, reserved_day = reserve_daily_usage(
            user_id, "search", FREE_DAILY_SEARCH
        )
        if reserved is None:
            await message.reply_text(t(user_id, "mongo_missing"))
            return
        if not reserved:
            await send_daily_limit(client, message, user_id, "search")
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

    try:
        search_message = await message.reply_text(
            t(message.from_user.id, "search_header",
              keywords=" ".join(keywords), count=total),
            reply_markup=build_search_keyboard(token, results, page, total_pages),
            parse_mode=None
        )
    except Exception as e:
        logger.error(f"Search menu failed for {user_id}: {e}")
        search_sessions.pop(token, None)
        if reserved_day:
            refund_daily_usage(user_id, "search", reserved_day)
        await message.reply_text(t(user_id, "search_unavailable"))
        return

    search_sessions[token]["message"] = search_message
    asyncio.create_task(expire_search_session(token))
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f"Could not delete search command message: {e}")
    if reserved_day:
        await send_quota_note(client, message, user_id, "search")

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

def _snapshot_or_record(client_snapshot, record):
    if client_snapshot:
        return client_snapshot
    fallback = user_snapshot_from_record(record)
    return fallback


async def _notify_access_user(client, target_id, text):
    try:
        await client.send_message(target_id, text, parse_mode=None)
    except Exception as e:
        logger.info(f"Could not notify user {target_id}: {e}")


def _access_audit_text(title, target_id, snapshot, plan, expires_at, actor_id):
    username = snapshot.get("username")
    username_text = f"@{escape(username)}" if username else "N/A"
    return (
        f"{title}\n\n"
        f"User: <b>{escape(str(snapshot.get('name') or 'Unknown'))}</b>\n"
        f"Username: {username_text}\n"
        f"User ID: <code>{target_id}</code>\n"
        f"Plan: {plan}\n"
        f"Expires: {format_ist(expires_at) if expires_at else 'Never'}\n"
        f"Action by: <code>{actor_id}</code>\n"
        f"Time: {format_ist(utcnow())}"
    )


async def grant_monthly_subscription(client, target_id, actor_id):
    state = premium_state(target_id)
    if state["permanent"]:
        return "permanent", state["record"]

    now = utcnow()
    record = state["record"]
    snapshot = _snapshot_or_record(
        await fetch_user_snapshot(client, target_id), record
    )

    if record:
        first_joined = (
            record.get("first_joined_at")
            or record.get("added_at")
            or now
        )
        old_expiry = to_utc(record.get("expires_at"))
        if old_expiry and old_expiry > now:
            expires_at = old_expiry + timedelta(days=SUBSCRIPTION_DAYS)
            event = "renewed"
        else:
            expires_at = now + timedelta(days=SUBSCRIPTION_DAYS)
            event = "reactivated"
    else:
        first_joined = now
        expires_at = now + timedelta(days=SUBSCRIPTION_DAYS)
        event = "activated"

    premium_col.update_one(
        {"user_id": target_id},
        {"$set": {
            "user_id": target_id,
            "plan": "bot_monthly",
            "first_joined_at": first_joined,
            "period_started_at": now,
            "expires_at": expires_at,
            "added_at": first_joined,
            "added_by": actor_id,
            "updated_at": now,
            "expiry_notified_at": None,
            "user_snapshot": snapshot,
        }},
        upsert=True,
    )
    return event, premium_col.find_one({"user_id": target_id})


async def grant_dump_access(client, target_id, actor_id):
    state = premium_state(target_id)
    if state["permanent"]:
        return "already_permanent", state["record"]

    now = utcnow()
    record = state["record"]
    snapshot = _snapshot_or_record(
        await fetch_user_snapshot(client, target_id), record
    )
    first_joined = (
        (record or {}).get("first_joined_at")
        or (record or {}).get("added_at")
        or now
    )

    premium_col.update_one(
        {"user_id": target_id},
        {"$set": {
            "user_id": target_id,
            "plan": "dump_permanent",
            "first_joined_at": first_joined,
            "period_started_at": now,
            "expires_at": None,
            "added_at": first_joined,
            "added_by": actor_id,
            "updated_at": now,
            "expiry_notified_at": None,
            "user_snapshot": snapshot,
        }},
        upsert=True,
    )
    return "granted", premium_col.find_one({"user_id": target_id})


def _require_owner(message):
    return message.from_user is not None and message.from_user.id == OWNER_ID


async def handle_add_subscription(client, message, args):
    if not _require_owner(message):
        return
    if db is None:
        await message.reply_text("MongoDB not configured.")
        return
    if not args:
        await message.reply_text("Usage: /add USER_ID")
        return
    try:
        target_id = int(args[0])
    except ValueError:
        await message.reply_text("Invalid user ID.")
        return

    event, record = await grant_monthly_subscription(client, target_id, OWNER_ID)
    if event == "permanent":
        await message.reply_text("This user already has permanent dump access.")
        return

    expires = format_ist(record.get("expires_at"))
    snapshot = _snapshot_or_record(None, record)
    labels = {
        "activated": "Subscription activated",
        "renewed": "Subscription renewed",
        "reactivated": "Subscription reactivated",
    }
    await message.reply_text(
        f"✅ {labels.get(event, 'Subscription updated')} for "
        f"<a href='tg://user?id={target_id}'>{escape(str(snapshot.get('name') or 'Unknown'))}</a>\n"
        f"Expires: {expires}",
        parse_mode="html",
    )
    await _notify_access_user(
        client, target_id,
        "⭐ Jet Premium activated!\n\n"
        f"Your unlimited downloads, folders, /random and /search are active until {expires}.",
    )
    await send_premium_log(
        client,
        _access_audit_text(
            f"🟢 <b>{labels.get(event, 'Subscription updated')}</b>",
            target_id, snapshot, "Monthly subscription (30 days)",
            record.get("expires_at"), OWNER_ID,
        ),
    )


async def handle_add_dump(client, message, args):
    if not _require_owner(message):
        return
    if db is None:
        await message.reply_text("MongoDB not configured.")
        return
    if not args:
        await message.reply_text("Usage: /adddump USER_ID")
        return
    try:
        target_id = int(args[0])
    except ValueError:
        await message.reply_text("Invalid user ID.")
        return

    event, record = await grant_dump_access(client, target_id, OWNER_ID)
    if event == "already_permanent":
        await message.reply_text("This user already has permanent dump access.")
        return

    snapshot = _snapshot_or_record(None, record)
    await message.reply_text(
        f"💾 Permanent dump access granted to "
        f"<a href='tg://user?id={target_id}'>{escape(str(snapshot.get('name') or 'Unknown'))}</a>.",
        parse_mode="html",
    )
    await _notify_access_user(
        client, target_id,
        "💾 Permanent dump access activated!\n\n"
        "You now have permanent access to the dump channel, unlimited TeraBox "
        "downloads, folder downloads, /random and /search.",
    )
    await send_premium_log(
        client,
        _access_audit_text(
            "💾 <b>Permanent dump access granted</b>",
            target_id, snapshot, "Permanent dump access", None, OWNER_ID,
        ),
    )


async def handle_remove_premium(client, message, args):
    if not _require_owner(message):
        return
    if db is None:
        await message.reply_text("MongoDB not configured.")
        return
    if not args:
        await message.reply_text("Usage: /remove USER_ID")
        return
    try:
        target_id = int(args[0])
    except ValueError:
        await message.reply_text("Invalid user ID.")
        return

    record = get_premium_record(target_id)
    if not record:
        await message.reply_text("No premium record found for this user.")
        return

    snapshot = _snapshot_or_record(None, record)
    premium_col.delete_one({"user_id": target_id})
    await message.reply_text(
        f"🗑 Premium record removed for "
        f"<a href='tg://user?id={target_id}'>{escape(str(snapshot.get('name') or 'Unknown'))}</a>.",
        parse_mode="html",
    )
    await _notify_access_user(
        client, target_id,
        "Your Jet Premium access has been removed. Send /subscribe to see the plans.",
    )
    await send_premium_log(
        client,
        _access_audit_text(
            "🔴 <b>Premium record removed</b>",
            target_id, snapshot,
            "Permanent" if record_is_permanent(record) else "Monthly subscription",
            record.get("expires_at"), OWNER_ID,
        ),
    )


def _user_info_entry(target_id, snapshot, record, status):
    username = snapshot.get("username")
    username_text = f"@{escape(username)}" if username else "N/A"
    dc_id = snapshot.get("dc_id")
    first_joined = (
        record.get("first_joined_at")
        or record.get("added_at")
    )
    period_start = record.get("period_started_at") or record.get("added_at")
    permanent = record_is_permanent(record)
    plan = "Permanent dump access" if permanent else "Monthly subscription"
    expires = "Never" if permanent else format_ist(record.get("expires_at"))
    remaining = "Never" if permanent else format_remaining(record.get("expires_at"))
    return (
        f"👤 <b>{escape(str(snapshot.get('name') or 'Unknown'))}</b>\n"
        f"🔗 {username_text}\n"
        f"🆔 <code>{target_id}</code>\n"
        f"📡 DC: {dc_id if dc_id else 'N/A'}\n"
        f"💎 Plan: {plan}\n"
        f"📅 DOJ: {format_ist(first_joined)}\n"
        f"🔁 Period start: {format_ist(period_start)}\n"
        f"⏳ Expires: {expires}\n"
        f"⌛ Remaining: {remaining}\n"
        f"📌 Status: {status}"
    )


async def handle_user_info(client, message, args=None):
    if not _require_owner(message):
        return
    if db is None:
        await message.reply_text("MongoDB not configured.")
        return

    records = list(premium_col.find({}))
    if not records:
        await message.reply_text("No premium users yet.")
        return

    permanent = []
    active = []
    expired = []
    now = utcnow()

    for record in records:
        target_id = record.get("user_id")
        if target_id is None:
            continue
        snapshot = user_snapshot_from_record(record)
        if not snapshot.get("name") or snapshot.get("name") == "Unknown":
            snapshot = _snapshot_or_record(
                await fetch_user_snapshot(client, target_id), record
            )
        if record_is_permanent(record):
            permanent.append((target_id, snapshot, record))
            continue
        expiry = to_utc(record.get("expires_at"))
        if expiry and expiry > now:
            active.append((target_id, snapshot, record))
        else:
            expired.append((target_id, snapshot, record))

    active.sort(key=lambda item: to_utc(item[2].get("expires_at")) or now)
    expired.sort(key=lambda item: to_utc(item[2].get("expires_at")) or now)

    bot_username = client.me.username if client.me else ""
    remove_hint = (
        f"\nTo remove: /remove@{bot_username} USER_ID"
        if bot_username else ""
    )

    text = (
        "📊 <b>Premium Information</b>\n\n"
        f"Permanent: {len(permanent)} | Active: {len(active)} | Expired: {len(expired)}\n"
        f"Updated: {format_ist(now)}"
    )

    if permanent:
        text += "\n\n💾 <b>Permanent dump users</b>"
        for target_id, snapshot, record in permanent:
            text += "\n\n" + _user_info_entry(
                target_id, snapshot, record, "Permanent"
            )

    if active:
        text += "\n\n⭐ <b>Active monthly subscriptions</b>"
        for target_id, snapshot, record in active:
            text += "\n\n" + _user_info_entry(
                target_id, snapshot, record, "Active"
            )

    if expired:
        text += "\n\n⌛ <b>Expired records — not removed</b>"
        for target_id, snapshot, record in expired:
            text += "\n\n" + _user_info_entry(
                target_id, snapshot, record, "Expired — awaiting removal"
            )
        text += f"\n\n{remove_hint}" if remove_hint else ""

    await send_long_html(client, message.chat.id, text)


async def handle_my_status(client, message):
    if not message.from_user:
        return
    user_id = message.from_user.id
    if user_id == OWNER_ID:
        await message.reply_text(
            "👑 Owner access: unlimited downloads, folders, /random and /search."
        )
        return

    state = premium_state(user_id)
    limits = remaining_daily_usage(user_id)

    if state["permanent"]:
        plan_line = "💾 Permanent dump access"
        expiry_line = "Expires: Never"
        access_line = "Downloads: Unlimited | Folders: Unlimited | /random: Unlimited | /search: Unlimited"
    elif state["active"]:
        plan_line = "⭐ Monthly subscription"
        expiry_line = f"Expires: {format_ist(state['expires_at'])}"
        access_line = "Downloads: Unlimited | Folders: Unlimited | /random: Unlimited | /search: Unlimited"
    else:
        plan_line = "🆓 Free tier"
        expiry_line = "Expires: N/A"
        access_line = (
            f"Downloads: {limits['terabox']}/{FREE_DAILY_TERABOX} left | "
            f"/random: {limits['random']}/{FREE_DAILY_RANDOM} left | "
            f"/search: {limits['search']}/{FREE_DAILY_SEARCH} left | "
            f"Folders: {limits['folder']}/{FREE_DAILY_FOLDERS} left "
            f"(max {FREE_FOLDER_MAX_FILES} files)"
        )

    await message.reply_text(
        "👤 <b>Your Jet Premium status</b>\n\n"
        f"Plan: {plan_line}\n"
        f"{expiry_line}\n"
        f"{access_line}\n\n"
        f"Daily limits reset in {time_until_reset()} (12:00 AM IST).\n"
        "Use /subscribe to unlock unlimited access.",
        parse_mode="html",
        reply_markup=build_upgrade_keyboard() if not state["active"] else None,
    )


@app.on_message(filters.command("add"))
async def add_premium(client: Client, message: Message):
    await handle_add_subscription(client, message, message.command[1:])


@app.on_message(filters.command("adddump"))
async def add_dump(client: Client, message: Message):
    await handle_add_dump(client, message, message.command[1:])


@app.on_message(filters.command("remove"))
async def remove_premium(client: Client, message: Message):
    await handle_remove_premium(client, message, message.command[1:])


@app.on_message(filters.command("user_info"))
async def user_info_command(client: Client, message: Message):
    # Works in PM and in the audit chat (the audit chat guard handles the
    # latter before this handler is reached).
    await handle_user_info(client, message, message.command[1:])


@app.on_message(filters.command("list"))
async def list_premium(client: Client, message: Message):
    # Owner-only alias kept for convenience outside the log chat.
    if message.chat.id == PREMIUM_INFO_ID:
        return
    await handle_user_info(client, message)


@app.on_message(filters.command(["subscribe", "plans"]))
async def subscribe_command(client: Client, message: Message):
    await message.reply_text(
        PLANS_CAPTION,
        reply_markup=build_upgrade_keyboard(),
        parse_mode=None,
        disable_web_page_preview=True,
    )


@app.on_message(filters.command("mystatus"))
async def my_status_command(client: Client, message: Message):
    await handle_my_status(client, message)


@app.on_callback_query(filters.regex(r"^plans:"))
async def plans_callback(client: Client, callback_query):
    action = callback_query.data.split(":", 1)[1]
    chat_id = callback_query.message.chat.id

    if action == "dump":
        if not os.path.exists(DUMP_DONATION_IMAGE):
            await callback_query.answer("Payment information is unavailable.", show_alert=True)
            return
        await callback_query.answer("Opening permanent plan...")
        await client.send_photo(
            chat_id, DUMP_DONATION_IMAGE,
            caption=DUMP_OFFER_CAPTION,
            reply_markup=build_dump_payment_keyboard(callback_query.from_user.id),
            parse_mode=None,
        )
        return

    if action == "sub":
        upi_path = DUMP_QR_FILES["upi"]
        if not os.path.exists(upi_path):
            await callback_query.answer("Payment information is unavailable.", show_alert=True)
            return
        await callback_query.answer("Opening monthly plan...")
        await client.send_photo(
            chat_id, upi_path,
            caption=MONTHLY_CAPTION,
            reply_markup=build_plan_back_keyboard(),
            parse_mode=None,
        )
        return

    if action == "menu":
        await callback_query.answer()
        await client.send_message(
            chat_id, PLANS_CAPTION,
            reply_markup=build_upgrade_keyboard(),
            parse_mode=None,
            disable_web_page_preview=True,
        )
        return

    await callback_query.answer("Unknown plan.", show_alert=True)

async def premium_expiry_monitor():
    await asyncio.sleep(20)
    while True:
        try:
            if premium_col is not None:
                now = utcnow()
                expired = list(premium_col.find({
                    "plan": "bot_monthly",
                    "expires_at": {"$lte": now},
                    "expiry_notified_at": None,
                }))
                for record in expired:
                    target_id = record.get("user_id")
                    if target_id is None:
                        continue
                    snapshot = _snapshot_or_record(None, record)
                    bot_username = app.me.username if app.me else ""
                    remove_command = (
                        f"/remove@{bot_username} {target_id}"
                        if bot_username else f"/remove {target_id}"
                    )
                    text = (
                        "🔴 <b>Subscription ended</b>\n\n"
                        f"<code>{target_id}</code> "
                        f"({escape(str(snapshot.get('name') or 'Unknown'))}) "
                        "sub has just ended, Should i remove them?\n\n"
                        f"Expired: {format_ist(record.get('expires_at'))}\n"
                        "The record was <b>not</b> removed.\n"
                        f"<code>{escape(remove_command)}</code>"
                    )
                    if await send_premium_log(app, text):
                        premium_col.update_one(
                            {"_id": record["_id"]},
                            {"$set": {"expiry_notified_at": now}},
                        )
                        logger.info(f"Premium expiry notified for {target_id}")
        except Exception as e:
            logger.exception(f"Premium expiry monitor failed: {e}")
        await asyncio.sleep(300)


def _update_chat(update):
    chat = getattr(update, "chat", None)
    if chat is None:
        chat = getattr(getattr(update, "message", None), "chat", None)
    return chat


def _is_audit_chat(chat):
    return (
        PREMIUM_INFO_ID is not None
        and chat is not None
        and chat.id == PREMIUM_INFO_ID
    )


def _audit_chat_filter(_, __, update):
    return _is_audit_chat(_update_chat(update))


def _other_group_message_filter(_, __, message):
    chat = getattr(message, "chat", None)
    if chat is None or chat.type == ChatType.PRIVATE:
        return False
    return not _is_audit_chat(chat)


def _other_group_callback_filter(_, __, callback_query):
    chat = getattr(getattr(callback_query, "message", None), "chat", None)
    if chat is None or chat.type == ChatType.PRIVATE:
        return False
    return not _is_audit_chat(chat)


audit_chat_filter = filters.create(_audit_chat_filter)
other_group_message_filter = filters.create(_other_group_message_filter)
other_group_callback_filter = filters.create(_other_group_callback_filter)


# The bot only works in PM. The audit chat is the sole exception and answers
# only the owner's /user_info. Every other group is completely silent.
@app.on_message(audit_chat_filter, group=-3)
async def audit_chat_guard(client, message):
    try:
        if (
            message.from_user
            and message.from_user.id == OWNER_ID
            and message.text
        ):
            parsed = parse_addressed_command(
                message.text,
                client.me.username if client.me else None,
            )
            if parsed and parsed[0] == "user_info":
                await handle_user_info(client, message, parsed[1])
    except Exception as e:
        logger.exception(f"Audit chat guard failed: {e}")
    raise StopPropagation


@app.on_message(other_group_message_filter, group=-3)
async def group_silence_guard(client, message):
    raise StopPropagation


@app.on_callback_query(audit_chat_filter, group=-3)
async def audit_chat_callback_guard(client, callback_query):
    raise StopPropagation


@app.on_callback_query(other_group_callback_filter, group=-3)
async def group_callback_silence_guard(client, callback_query):
    raise StopPropagation


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
        return {"sent": 0, "failed": 0, "delivered": False}

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
            return {"sent": 0, "failed": failed, "delivered": False}

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
    return {
        "sent": sent,
        "failed": failed,
        "delivered": delivered or bool(user_msgs),
    }


def _zip_part_sort_key(path):
    name = os.path.basename(path)
    match = re.search(r"\.z(\d+)$", name)
    if match:
        return (0, int(match.group(1)))
    match = re.search(r"\.zip\.(\d+)$", name)
    if match:
        return (0, int(match.group(1)))
    return (1, 0)


def _create_single_zip(archive_path, items):
    with zipfile.ZipFile(
        archive_path, "w", zipfile.ZIP_STORED, allowZip64=True
    ) as archive:
        for path, rel in items:
            if os.path.exists(path):
                archive.write(path, rel)
    return [archive_path]


def create_folder_archive(workdir, archive_base, items, split_size):
    """Create a zip archive (splitting into volumes when needed).

    Uses the ``zip`` binary when available, then ``7z``/``7za``, and finally
    Python's stdlib ``zipfile`` so the bot never fails just because the image
    lacks the zip package. Runs in a worker thread.
    """
    existing = [(p, rel) for p, rel in items if os.path.exists(p)]
    if not existing:
        return []

    total_bytes = sum(os.path.getsize(p) for p, _ in existing)
    margin = min(50 * 1024 * 1024, max(0, split_size // 10))
    part_bytes = max(1, split_size - margin)
    part_mb = max(1, part_bytes // (1024 * 1024))
    archive_path = archive_base + ".zip"
    needs_split = total_bytes > part_bytes

    zip_bin = shutil.which("zip")
    seven_zip = shutil.which("7z") or shutil.which("7za")

    def run(cmd):
        subprocess.run(
            cmd, cwd=workdir, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

    if zip_bin:
        cmd = [zip_bin, "-r", "-q"]
        if needs_split:
            cmd += ["-s", f"{part_mb}m"]
        cmd += [archive_path, "."]
        run(cmd)
    elif seven_zip:
        cmd = [seven_zip, "a", "-tzip"]
        if needs_split:
            cmd += [f"-v{part_mb}m"]
        cmd += [archive_path, "."]
        run(cmd)
    elif not needs_split:
        return _create_single_zip(archive_path, existing)
    else:
        # No zip tool at all: send independent archives that each fit the
        # upload limit. A single file larger than the limit still cannot fit.
        groups = []
        current = []
        current_size = 0
        for item in existing:
            size = os.path.getsize(item[0])
            if current and current_size + size > part_bytes:
                groups.append(current)
                current = []
                current_size = 0
            current.append(item)
            current_size += size
        if current:
            groups.append(current)
        paths = []
        for index, group in enumerate(groups, 1):
            path = f"{archive_base}_part{index}.zip"
            _create_single_zip(path, group)
            paths.append(path)
        return paths

    parts = [
        p for p in glob.glob(archive_base + ".*")
        if os.path.isfile(p) and re.search(r"\.zip(\.\d+)?$|\.z\d+$", p)
    ]
    return sorted(parts, key=_zip_part_sort_key)


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
            return {"sent": 0, "failed": failed, "delivered": False}

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
            return {"sent": 0, "failed": failed, "delivered": False}

        await update_status_message(
            status_message,
            f"🗜️ Creating archive\n{len(downloaded)} files • {format_size(total_bytes)}",
        )
        try:
            parts = await asyncio.to_thread(
                create_folder_archive,
                workdir, archive_base, downloaded, SPLIT_SIZE,
            )
        except Exception as e:
            logger.exception(f"Could not create folder archive: {e}")
            await message.reply_text(t(user_id, "download_failed"))
            return {"sent": 0, "failed": failed, "delivered": False}
        if not parts:
            await message.reply_text(t(user_id, "download_failed"))
            return {"sent": 0, "failed": failed, "delivered": False}

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
        return {
            "sent": len(user_msgs),
            "failed": failed,
            "delivered": delivered or bool(user_msgs),
        }
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
        privileged = user_id == OWNER_ID or premium_state(user_id)["active"]
        all_files = info.get("files") or []
        downloadable, _ = _split_folder_files(info)
        if not downloadable:
            try:
                await status_message.delete()
                await message.delete()
            except Exception:
                pass
            await client.send_message(
                message.chat.id,
                t(user_id, "folder_empty"),
                parse_mode=None,
            )
            return

        reserved_day = None
        if not privileged:
            if len(all_files) > FREE_FOLDER_MAX_FILES:
                try:
                    await status_message.delete()
                    await message.delete()
                except Exception:
                    pass
                await client.send_message(
                    message.chat.id,
                    t(
                        user_id, "folder_too_large",
                        count=len(all_files), max=FREE_FOLDER_MAX_FILES,
                    ),
                    reply_markup=build_upgrade_keyboard(),
                    parse_mode=None,
                )
                return
            reserved, reserved_day = reserve_daily_usage(
                user_id, "folder", FREE_DAILY_FOLDERS
            )
            if reserved is None:
                try:
                    await status_message.delete()
                except Exception:
                    pass
                await message.reply_text(t(user_id, "mongo_missing"))
                return
            if not reserved:
                try:
                    await status_message.delete()
                    await message.delete()
                except Exception:
                    pass
                await send_daily_limit(client, message, user_id, "folder")
                return

        mode = get_user_setting(user_id, "folder_mode", DEFAULT_FOLDER_MODE)
        folder_result = None
        try:
            if mode == "zip":
                folder_result = await process_folder_zip(
                    client, message, user_id, info, status_message
                )
            else:
                folder_result = await process_folder_single(
                    client, message, user_id, info, status_message
                )
        except Exception as e:
            logger.exception(f"Folder processing failed: {e}")
            if reserved_day:
                refund_daily_usage(user_id, "folder", reserved_day)
            await message.reply_text(t(user_id, "download_failed"))
        else:
            if reserved_day and not (folder_result or {}).get("delivered"):
                refund_daily_usage(user_id, "folder", reserved_day)
    else:
        privileged = user_id == OWNER_ID or premium_state(user_id)["active"]
        reserved_day = None
        if not privileged:
            reserved, reserved_day = reserve_daily_usage(
                user_id, "terabox", FREE_DAILY_TERABOX
            )
            if reserved is None:
                try:
                    await status_message.delete()
                except Exception:
                    pass
                await message.reply_text(t(user_id, "mongo_missing"))
                return
            if not reserved:
                try:
                    await status_message.delete()
                    await message.delete()
                except Exception:
                    pass
                await send_daily_limit(client, message, user_id, "terabox")
                return

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
            if reserved_day:
                refund_daily_usage(user_id, "terabox", reserved_day)
            await message.reply_text(t(user_id, "download_failed"))
        elif reserved_day:
            await send_quota_note(client, message, user_id, "terabox")

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

OWNER_MENU_LABEL = "𝗢𝘄𝗻𝗲𝗿 𝗢𝗻𝗹𝘆"


def _telegram_api(method, payload):
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/{method}",
            json=payload,
            timeout=20,
        )
        data = resp.json()
        if not data.get("ok"):
            logger.warning(f"{method} failed: {data.get('description')}")
        return data
    except Exception as e:
        logger.warning(f"{method} request failed: {e}")
        return None


def setup_command_menu():
    """Publish the command menu: full list in PM, /user_info in audit chat."""
    user_info_command = {
        "command": "user_info",
        "description": f"{OWNER_MENU_LABEL} — Show all premium users",
    }
    private_commands = [
        {"command": "start", "description": "Start the Bot"},
        {"command": "user_settings", "description": "User Specific Settings"},
        {"command": "random", "description": "Get Random Media from Dump Channel"},
        {"command": "search", "description": "Search a Video in Dump Channel"},
        {"command": "dump", "description": "Get Full Permanent Access to Dump Channel"},
        {"command": "subscribe", "description": "Monthly plan — ₹59 for 30 days"},
        {"command": "plans", "description": "View all plans and prices"},
        {"command": "mystatus", "description": "Check your plan and daily limits"},
        {"command": "cancel", "description": "Cancel a pending input"},
        {"command": "refresh", "description": f"{OWNER_MENU_LABEL} — Refresh the video index"},
        user_info_command,
        {"command": "add", "description": f"{OWNER_MENU_LABEL} — Add/renew a 30-day subscription"},
        {"command": "adddump", "description": f"{OWNER_MENU_LABEL} — Grant permanent dump access"},
        {"command": "remove", "description": f"{OWNER_MENU_LABEL} — Remove a user's premium access"},
        {"command": "list", "description": f"{OWNER_MENU_LABEL} — List premium users"},
    ]
    _telegram_api("setMyCommands", {"commands": private_commands})
    _telegram_api(
        "setMyCommands",
        {"commands": [], "scope": {"type": "all_group_chats"}},
    )
    if PREMIUM_INFO_ID is not None:
        _telegram_api(
            "setMyCommands",
            {
                "commands": [user_info_command],
                "scope": {"type": "chat", "chat_id": PREMIUM_INFO_ID},
            },
        )


async def run_bot():
    await app.start()
    logger.info("Bot client started!")
    setup_command_menu()
    asyncio.create_task(premium_expiry_monitor())
    await idle()
    await app.stop()


if __name__ == "__main__":
    keep_alive()

    if user:
        logger.info("Starting user client...")
        Thread(target=run_user).start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_indexing())

    loop.run_until_complete(run_bot())
