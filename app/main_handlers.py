from aiogram import Router, F 
from aiogram.types import Message 
from aiogram.fsm.context import FSMContext 
from aiogram.fsm.state import StatesGroup, State

from app.keyboards import ( get_language_keyboard, get_main_menu, get_edit_data_menu, get_back_keyboard, ) 
from app.database import save_user, get_user_by_telegram_id, update_user_field, save_partial_user 
from app.messages import get_lang_safe

import re

router = Router()

=== СТЕЙТЫ ===

class RegisterState(StatesGroup): waiting_for_full_name = State() waiting_for_phone = State() waiting_for_birthday = State() waiting_for_pinfl = State()

class EditFieldState(StatesGroup): choosing_field = State() editing_value = State()

=== /start ===

@router.message(F.text == "/start") async def cmd_start(message: Message, state: FSMContext): await state.clear() await message.answer("\ud83c\uddf7\ud83c\uddfa \u041f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430, \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u044f\u0437\u044b\u043a\n\ud83c\uddfa\ud83c\uddff Iltimos, tilni tanlang", reply_markup=get_language_keyboard())

@router.message(F.text.in_(["\ud83c\uddf7\ud83c\uddfa \u0420\u0443\u0441\u0441\u043a\u0438\u0439", "\ud83c\uddfa\ud83c\uddff O\u02bbzbek"])) async def set_language(message: Message, state: FSMContext): lang = "ru" if message.text == "\ud83c\uddf7\ud83c\uddfa \u0420\u0443\u0441\u0441\u043a\u0438\u0439" else "uz" user = await get_user_by_telegram_id(message.from_user.id)

if user:
    await update_user_field(message.from_user.id, "lang", lang)
else:
    await save_partial_user(message.from_user.id, lang)

await state.clear()
texts = get_lang_safe(lang)
await message.answer(texts["menu"], reply_markup=get_main_menu(lang))

=== Регистрация ===

@router.message(F.text.in_(["\ud83d\udccb \u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f", "\ud83d\udccb Ro‘yxatdan o‘tish"])) async def register_start(message: Message, state: FSMContext): user = await get_user_by_telegram_id(message.from_user.id) lang = user.get("lang", "ru") if user else "ru" texts = get_lang_safe(lang)

await state.set_state(RegisterState.waiting_for_full_name)
await message.answer(texts["full_name"], reply_markup=get_back_keyboard(lang))

@router.message(RegisterState.waiting_for_full_name) async def process_full_name(message: Message, state: FSMContext): await state.update_data(full_name=message.text.strip()) user = await get_user_by_telegram_id(message.from_user.id) lang = user.get("lang", "ru") if user else "ru" texts = get_lang_safe(lang)

await state.set_state(RegisterState.waiting_for_phone)
await message.answer(texts["phone"], reply_markup=get_back_keyboard(lang))

@router.message(RegisterState.waiting_for_phone) async def process_phone(message: Message, state: FSMContext): phone = message.text.strip() user = await get_user_by_telegram_id(message.from_user.id) lang = user.get("lang", "ru") if user else "ru" texts = get_lang_safe(lang)

if not re.match(r"^\+?\d{9,15}$", phone):
    await message.answer(texts["invalid_phone"])
    return

await state.update_data(phone=phone)
await state.set_state(RegisterState.waiting_for_birthday)
await message.answer(texts["birthday"], reply_markup=get_back_keyboard(lang))

@router.message(RegisterState.waiting_for_birthday) async def process_birthday(message: Message, state: FSMContext): await state.update_data(birthday=message.text.strip()) user = await get_user_by_telegram_id(message.from_user.id) lang = user.get("lang", "ru") if user else "ru" texts = get_lang_safe(lang)

await state.set_state(RegisterState.waiting_for_pinfl)
await message.answer(texts["pinfl"], reply_markup=get_back_keyboard(lang))

@router.message(RegisterState.waiting_for_pinfl) async def process_pinfl(message: Message, state: FSMContext): pinfl = message.text.strip() data = await state.get_data() user = await get_user_by_telegram_id(message.from_user.id) lang = user.get("lang", "ru") if user else "ru" texts = get_lang_safe(lang)

await save_user(
    telegram_id=message.from_user.id,
    full_name=data["full_name"],
    phone=data["phone"],
    birthday=data["birthday"],
    pinfl=pinfl,
    lang=lang
)

await state.clear()
await message.answer(texts["saved"], reply_markup=get_main_menu(lang))

=== Мои данные ===

@router.message(F.text.in_(["\u270f\ufe0f \u041c\u043e\u0438 \u0434\u0430\u043d\u043d\u044b\u0435", "\u270f\ufe0f Ma’lumotlarim"])) async def edit_data(message: Message, state: FSMContext): user = await get_user_by_telegram_id(message.from_user.id) lang = user.get("lang", "ru") if user else "ru" texts = get_lang_safe(lang)

await state.set_state(EditFieldState.choosing_field)
await message.answer(texts["choose_field"], reply_markup=get_edit_data_menu(lang))

@router.message(EditFieldState.choosing_field) async def choose_field_to_edit(message: Message, state: FSMContext): field_map = { "\ud83d\udcdb \u0424\u0418\u041e": "full_name", "\ud83d\udcde \u0422\u0435\u043b\u0435\u0444\u043e\u043d": "phone", "\ud83d\udcc5 \u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f": "birthday", "\ud83c\udd94 \u041f\u0418\u041d\u0424\u041b": "pinfl", "\ud83d\udcdb Ism sharifi": "full_name", "\ud83d\udcde Telefon": "phone", "\ud83d\udcc5 Tug\u2018ilgan sana": "birthday", "\ud83c\udd94 JSHSHIR": "pinfl" }

field = field_map.get(message.text)
if not field:
    await message.answer("\u2757 \u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u0432\u044b\u0431\u043e\u0440")
    return

await state.update_data(field=field)
user = await get_user_by_telegram_id(message.from_user.id)
lang = user.get("lang", "ru") if user else "ru"
texts = get_lang_safe(lang)

await state.set_state(EditFieldState.editing_value)
await message.answer(texts["enter_new_value"], reply_markup=get_back_keyboard(lang))

@router.message(EditFieldState.editing_value) async def edit_value(message: Message, state: FSMContext): value = message.text.strip() data = await state.get_data() field = data["field"]

await update_user_field(message.from_user.id, field, value)
user = await get_user_by_telegram_id(message.from_user.id)
lang = user.get("lang", "ru") if user else "ru"
texts = get_lang_safe(lang)

await state.clear()
await message.answer(texts["data_updated"], reply_markup=get_main_menu(lang))

=== Назад ===

@router.message(F.text.in_(["\ud83d\udd19 \u041d\u0430\u0437\u0430\u0434", "\ud83d\udd19 Orqaga"])) async def go_back(message: Message, state: FSMContext): user = await get_user_by_telegram_id(message.from_user.id) lang = user.get("lang", "ru") if user else "ru" texts = get_lang_safe(lang)

await state.clear()
await message.answer(texts["menu"], reply_markup=get_main_menu(lang))

                            
