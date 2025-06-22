# ✅ Финальный main.py (часть 2): Главное меню, заявка в группу, inline-кнопки, ответы

import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton, Message)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart, Text
from datetime import datetime
import os
from config import BOT_TOKEN, GROUP_CHAT_ID

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect("data.db")
c = conn.cursor()

class Reg(StatesGroup):
    language = State()
    full_name = State()
    phone = State()
    passport = State()
    birth_date = State()
    pinfl = State()

class Problem(StatesGroup):
    entering = State()
    awaiting_reply = State()

client_last_message = {}

@dp.message(Text(startswith="3️⃣"))
async def handle_problem_request(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    text = "✍️ Опишите вашу проблему одним сообщением:" if lang == 'ru' else "✍️ Muammoni yozing, iltimos."
    await message.answer(text)
    await state.set_state(Problem.entering)

@dp.message(Problem.entering)
async def collect_problem(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or f"id{user_id}"
    problem_text = message.text

    c.execute("SELECT full_name, phone, passport, birth_date, pinfl FROM clients WHERE telegram_id = ?", (user_id,))
    data = c.fetchone()
    full_name, phone, passport, birth_date, pinfl = data

    now = datetime.now().strftime("%d.%m.%Y, %H:%M")

    c.execute("INSERT INTO requests (request_type, full_name, phone, passport, birth_date, pinfl, telegram_id, problem, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              ("manager_help", full_name, phone, passport, birth_date, pinfl, user_id, problem_text, now))
    conn.commit()

    request_id = c.lastrowid

    text = f"📩 *Заявка от* @{username}
🕒 {now}

❓ _"{problem_text}"_

🔘 [Ответить] 🔘 [Закрыть заявку]"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Ответить", callback_data=f"reply_{request_id}"),
         InlineKeyboardButton(text="✅ Закрыть заявку", callback_data=f"close_{request_id}")]
    ])
    sent = await bot.send_message(GROUP_CHAT_ID, text, reply_markup=keyboard)

    client_last_message[request_id] = (user_id, sent.message_id)
    await message.answer("✅ Ваша проблема отправлена. Ожидайте ответа от сотрудников.")
    await state.clear()

@dp.callback_query(F.data.startswith("reply_"))
async def handle_reply_callback(callback: types.CallbackQuery, state: FSMContext):
    request_id = int(callback.data.split("_")[1])
    await state.update_data(request_id=request_id, group_message_id=callback.message.message_id)
    await bot.send_message(callback.from_user.id, "✍️ Введите ответ на проблему:")
    await state.set_state(Problem.awaiting_reply)
    await callback.answer()

@dp.message(Problem.awaiting_reply)
async def receive_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    request_id = data['request_id']
    group_message_id = data['group_message_id']

    username = message.from_user.username or f"id{message.from_user.id}"
    answer_text = message.text

    c.execute("UPDATE requests SET response = ? WHERE id = ?", (answer_text, request_id))
    conn.commit()

    user_id, _ = client_last_message.get(request_id, (None, None))
    if user_id:
        await bot.send_message(user_id, f"💬 @{username}: _{answer_text}_")

    c.execute("SELECT problem FROM requests WHERE id = ?", (request_id,))
    problem_text = c.fetchone()[0]
    now = datetime.now().strftime("%d.%m.%Y, %H:%M")
    new_text = f"📩 *Заявка от* @{get_username(user_id)}
🕒 {now}

❓ _"{problem_text}"_

💬 @{username}: _{answer_text}_

✅ Статус: Отвечено"
    await bot.edit_message_text(new_text, GROUP_CHAT_ID, group_message_id)
    await state.clear()

@dp.callback_query(F.data.startswith("close_"))
async def handle_close(callback: types.CallbackQuery):
    request_id = int(callback.data.split("_")[1])
    c.execute("SELECT problem, telegram_id FROM requests WHERE id = ?", (request_id,))
    row = c.fetchone()
    if row:
        problem, user_id = row
        now = datetime.now().strftime("%d.%m.%Y, %H:%M")
        new_text = f"📩 *Заявка от* @{get_username(user_id)}
🕒 {now}

❓ _"{problem}"_

✅ Статус: Завершено"
        await bot.edit_message_text(new_text, GROUP_CHAT_ID, callback.message.message_id)
    await callback.answer("Заявка закрыта")

def get_user_lang(user_id):
    c.execute("SELECT lang FROM clients WHERE telegram_id = ?", (user_id,))
    row = c.fetchone()
    return row[0] if row else 'ru'

def get_username(user_id):
    try:
        user = asyncio.run(bot.get_chat(user_id))
        return user.username or f"id{user_id}"
    except:
        return f"id{user_id}"

if __name__ == '__main__':
    import asyncio
    asyncio.run(dp.start_polling(bot))