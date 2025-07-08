from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.keyboards import (
    get_main_menu,
    get_edit_data_menu,
    get_back_keyboard,
)
from app.database import get_user_by_telegram_id, update_user_field
from app.messages import get_lang_safe

router = Router()

# Состояния для редактирования
class EditFieldState(StatesGroup):
    choosing_field = State()
    editing_value = State()

# ====== Пункт 5: Мои данные ======

@router.message(F.text.in_(["🗂 Мои данные", "🗂 Ma’lumotlarim"]))
async def edit_data_start(message: Message, state: FSMContext):
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
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    if field:
        await state.update_data(field=field)
        await state.set_state(EditFieldState.editing_value)
        await message.answer(texts["enter_new_value"], reply_markup=get_back_keyboard(lang))
    else:
        await message.answer("❗️ Неверный выбор")


@router.message(EditFieldState.editing_value)
async def process_field_editing(message: Message, state: FSMContext):
    value = message.text.strip()
    data = await state.get_data()
    field = data.get("field")

    await update_user_field(message.from_user.id, field, value)

    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    await state.clear()
    await message.answer(texts["data_updated"], reply_markup=get_main_menu(lang))


# ====== Назад из "Мои данные" ======

@router.message(EditFieldState.choosing_field, F.text.in_(["🔙 Назад", "🔙 Orqaga"]))
@router.message(EditFieldState.editing_value, F.text.in_(["🔙 Назад", "🔙 Orqaga"]))
async def go_back_from_editing(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    await state.clear()
    await message.answer(texts["menu"], reply_markup=get_main_menu(lang))
