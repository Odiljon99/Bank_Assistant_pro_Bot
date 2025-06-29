from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from app.database import get_user_by_telegram_id
from app.messages import langs
from app.keyboards import get_credit_history_agree_keyboard

router = Router()
STAFF_GROUP_ID = -4813065675

# Временное хранилище заявок
requests_cache = {}

def get_credit_request_buttons(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✍️ Ответить", callback_data=f"reply_to_client:{user_id}"),
                InlineKeyboardButton(text="✅ Завершить", callback_data=f"finish_request:{user_id}")
            ]
        ]
    )

# 📊 Узнать кредитную историю
@router.message(F.text == "📊 Узнать кредитную историю")
async def request_credit_history(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await message.answer(
        (
            "Чтобы узнать вашу кредитную историю, мы должны отправить ваши данные менеджеру. Вы согласны?"
            if lang == "ru"
            else "Kredit tarixingizni bilish uchun biz ma‘lumotlaringizni menejerga yuborishimiz kerak. Rozimisiz?"
        ),
        reply_markup=get_credit_history_agree_keyboard(lang)
    )

# 📤 Согласие на отправку данных
@router.callback_query(F.data == "agree_send_data")
async def send_credit_request(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_by_telegram_id(user_id)

    if not user_data:
        return await callback.message.answer("⛔️ Данные не найдены")

    full_name, phone, birthday, pinfl = user_data
    text = (
        f"✉️ <b>Новая заявка на кредитную историю</b>\n\n"
        f"<b>ФИО:</b> {full_name}\n"
        f"<b>Телефон:</b> {phone}\n"
        f"<b>Дата рождения:</b> {birthday}\n"
        f"<b>ПИНФЛ:</b> {pinfl}"
    )

    await callback.answer("✉️ Данные отправлены")
    await callback.message.answer("✉️ Заявка отправлена, ожидайте ответа")

    await callback.bot.send_message(
        STAFF_GROUP_ID,
        text,
        reply_markup=get_credit_request_buttons(user_id),
        parse_mode="HTML"
    )

# 📝 Ответить клиенту
@router.callback_query(F.data.startswith("reply_to_client:"))
async def reply_to_client(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(":")[1])
    await state.update_data(reply_target=user_id)
    await callback.message.answer("📝 Напишите свой ответ для клиента")
    await callback.answer("Введите сообщение")

# 📬 Получение ответа от менеджера
@router.message(F.text)
async def handle_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    target_id = data.get("reply_target")

    if target_id:
        await message.bot.send_message(target_id, f"📢 Ответ от менеджера:\n\n{message.text}")
        await message.answer("✅ Ответ отправлен клиенту.")
        await state.update_data(reply_target=None)

# ✅ Завершить заявку
@router.callback_query(F.data.startswith("finish_request:"))
async def finish_request(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])

    await callback.bot.send_message(
        user_id,
        "✅ Заявка завершена. Если у вас будут еще вопросы, обращайтесь!"
    )
    await callback.message.edit_reply_markup()
    await callback.answer("✅ Заявка помечена как завершённая.")
