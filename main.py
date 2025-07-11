import os
from aiohttp import web
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import setup_application

# 🔧 Load .env
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
WEBHOOK_URL_FULL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8443))

# 🔁 Initialize bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# 📥 Router for /start and general messages
from handlers import debug
dp.include_router(debug.router)

# ✅ 🔥 Catch-all update to avoid 404 from Telegram
@dp.update()
async def catch_all_updates(update: Update):
    print("📥 Got update:", update)

# 🔄 Webhook setup
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL_FULL)
    print(f"✅ Webhook set: {WEBHOOK_URL_FULL}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()
    print("🛑 Webhook deleted and bot session closed.")

# 🚀 Start server
def main():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    print(f"👉 WEBHOOK_PATH: {WEBHOOK_PATH}")
    print(f"👉 WEBHOOK_URL_FULL: {WEBHOOK_URL_FULL}")
    setup_application(app, dp, path=WEBHOOK_PATH)

    web.run_app(app, host=HOST, port=PORT)

if __name__ == "__main__":
    main()
