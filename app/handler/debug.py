from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text)
async def show_chat_id(message: Message):
    await message.answer(
        f"💬 <b>chat.id</b>: <code>{message.chat.id}</code>",
        parse_mode="HTML"
    )
