from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart("/start"))
async def cmd_start(message: types.Message):
    await message.answer(f"👋 Sveiks! Bots darbojas (webhook aktīvs).")

@router.message()
async def catch_all(message: types.Message):
    await message.answer("✅ Saņēmu tavu ziņu.")
