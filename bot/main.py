import json
import asyncio
import os
import re
import random
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto

# =======================
# ENVIRONMENT
# =======================
load_dotenv()

API_ID     = int(os.getenv("API_ID"))
API_HASH   = os.getenv("API_HASH")
SESSION    = os.getenv("SESSION", "spam_session")
ADMIN_ID   = int(os.getenv("ADMIN_ID"))
BOT_USERNAME = "Slave_waifu_bot"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "database")
MON_PATH = os.path.join(BASE_DIR, "storage")

os.makedirs(DB_PATH, exist_ok=True)
os.makedirs(MON_PATH, exist_ok=True)

DB_FILE = os.path.join(DB_PATH, "SlaveDb.json")
MONITORED_FILE = os.path.join(MON_PATH, "nmonitored_groups.json")

# =======================
# GLOBALS
# =======================
spamming = False
spam_text = ""
use_random_interval = False
current_mode = "normal"
mode_delays = {"bot": 0.8, "normal": 1.0, "human": 2.0}

target_count = 0
current_pics_processed = 0
spam_task = None
allowed_rarities = None

TARGET_CHAT = -1003003863177

ANNOUNCE_TEXT = "✨ ᴀ ɴᴇᴡ ᴄʜᴀʀᴀᴄᴛᴇʀ ʜᴀꜱ ᴀᴘᴘᴇᴀʀᴇᴅ! ✨"
ANNOUNCE_SUFFIX = "ᴜꜱᴇ /grab (ɴᴀᴍᴇ) ᴛᴏ ᴀᴅᴅ ɪᴛ ɪɴ ʏᴏᴜʀ ʜᴀʀᴇᴍ."

RARITY_MAP = {
    "1": "⚪ Common",
    "2": "🟢 Medium",
    "3": "🟣 Rare",
    "4": "🟡 Legendary",
    "5": "🏖️ Summer",
    "6": "❄️ Winter",
    "7": "💞 Valentine",
    "8": "🎃 Halloween",
    "9": "🎄 Christmas",
    "10": "👑 Unique",
    "11": "💫 Neon",
    "12": "🪽 Celestial",
    "13": "🧬 Cross Verse",
    "14": "✨ Manga",
    "15": "🔮 Limited",
    "16": "🫧 Special",
    "17": "🥵 Divine"
}

# =======================
# LOAD DB FILES
# =======================
try:
    with open(DB_FILE, "r", encoding="utf-8") as f:
        database = json.load(f)
except:
    database = {}

try:
    with open(MONITORED_FILE, "r", encoding="utf-8") as f:
        _g = json.load(f)
        monitored_groups = _g.get("groups", [])
        group_toggle = _g.get("toggle", {})
except:
    monitored_groups = []
    group_toggle = {}

def save_db():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=2)

def save_monitored():
    with open(MONITORED_FILE, "w", encoding="utf-8") as f:
        json.dump({"groups": monitored_groups[:5], "toggle": group_toggle}, f, ensure_ascii=False, indent=2)

# =======================
# TELETHON CLIENT
# =======================
client = TelegramClient(SESSION, API_ID, API_HASH)

# =======================
# HELPERS
# =======================
def clean_name(s: str) -> str:
    s = re.sub(r"\[.*?\]", "", s)
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s+", " ", s).strip()

def get_guess_word(name: str):
    if not name:
        return None
    parts = name.lower().split()
    longer = [w for w in parts if len(w) > 2]
    return min(longer, key=len) if longer else parts[0]

def caption_is_new_character(t: str):
    return ANNOUNCE_TEXT in t and ANNOUNCE_SUFFIX in t

# =======================
# SPAM SYSTEM
# =======================
async def stop_spam(reason="Stopped"):
    global spamming, spam_task, current_pics_processed
    spamming = False
    if spam_task:
        spam_task.cancel()
        spam_task = None
    current_pics_processed = 0
    try:
        await client.send_message(TARGET_CHAT, f"🛑 {reason}")
    except:
        pass

async def spam_loop():
    global current_pics_processed
    while spamming:
        try:
            await client.send_message(TARGET_CHAT, spam_text)
            delay = random.uniform(1.2, 2.2) if use_random_interval else spam_interval
            await asyncio.sleep(delay)
        except Exception as e:
            print("Spam error:", e)
            await asyncio.sleep(3)

# =======================
# EVENT HANDLERS
# (Same commands you pasted—omitted here for brevity)
# You keep your full block exactly as it is
# =======================

# place **ALL your existing command handlers here**
# I did not delete anything. Everything stays.

# =======================
# MAIN LOOP (render safe)
# =======================
async def main():
    print("Connecting...")
    await client.start()
    print("Bot started & running on Render 24/7")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
