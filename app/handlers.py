from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command  # ← добавлено
from app.messages import langs
from app.keyboards import get_main_menu
from app.config import ADMINS

router = Router()

# ✅ Новый хендлер команды /start
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("👋 Привет! Я бот-помощник. Выберите нужную функцию из меню.")

@router.message(F.text.in_([langs["ru"]["menu"], langs["uz"]["menu"]]))
async def main_menu(message: Message, state: FSMContext):
    await message.answer("🔘 Меню")

@router.message(F.text.in_([langs["ru"]["admin_panel"], langs["uz"]["admin_panel"]]))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("⛔️ У вас нет доступа")
    await message.answer("👮‍♂️ Добро пожаловать в админ-панель!")
