from aiogram import Router, types

router = Router()

@router.message()
async def test_handler(message: types.Message):
    await message.answer("✅ Bot ir dzīvs un darbojas!")
