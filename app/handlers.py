from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.messages import langs
from app.keyboards import get_main_menu, get_language_keyboard, get_agree_keyboard, get_calendar_keyboard
from app.config import ADMINS
from aiogram.fsm.state import StatesGroup, State
import re

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
        reply_markup=get_agree_keyboard(lang)
    )

# ⚠️ Подтверждение согласия
@router.message(F.text.in_(["✅ Я согласен", "✅ Men roziman"]))
async def agreement_accepted(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await message.answer(langs[lang]["start_registration"], reply_markup=ReplyKeyboardRemove())
    await message.answer(langs[lang]["ask_full_name"])
    await state.set_state(RegisterState.full_name)

# 👤 ФИО
@router.message(RegisterState.full_name)
async def get_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await message.answer("📞 Введите номер телефона (например: 991112233)")
    await state.set_state(RegisterState.phone)

# 📞 Телефон
@router.message(RegisterState.phone)
async def get_phone(message: Message, state: FSMContext):
    phone_raw = message.text.strip()
    if not re.fullmatch(r"\d{9}", phone_raw):
        return await message.answer("❌ Номер должен содержать ровно 9 цифр, например: 991112233")

    phone = f"998{phone_raw}"
    await state.update_data(phone=phone)
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await message.answer("📅 Пожалуйста, выберите дату рождения:", reply_markup=get_calendar_keyboard())
    await state.set_state(RegisterState.birthday)

# 📅 Дата рождения (инлайн-календарь)
@router.callback_query(RegisterState.birthday)
async def process_calendar(callback: CallbackQuery, state: FSMContext):
    selected_date = callback.data.split(":")[-1]  # calendar:YYYY-MM-DD → YYYY-MM-DD
    await callback.message.delete_reply_markup()
    await state.update_data(birthday=selected_date)
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await callback.message.answer(langs[lang]["ask_pinfl"])
    await state.set_state(RegisterState.pinfl)
    await callback.answer()

# 🆔 ПИНФЛ + Сохранение в БД
@router.message(RegisterState.pinfl)
async def get_pinfl(message: Message, state: FSMContext):
    await state.update_data(pinfl=message.text)
    data = await state.get_data()
    lang = data.get("lang", "ru")

    from app.database import cursor, conn
    cursor.execute(
        "INSERT INTO users (telegram_id, full_name, phone, birthday, pinfl) VALUES (?, ?, ?, ?, ?)",
        (message.from_user.id, data["full_name"], data["phone"], data["birthday"], data["pinfl"])
    )
    conn.commit()

    await message.answer("✅ Данные сохранены! Спасибо за регистрацию.", reply_markup=get_main_menu(lang))
    await state.clear()

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
