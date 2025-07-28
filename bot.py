import os
import asyncio
from telethon import TelegramClient, events
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
VIP_CHANNEL_LINK = os.getenv("VIP_CHANNEL_LINK")

bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond("👋 Welcome! Please send your Quotex UID for verification.")

@bot.on(events.NewMessage(pattern=r"^\d{6,}$"))
async def verify_uid(event):
    uid = event.raw_text.strip()
    await event.respond("⏳ Verifying UID... Please wait.")

    try:
        options = Options()
        options.binary_location = "/usr/bin/google-chrome"
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://t.me/QuotexPartnerBot")
        await asyncio.sleep(5)

        await event.respond(f"✅ UID Verified!
Welcome to VIP: {VIP_CHANNEL_LINK}")
        driver.quit()
    except Exception as e:
        await event.respond(f"❌ Error during verification: {e}")

bot.run_until_disconnected()