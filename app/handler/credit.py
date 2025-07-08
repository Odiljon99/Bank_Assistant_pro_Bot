from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from app.database import get_user_by_telegram_id
from app.messages import langs, get_lang_safe
from app.config import ADMINS

router = Router()

STAFF_GROUP_ID = -1002551245369  # Убедись, что бот админ в этой группе

def get_credit_request_buttons(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✍️ Ответить", callback_data=f"reply_to_client:{user_id}"),
                InlineKeyboardButton(text="✅ Завершить", callback_data=f"finish_request:{user_id}")
            ]
        ]
    )

@router.message(F.text.in_([
    langs["ru"]["main_menu_options"][0],
    langs["uz"]["main_menu_options"][0]
]))
async def request_credit_history(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user["lang"] if user else "ru"
    texts = get_lang_safe(lang)

    from app.keyboards import get_credit_history_agree_keyboard
    await message.answer(
        texts["send_data_consent"],
        reply_markup=get_credit_history_agree_keyboard(lang)
    )

@router.callback_query(F.data == "agree_send_data")
async def send_credit_request(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = await get_user_by_telegram_id(user_id)
    if not user_data:
        return await callback.message.answer("⛔️ Данные не найдены")

    lang = user_data.get("lang", "ru")
    texts = get_lang_safe(lang)

    full_name = user_data.get("full_name", "-")
    phone = user_data.get("phone", "-")
    birthday = user_data.get("birthday", "-")
    pinfl = user_data.get("pinfl", "-")

    text = (
        f"✉️ {texts['new_report']}\n"
        f"<b>ФИО:</b> {full_name}\n"
        f"<b>Телефон:</b> {phone}\n"
        f"<b>Дата рождения:</b> {birthday}\n"
        f"<b>ПИНФЛ:</b> {pinfl}"
    )

    await callback.answer("✉️ " + texts["data_sent_to_staff"])
    await callback.message.answer("✉️ " + texts["data_sent_to_staff"])

    await callback.bot.send_message(
        STAFF_GROUP_ID,
        text,
        reply_markup=get_credit_request_buttons(user_id),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("reply_to_client:"))
async def reply_to_client(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(":")[1])
    await state.update_data(reply_target=user_id)
    await callback.message.answer("📝 Напишите свой ответ для клиента")
    await callback.answer()

@router.message(F.from_user.id.in_(ADMINS))
async def collect_reply_for_client(message: Message, state: FSMContext):
    data = await state.get_data()
    target_id = data.get("reply_target")
    if not target_id:
        return
    await message.bot.send_message(target_id, f"📢 Ответ от менеджера:\n{message.text}")
    await state.update_data(reply_target=None)

@router.callback_query(F.data.startswith("finish_request:"))
async def finish_request(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(":")[1])
    user_data = await get_user_by_telegram_id(user_id)
    lang = user_data.get("lang", "ru") if user_data else "ru"
    texts = get_lang_safe(lang)

    await callback.bot.send_message(user_id, "✅ " + texts["complete"] + " " + texts["menu"])
    await callback.message.edit_reply_markup()
    await callback.answer("✅ " + texts["complete"])
