from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
import re

from app.messages import langs
from app.keyboards import get_main_menu, get_language_keyboard, get_agree_keyboard
from app.config import ADMINS
from app.database import (
    get_user_by_telegram_id,
    save_user,
    update_user_field
)

router = Router()


class RegisterState(StatesGroup):
    full_name = State()
    phone = State()
    birth_day = State()
    birth_month = State()
    birth_year = State()
    pinfl = State()


class EditFieldState(StatesGroup):
    choosing = State()
    editing = State()


def get_lang(state_data):
    return state_data.get("lang") if state_data.get("lang") in langs else "ru"


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    user_data = await get_user_by_telegram_id(message.from_user.id)
    if user_data:
        lang = "ru"
        await state.update_data(lang=lang)
        await message.answer("👋 Добро пожаловать обратно!", reply_markup=get_main_menu(lang))
    else:
        await message.answer(
            "🇷🇺 Пожалуйста, выберите язык / 🇺🇿 Iltimos, tilni tanlang",
            reply_markup=get_language_keyboard()
        )


@router.message(F.text.in_(["🇷🇺 Русский", "🇺🇿 O‘zbek"]))
async def select_language(message: Message, state: FSMContext):
    lang = "ru" if message.text == "🇷🇺 Русский" else "uz"
    await state.update_data(lang=lang)
    await message.answer(langs[lang]["warning_text"], reply_markup=get_agree_keyboard(lang))


@router.message(F.text.in_(["✅ Я согласен", "✅ Men roziman"]))
async def agreement_accepted(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = get_lang(data)
    await message.answer(langs[lang]["start_registration"], reply_markup=ReplyKeyboardRemove())
    await message.answer(langs[lang]["ask_full_name"])
    await state.set_state(RegisterState.full_name)


@router.message(RegisterState.full_name)
async def get_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    lang = get_lang(data)
    await message.answer(langs[lang]["ask_phone"])
    await state.set_state(RegisterState.phone)


@router.message(RegisterState.phone)
async def get_phone(message: Message, state: FSMContext):
    raw_input = message.text.strip()
    cleaned = re.sub(r"[^\d]", "", raw_input)
    if cleaned.startswith("998"):
        cleaned = cleaned[3:]
    if len(cleaned) != 9:
        return await message.answer("❌ Номер должен содержать ровно 9 цифр (без кода страны). Например: 991112233")
    phone = f"998{cleaned}"
    await state.update_data(phone=phone)
    data = await state.get_data()
    lang = get_lang(data)
    await message.answer(langs[lang]["ask_birth_day"])
    await state.set_state(RegisterState.birth_day)


@router.message(RegisterState.birth_day)
async def get_birth_day(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (1 <= int(message.text) <= 31):
        return await message.answer("❌ Введите число от 1 до 31.")
    await state.update_data(birth_day=int(message.text))
    data = await state.get_data()
    lang = get_lang(data)
    await message.answer(langs[lang]["ask_birth_month"])
    await state.set_state(RegisterState.birth_month)


@router.message(RegisterState.birth_month)
async def get_birth_month(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (1 <= int(message.text) <= 12):
        return await message.answer("❌ Введите число от 1 до 12.")
    await state.update_data(birth_month=int(message.text))
    data = await state.get_data()
    lang = get_lang(data)
    await message.answer(langs[lang]["ask_birth_year"])
    await state.set_state(RegisterState.birth_year)


@router.message(RegisterState.birth_year)
async def get_birth_year(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (1900 <= int(message.text) <= 2025):
        return await message.answer("❌ Введите корректный год рождения.")
    await state.update_data(birth_year=int(message.text))
    data = await state.get_data()
    lang = get_lang(data)
    day = f"{data['birth_day']:02d}"
    month = f"{data['birth_month']:02d}"
    year = f"{data['birth_year']}"
    birthday = f"{year}-{month}-{day}"
    await state.update_data(birthday=birthday)
    await message.answer(langs[lang]["ask_pinfl"])
    await state.set_state(RegisterState.pinfl)


@router.message(RegisterState.pinfl)
async def get_pinfl(message: Message, state: FSMContext):
    await state.update_data(pinfl=message.text)
    data = await state.get_data()
    lang = get_lang(data)
    await save_user(
        telegram_id=message.from_user.id,
        full_name=data["full_name"],
        phone=data["phone"],
        birthday=data["birthday"],
        pinfl=data["pinfl"]
    )
    await message.answer("✅ Данные сохранены! Спасибо за регистрацию.", reply_markup=get_main_menu(lang))
    await state.clear()


@router.message(F.text.in_([langs["ru"]["menu"], langs["uz"]["menu"]]))
async def main_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = get_lang(data)
    await message.answer(langs[lang]["menu"])


@router.message(F.text.in_([langs["ru"]["admin_panel"], langs["uz"]["admin_panel"]]))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("⛔️ У вас нет доступа")
    await message.answer("👮‍♂️ Добро пожаловать в админ-панель!")


@router.message(F.text.in_([langs["ru"]["main_menu_options"][-1], langs["uz"]["main_menu_options"][-1]]))
async def show_my_data(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = get_lang(data)
    user_data = await get_user_by_telegram_id(message.from_user.id)
    if not user_data:
        return await message.answer("⛔️ Данные не найдены")
    full_name, phone, birthday, pinfl = user_data
    await message.answer(
        f"📛 ФИО: {full_name}\n📞 Телефон: {phone}\n📅 Дата рождения: {birthday}\n🆔 ПИНФЛ: {pinfl}\n\n{langs[lang]['edit_data_prompt']}",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=field)] for field in ["ФИО", "Телефон", "Дата рождения", "ПИНФЛ"]] +
                     [[KeyboardButton(text=langs[lang]["cancel"])]],
            resize_keyboard=True
        )
    )
    await state.set_state(EditFieldState.choosing)


@router.message(EditFieldState.choosing)
async def choose_field_to_edit(message: Message, state: FSMContext):
    field_map = {
        "ФИО": "full_name", "Телефон": "phone", "Дата рождения": "birthday", "ПИНФЛ": "pinfl",
        "Ism": "full_name", "Telefon": "phone", "Tug‘ilgan sana": "birthday", "PINFL": "pinfl"
    }
    chosen = message.text
    if chosen not in field_map:
        return await message.answer("❌ Неверный выбор")
    await state.update_data(edit_field=field_map[chosen])
    await message.answer("✏️ Введите новое значение:")
    await state.set_state(EditFieldState.editing)


@router.message(EditFieldState.editing)
async def update_field_value(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get("edit_field")
    if not field:
        return await message.answer("⚠️ Ошибка. Поле не выбрано.")
    await update_user_field(message.from_user.id, field, message.text)
    lang = get_lang(data)
    await message.answer(langs[lang]["data_updated"], reply_markup=get_main_menu(lang))
    await state.clear()
