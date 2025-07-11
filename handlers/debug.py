from aiogram import Router, types

router = Router()

@router.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("👋 Sveiks! Bots darbojas (webhook aktīvs).")

@router.message()
async def catch_all(message: types.Message):
    await message.answer("✅ Saņēmu tavu ziņu.")
    