from aiogram import Router, types

router = Router()

@router.message()
async def debug_response(message: types.Message):
    await message.answer("✅ Bot ir dzīvs un darbojas!")
