from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.messages import langs
from app.keyboards import get_main_menu, get_language_keyboard, get_agreement_keyboard
from app.config import ADMINS
from aiogram.fsm.state import StatesGroup, State

router = Router()

# 👤 Шаги регистрации
class RegisterState(StatesGroup):
    full_name = State()
    phone = State()
    birthday = State()
    pinfl = State()

# 🚀 Стартовая команда
@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🇷🇺 Пожалуйста, выберите язык / 🇺🇿 Iltimos, tilni tanlang",
        reply_markup=get_language_keyboard()
    )

# 🌐 Выбор языка
@router.message(F.text.in_(["🇷🇺 Русский", "🇺🇿 O‘zbek"]))
async def select_language(message: Message, state: FSMContext):
    lang = "ru" if message.text == "🇷🇺 Русский" else "uz"
    await state.update_data(lang=lang)
    await message.answer(
        langs[lang]["warning_text"],
        reply_markup=get_agreement_keyboard(lang)
    )

# ⚠️ Подтверждение согласия
@router.message(F.text.in_(["✅ Я согласен", "✅ Men roziman"]))
async def agreement_accepted(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await message.answer(langs[lang]["start_registration"], reply_markup=ReplyKeyboardRemove())
    await message.answer(langs[lang]["ask_full_name"])
    await state.set_state(RegisterState.full_name)

# 👤 Пример дальнейших шагов (регистрация)
@router.message(RegisterState.full_name)
async def get_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await message.answer(langs[lang]["ask_phone"])
    await state.set_state(RegisterState.phone)

# 🔘 Главное меню
@router.message(F.text.in_([langs["ru"]["menu"], langs["uz"]["menu"]]))
async def main_menu(message: Message, state: FSMContext):
    await message.answer("🔘 Меню")

# 👮‍♂️ Панель администратора
@router.message(F.text.in_([langs["ru"]["admin_panel"], langs["uz"]["admin_panel"]]))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("⛔️ У вас нет доступа")
    await message.answer("👮‍♂️ Добро пожаловать в админ-панель!")
