import sys
import logging
from os import getenv
from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

API_TOKEN = getenv("API_TOKEN")
WEBHOOK_URL = getenv("WEBHOOK_URL")
WEBHOOK_PATH = getenv("WEBHOOK_PATH")
WEBHOOK_URL_FULL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"
HOST = getenv("HOST")
PORT = int(getenv("PORT"))

# 🔁 Initialize bot
bot = Bot(token=API_TOKEN)
router = Router ()
dp = Dispatcher

# 📥 Router for /start and general messages
from handlers import debug
router(debug.cmd_start, debug.catch_all)

# ✅ 🔥 Catch-all update to avoid 404 from Telegram

@dp.update()
async def handle_all_updates(update: Update):
    print("📥 Telegram update received")

# 🔄 Webhook setup
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL_FULL)
    print(f"✅ Webhook set: {WEBHOOK_URL_FULL}")    

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()
    print("🛑 Webhook deleted and bot session closed.")

# 🚀 Start server
def main():
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot, 
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=HOST, port=PORT)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    logging.info(f"👉 WEBHOOK_PATH: {WEBHOOK_PATH}")
    logging.info(f"👉 WEBHOOK_URL_FULL: {WEBHOOK_URL_FULL}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
