from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from app.keyboards import (
    get_language_keyboard,
    get_main_menu,
    get_edit_data_menu,
    get_back_keyboard,
)
from app.database import save_user, get_user_by_telegram_id, update_user_field
from app.messages import get_lang_safe

import re

router = Router()

# ====== СТЕЙТЫ ======

class RegisterState(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_phone = State()
    waiting_for_birthday = State()
    waiting_for_pinfl = State()


class EditFieldState(StatesGroup):
    choosing_field = State()
    editing_value = State()


# ====== СТАРТ ======

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🇷🇺 Пожалуйста, выберите язык\n🇺🇿 Iltimos, tilni tanlang", reply_markup=get_language_keyboard())


@router.message(F.text.in_(["🇷🇺 Русский", "🇺🇿 O‘zbek"]))
async def set_language(message: Message, state: FSMContext):
    lang = "ru" if message.text == "🇷🇺 Русский" else "uz"
    user = await get_user_by_telegram_id(message.from_user.id)

    if user:
        await update_user_field(message.from_user.id, "lang", lang)
    else:
        await save_user(telegram_id=message.from_user.id, lang=lang)

    await state.clear()
    texts = get_lang_safe(lang)
    await message.answer(texts["menu"], reply_markup=get_main_menu(lang))


# ====== ГЛАВНОЕ МЕНЮ ======

@router.message(F.text.in_(["📋 Регистрация", "📋 Ro‘yxatdan o‘tish"]))
async def register_start(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    await state.set_state(RegisterState.waiting_for_full_name)
    await message.answer(texts["full_name"], reply_markup=get_back_keyboard(lang))


@router.message(RegisterState.waiting_for_full_name)
async def process_full_name(message: Message, state: FSMContext):
    full_name = message.text.strip()
    await state.update_data(full_name=full_name)
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    await state.set_state(RegisterState.waiting_for_phone)
    await message.answer(texts["phone"], reply_markup=get_back_keyboard(lang))


@router.message(RegisterState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not re.match(r"^\+?\d{9,15}$", phone):
        user = await get_user_by_telegram_id(message.from_user.id)
        lang = user["lang"] if user else "ru"
        texts = get_lang_safe(lang)
        await message.answer(texts["invalid_phone"])
        return

    await state.update_data(phone=phone)
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    await state.set_state(RegisterState.waiting_for_birthday)
    await message.answer(texts["birthday"], reply_markup=get_back_keyboard(lang))


@router.message(RegisterState.waiting_for_birthday)
async def process_birthday(message: Message, state: FSMContext):
    birthday = message.text.strip()
    await state.update_data(birthday=birthday)
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    await state.set_state(RegisterState.waiting_for_pinfl)
    await message.answer(texts["pinfl"], reply_markup=get_back_keyboard(lang))


@router.message(RegisterState.waiting_for_pinfl)
async def process_pinfl(message: Message, state: FSMContext):
    pinfl = message.text.strip()
    data = await state.get_data()
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    await save_user(
        telegram_id=message.from_user.id,
        full_name=data["full_name"],
        phone=data["phone"],
        birthday=data["birthday"],
        pinfl=pinfl,
        lang=lang,
    )

    await state.clear()
    await message.answer(texts["saved"], reply_markup=get_main_menu(lang))


# ====== ИЗМЕНЕНИЕ ДАННЫХ ======

@router.message(F.text.in_(["✏️ Изменить данные", "✏️ Maʼlumotlarni o‘zgartirish"]))
async def edit_data(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    await state.set_state(EditFieldState.choosing_field)
    await message.answer(texts["choose_field"], reply_markup=get_edit_data_menu(lang))


@router.message(EditFieldState.choosing_field)
async def choose_field_to_edit(message: Message, state: FSMContext):
    field_map = {
        "📛 ФИО": "full_name",
        "📱 Телефон": "phone",
        "🎂 Дата рождения": "birthday",
        "🆔 ПИНФЛ": "pinfl",
        "📛 Ism sharifi": "full_name",
        "📱 Telefon": "phone",
        "🎂 Tug‘ilgan sana": "birthday",
        "🆔 JSHSHIR": "pinfl",
    }

    field = field_map.get(message.text)
    if field:
        await state.update_data(field=field)
        user = await get_user_by_telegram_id(message.from_user.id)
        lang = user["lang"] if user else "ru"
        texts = get_lang_safe(lang)

        await state.set_state(EditFieldState.editing_value)
        await message.answer(texts["enter_new_value"], reply_markup=get_back_keyboard(lang))
    else:
        await message.answer("❗ Неверный выбор")


@router.message(EditFieldState.editing_value)
async def edit_value(message: Message, state: FSMContext):
    value = message.text.strip()
    data = await state.get_data()
    field = data["field"]
    await update_user_field(message.from_user.id, field, value)

    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    await state.clear()
    await message.answer(texts["data_updated"], reply_markup=get_main_menu(lang))


# ====== НАЗАД ======

@router.message(F.text.in_(["🔙 Назад", "🔙 Orqaga"]))
async def go_back(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    await state.clear()
    await message.answer(texts["menu"], reply_markup=get_main_menu(lang))
