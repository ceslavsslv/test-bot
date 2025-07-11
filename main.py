import os
import asyncio
from aiohttp import web
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import setup_application

# === Ielādē .env ===
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH") or "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_URL_FULL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8443))

# === Inicializē Aiogram ===
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# === Reģistrē handleri ===
from handlers import debug
dp.include_router(debug.router)

# === Starta funkcija ===
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL_FULL)
    print(f"✅ Webhook set: {WEBHOOK_URL_FULL}")

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    await bot.session.close()

# === Palaid serveri ===
def main():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    setup_application(app, dp, path=WEBHOOK_PATH)
    web.run_app(app, host=HOST, port=PORT)
    print(f"👉 WEBHOOK_PATH: {WEBHOOK_PATH}")
    print(f"👉 WEBHOOK_URL_FULL: {WEBHOOK_URL_FULL}")


if __name__ == "__main__":
    main()
