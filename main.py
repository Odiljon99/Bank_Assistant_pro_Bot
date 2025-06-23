import asyncio
import logging
import sqlite3
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties  # ВАЖНО
from dotenv import load_dotenv
from aiogram.filters import CommandStart

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_CHAT_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)  # <-- вот правильный способ
)
dp = Dispatcher(storage=MemoryStorage())

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT,
    phone TEXT,
    birth TEXT,
    pinfl TEXT,
    lang TEXT
)
""")
conn.commit()

langs = {
    'ru': {
        'choose_lang': "Выберите язык / Tilni tanlang:",
        'start_warning': "❗ Не шутите, действия отслеживаются.",
        'send_full_name': "Введите ФИО:",
        'send_phone': "Введите номер телефона:",
        'send_birth': "Введите дату рождения (ДД.ММ.ГГГГ):",
        'send_pinfl': "Введите ПИНФЛ (14 цифр):",
        'reg_done': "✅ Зарегистрированы",
        'menu': "📋 Главное меню:",
        'credit_history': "📈 Кредитная история",
        'credit_calc': "📊 Кредит калькулятор",
        'manager': "👤 Менеджер",
        'my_data': "📁 Мои данные",
        'change_lang': "🌐 Сменить язык",
        'back': "🔙 Назад",
        'main_menu': "🏠 Меню",
        'send_problem': "Опишите проблему:",
        'problem_sent': "✅ Заявка отправлена"
    },
    'uz': {
        'choose_lang': "Выберите язык / Tilni tanlang:",
        'start_warning': "❗ Iltimos, hazillashmang.",
        'send_full_name': "FIO kiriting:",
        'send_phone': "Telefon raqam:",
        'send_birth': "Tug'ilgan sana (KK.OY.YYYY):",
        'send_pinfl': "PINFL (14 raqam):",
        'reg_done': "✅ Ro‘yxatdan o‘tildi",
        'menu': "📋 Asosiy menyu:",
        'credit_history': "📈 Kredit tarixi",
        'credit_calc': "📊 Kredit kalkulyatori",
        'manager': "👤 Menejer",
        'my_data': "📁 Mening ma’lumotlarim",
        'change_lang': "🌐 Tilni o‘zgartirish",
        'back': "🔙 Orqaga",
        'main_menu': "🏠 Menyu",
        'send_problem': "Muammoni yozing:",
        'problem_sent': "✅ So‘rov yuborildi"
    }
}

class Register(StatesGroup):
    language = State()
    full_name = State()
    phone = State()
    birth = State()
    pinfl = State()
    problem = State()

user_data = {}

def menu_kb(lang: str):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(langs[lang]['credit_history'], langs[lang]['credit_calc'])
    kb.add(langs[lang]['manager'], langs[lang]['my_data'])
    kb.add(langs[lang]['change_lang'], langs[lang]['main_menu'])
    return kb

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🇷🇺 Русский", "🇺🇿 O‘zbek")
    await message.answer(langs['ru']['choose_lang'], reply_markup=kb)
    await state.set_state(Register.language)

@dp.message(Register.language, F.text.in_(["🇷🇺 Русский", "🇺🇿 O‘zbek"]))
async def set_language(message: Message, state: FSMContext):
    lang = 'ru' if "Рус" in message.text else 'uz'
    await state.update_data(lang=lang)
    await message.answer(langs[lang]['start_warning'], reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(langs[lang]['back']))
    await message.answer(langs[lang]['send_full_name'])
    await state.set_state(Register.full_name)

@dp.message(Register.full_name)
async def set_fullname(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == langs[data['lang']]['back']:
        return await cmd_start(message, state)
    await state.update_data(full_name=message.text)
    await message.answer(langs[data['lang']]['send_phone'], reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(langs[data['lang']]['back']))
    await state.set_state(Register.phone)

@dp.message(Register.phone)
async def set_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == langs[data['lang']]['back']:
        return await set_fullname(message, state)
    await state.update_data(phone=message.text)
    await message.answer(langs[data['lang']]['send_birth'], reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(langs[data['lang']]['back']))
    await state.set_state(Register.birth)

@dp.message(Register.birth)
async def set_birth(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == langs[data['lang']]['back']:
        return await set_phone(message, state)
    await state.update_data(birth=message.text)
    await message.answer(langs[data['lang']]['send_pinfl'], reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(langs[data['lang']]['back']))
    await state.set_state(Register.pinfl)

@dp.message(Register.pinfl)
async def set_pinfl(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == langs[data['lang']]['back']:
        return await set_birth(message, state)
    await state.update_data(pinfl=message.text)
    data = await state.get_data()
    cursor.execute("REPLACE INTO users VALUES (?,?,?,?,?,?)", (
        message.from_user.id, data['full_name'], data['phone'], data['birth'], data['pinfl'], data['lang']
    ))
    conn.commit()
    await message.answer(langs[data['lang']]['reg_done'], reply_markup=menu_kb(data['lang']))
    await state.clear()

@dp.message(F.text.in_([langs['ru']['my_data'], langs['uz']['my_data']]))
async def my_data(message: Message):
    user = cursor.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,)).fetchone()
    lang = user[-1]
    text = f"👤 {user[1]}\n📞 {user[2]}\n🎂 {user[3]}\n🆔 {user[4]}"
    await message.answer(text, reply_markup=menu_kb(lang))

@dp.message(F.text.in_([langs['ru']['change_lang'], langs['uz']['change_lang']]))
async def change_lang(message: Message, state: FSMContext):
    return await cmd_start(message, state)

@dp.message(F.text.in_([langs['ru']['main_menu'], langs['uz']['main_menu']]))
async def to_menu(message: Message):
    user = cursor.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,)).fetchone()
    lang = user[-1]
    await message.answer(langs[lang]['menu'], reply_markup=menu_kb(lang))

@dp.message(F.text.in_([langs['ru']['credit_history'], langs['uz']['credit_history'], langs['ru']['manager'], langs['uz']['manager']]))
async def start_problem(message: Message, state: FSMContext):
    user = cursor.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,)).fetchone()
    lang = user[-1]
    await message.answer(langs[lang]['send_problem'], reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(langs[lang]['back'], langs[lang]['main_menu']))
    await state.set_state(Register.problem)

@dp.message(Register.problem)
async def handle_problem(message: Message, state: FSMContext):
    data = cursor.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,)).fetchone()
    lang = data[-1]
    text = message.text
    report = (f"📩 *Новая проблема от* @{message.from_user.username or message.from_user.full_name}\n\n"
              f"📝 _\"{text}\"_\n\n⏳ Статус: Ожидает ответа")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("🔁 Ответить", callback_data=f"answer:{message.from_user.id}")],
        [InlineKeyboardButton("✅ Завершить", callback_data=f"close:{message.from_user.id}")]
    ])
    sent = await bot.send_message(chat_id=GROUP_ID, text=report, reply_markup=markup)
    user_data[message.from_user.id] = {"chat_id": sent.chat.id, "msg_id": sent.message_id}
    await message.answer(langs[lang]['problem_sent'], reply_markup=menu_kb(lang))
    await state.clear()

@dp.callback_query(F.data.startswith("answer:"))
async def answer_query(call: CallbackQuery):
    uid = int(call.data.split(":")[1])
    await call.message.answer("📝 Введите ответ:")
    await call.answer()
    user_data['answer_for'] = uid

@dp.message(lambda m: 'answer_for' in user_data)
async def send_answer(message: Message):
    uid = user_data.pop('answer_for')
    reply = message.text
    data = user_data.get(uid)
    await bot.send_message(chat_id=uid, text=reply)
    await bot.edit_message_text(chat_id=data['chat_id'], message_id=data['msg_id'],
                                text=(message.reply_to_message.text + f"\n✅ Статус: Ответ отправлен\n👤 Ответил: @{message.from_user.username}"))
    await message.answer("Ответ отправлен.", reply_markup=menu_kb(langs[cursor.execute("SELECT lang FROM users WHERE user_id=?", (message.from_user.id,)).fetchone()[0]]))

@dp.callback_query(F.data.startswith("close:"))
async def close_query(call: CallbackQuery):
    uid = int(call.data.split(":")[1])
    data = user_data.get(uid)
    await bot.edit_message_text(chat_id=data['chat_id'], message_id=data['msg_id'],
                                text=(call.message.text.replace("⏳ Статус: Ожидает ответа", f"✅ Статус: Завершено\n👤 Ответил: @{call.from_user.username}")))
    await call.answer("Заявка закрыта.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
