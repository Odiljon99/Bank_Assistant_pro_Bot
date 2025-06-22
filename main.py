import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_CHAT_ID"))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, storage=MemoryStorage())

# База данных
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

class Register(StatesGroup):
    language = State()
    full_name = State()
    phone = State()
    birth = State()
    pinfl = State()
    problem = State()

user_data = {}

# Языки
langs = {
    'ru': {
        'welcome': "Добро пожаловать в бот банковского помощника.",
        'menu': "📋 Главное меню:",
        'reg_done': "✅ Вы успешно зарегистрированы.",
        'send_full_name': "Введите ваше ФИО:",
        'send_phone': "Введите номер телефона:",
        'send_birth': "Введите дату рождения (ДД.ММ.ГГГГ):",
        'send_pinfl': "Введите ваш ПИНФЛ (14 цифр):\n🔍 Найти можно в паспорте или онлайн в приложении банка.",
        'change_lang': "🇷🇺 Сменить язык",
        'to_menu': "🔙 В меню",
        'send_problem': "Опишите вашу проблему:",
        'problem_sent': "✅ Ваша заявка отправлена. Ожидайте ответ.",
        'start_warning': "❗ Пожалуйста, не используйте бота ради шутки. Ваши действия отслеживаются.",
        'choose_lang': "Выберите язык / Tilni tanlang:"
    },
    'uz': {
        'welcome': "Bank yordamchi botiga xush kelibsiz.",
        'menu': "📋 Asosiy menyu:",
        'reg_done': "✅ Roʻyxatdan oʻtdingiz.",
        'send_full_name': "FISH ni kiriting:",
        'send_phone': "Telefon raqamingizni kiriting:",
        'send_birth': "Tug'ilgan sanangiz (KK.OY.YYYY):",
        'send_pinfl': "PINFL kiriting (14 raqam):\n🔍 Uni pasportda yoki bank ilovasida topishingiz mumkin.",
        'change_lang': "🇺🇿 Tilni o‘zgartirish",
        'to_menu': "🔙 Menyuga",
        'send_problem': "Muammoni yozing:",
        'problem_sent': "✅ So‘rovingiz yuborildi. Javobni kuting.",
        'start_warning': "❗ Iltimos, botdan hazil uchun foydalanmang. Harakatlaringiz nazorat qilinadi.",
        'choose_lang': "Выберите язык / Tilni tanlang:"
    }
}

# Старт
@dp.message_handler(commands="start")
async def start_cmd(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🇷🇺 Русский"), KeyboardButton("🇺🇿 O‘zbek"))
    await message.answer(langs['ru']['choose_lang'], reply_markup=markup)
    await Register.language.set()

# Выбор языка
@dp.message_handler(lambda msg: msg.text in ["🇷🇺 Русский", "🇺🇿 O‘zbek"], state=Register.language)
async def set_lang(message: types.Message, state: FSMContext):
    lang = 'ru' if "Рус" in message.text else 'uz'
    await state.update_data(lang=lang)
    await message.answer(langs[lang]['start_warning'])
    await message.answer(langs[lang]['send_full_name'], reply_markup=types.ReplyKeyboardRemove())
    await Register.full_name.set()

@dp.message_handler(state=Register.full_name)
async def full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer(langs[(await state.get_data())['lang']]['send_phone'])
    await Register.phone.set()

@dp.message_handler(state=Register.phone)
async def phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(langs[(await state.get_data())['lang']]['send_birth'])
    await Register.birth.set()

@dp.message_handler(state=Register.birth)
async def birth(message: types.Message, state: FSMContext):
    await state.update_data(birth=message.text)
    await message.answer(langs[(await state.get_data())['lang']]['send_pinfl'])
    await Register.pinfl.set()

@dp.message_handler(state=Register.pinfl)
async def pinfl(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['pinfl'] = message.text

    # Сохраняем в БД
    cursor.execute("REPLACE INTO users (user_id, full_name, phone, birth, pinfl, lang) VALUES (?, ?, ?, ?, ?, ?)", (
        message.from_user.id,
        data['full_name'],
        data['phone'],
        data['birth'],
        data['pinfl'],
        data['lang']
    ))
    conn.commit()

    # Меню
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add("📈 Кредитная история", "📊 Кредит калькулятор", "👤 Менеджер")
    menu.add(langs[data['lang']]['change_lang'], langs[data['lang']]['to_menu'])
    await message.answer(langs[data['lang']]['reg_done'], reply_markup=menu)
    await state.finish()

# Обработка меню
@dp.message_handler(Text(equals=["📈 Кредитная история", "📊 Кредит калькулятор", "👤 Менеджер"]))
async def menu(message: types.Message):
    text = message.text
    user = cursor.execute("SELECT * FROM users WHERE user_id = ?", (message.from_user.id,)).fetchone()
    lang = user[-1] if user else 'ru'

    if text == "📈 Кредитная история":
        await message.answer(langs[lang]['send_problem'])
        await Register.problem.set()
    elif text == "📊 Кредит калькулятор":
        await message.answer("👉 Запустить кредит калькулятор: @YOUR_CREDIT_BOT")
    elif text == "👤 Менеджер":
        await message.answer("✍️ Напишите вашу проблему, менеджер ответит в ближайшее время.")
        await Register.problem.set()

@dp.message_handler(state=Register.problem)
async def get_problem(message: types.Message, state: FSMContext):
    user = cursor.execute("SELECT * FROM users WHERE user_id = ?", (message.from_user.id,)).fetchone()
    lang = user[-1]
    text = message.text

    report = f"""📩 *Новая проблема от* @{message.from_user.username or message.from_user.full_name}

📝 _"{text}"_

⏳ Статус: Ожидает ответа"""

    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🔁 Ответить", callback_data=f"answer:{message.from_user.id}"),
        InlineKeyboardButton("✅ Завершить", callback_data=f"close:{message.from_user.id}")
    )

    sent = await bot.send_message(chat_id=GROUP_ID, text=report, reply_markup=markup)
    user_data[message.from_user.id] = {"msg_id": sent.message_id, "chat_id": sent.chat.id}

    await message.answer(langs[lang]['problem_sent'])
    await state.finish()

# Кнопки для сотрудников
@dp.callback_query_handler(Text(startswith="answer:"))
async def answer_problem(call: types.CallbackQuery):
    user_id = int(call.data.split(":")[1])
    await call.message.answer(f"📝 Введите ответ для @{user_id}")
    await call.answer()

@dp.callback_query_handler(Text(startswith="close:"))
async def close_problem(call: types.CallbackQuery):
    user_id = int(call.data.split(":")[1])
    data = user_data.get(user_id)
    if data:
        await bot.edit_message_text(
            chat_id=data["chat_id"],
            message_id=data["msg_id"],
            text=call.message.text.replace("⏳ Статус: Ожидает ответа", f"✅ Статус: Завершено\n👤 Ответил: @{call.from_user.username}")
        )
    await call.answer("Заявка завершена.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
