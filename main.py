# ✅ main.py — финальная версия (aiogram 2.25.2, Render-ready)
# Включает: регистрацию, меню, выбор языка, мои данные, назад, обращения и ответы

# 📦 Импорты
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import logging, sqlite3, os
from datetime import datetime

# 📁 Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)
db = sqlite3.connect("data.db")
c = db.cursor()

# 📊 База данных
c.execute("""CREATE TABLE IF NOT EXISTS clients (
    telegram_id INTEGER PRIMARY KEY,
    lang TEXT,
    full_name TEXT,
    phone TEXT,
    passport TEXT,
    birth_date TEXT,
    pinfl TEXT
)""")
c.execute("""CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    request_type TEXT,
    full_name TEXT,
    phone TEXT,
    passport TEXT,
    birth_date TEXT,
    pinfl TEXT,
    problem TEXT,
    response TEXT,
    created_at TEXT
)""")
db.commit()

# 🚦 Состояния
class Reg(StatesGroup):
    lang = State()
    full_name = State()
    phone = State()
    passport = State()
    birth_date = State()
    pinfl = State()

class Problem(StatesGroup):
    entering = State()
    replying = State()

client_last_message = {}
step_stack = {}

# 🌐 Локализация
LANG_TEXT = {
    'ru': {
        'welcome': "Добро пожаловать в наш бот!",
        'enter_name': "Введите ФИО:",
        'enter_phone': "Введите номер телефона:",
        'enter_passport': "Введите серию и номер паспорта:",
        'enter_birth': "Введите дату рождения (дд.мм.гггг):",
        'enter_pinfl': "Введите ПИНФЛ (14 цифр):",
        'reg_done': "✅ Регистрация завершена. Выберите действие:",
        'menu': ["1️⃣ Узнать кредитную историю", "2️⃣ Кредит калькулятор", "3️⃣ Обратиться к менеджеру", "📄 Мои данные", "🌐 Изменить язык"],
        'describe_problem': "✍️ Опишите проблему одним сообщением:",
        'accepted': "✅ Принято. Ожидайте ответа.",
        'your_data': "📄 Ваши данные:",
    },
    'uz': {
        'welcome': "Botimizga xush kelibsiz!",
        'enter_name': "F.I.Sh.ni kiriting:",
        'enter_phone': "Telefon raqamingizni kiriting:",
        'enter_passport': "Pasport seriyasi va raqamini kiriting:",
        'enter_birth': "Tug'ilgan sanangiz (kk.oo.yyyy):",
        'enter_pinfl': "JShShIR ni kiriting (14 raqam):",
        'reg_done': "✅ Ro'yxatdan o'tish yakunlandi. Xizmatni tanlang:",
        'menu': ["1️⃣ Kredit tarixini bilish", "2️⃣ Kredit kalkulyator", "3️⃣ Menejer bilan bog'lanish", "📄 Ma'lumotlarim", "🌐 Tilni o‘zgartirish"],
        'describe_problem': "✍️ Muammoni yozing:",
        'accepted': "✅ Qabul qilindi. Javob kuting.",
        'your_data': "📄 Sizning ma'lumotlaringiz:",
    }
}

def get_lang(uid):
    c.execute("SELECT lang FROM clients WHERE telegram_id = ?", (uid,))
    row = c.fetchone()
    return row[0] if row else 'ru'

def make_menu(lang):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in LANG_TEXT[lang]['menu']:
        kb.add(item)
    kb.add("🔙 Назад" if lang == 'ru' else "🔙 Ortga", "📋 Меню" if lang == 'ru' else "📋 Asosiy menyu")
    return kb

# 🟢 Старт
@dp.message_handler(commands=['start'])
async def start_cmd(msg: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🇷🇺 Русский", "🇺🇿 O'zbekcha")
    await msg.answer("Выберите язык / Tilni tanlang:", reply_markup=kb)
    await Reg.lang.set()
    step_stack[msg.from_user.id] = []

@dp.message_handler(lambda m: m.text in ["🇷🇺 Русский", "🇺🇿 O'zbekcha"], state=Reg.lang)
async def choose_lang(msg: types.Message, state: FSMContext):
    lang = 'ru' if 'Рус' in msg.text else 'uz'
    await state.update_data(lang=lang)
    step_stack[msg.from_user.id].append(Reg.lang)
    await msg.answer(LANG_TEXT[lang]['enter_name'])
    await Reg.full_name.set()

@dp.message_handler(lambda m: m.text in ["🔙 Назад", "🔙 Ortga"], state="*")
async def go_back(msg: types.Message, state: FSMContext):
    stack = step_stack.get(msg.from_user.id, [])
    if len(stack) > 1:
        stack.pop()
        await stack[-1].set()
        await msg.answer("↩️ Назад. Введите снова:" if get_lang(msg.from_user.id) == 'ru' else "↩️ Ortga. Qayta kiriting:")
    else:
        await msg.answer("🚫 Назад невозможно.")

@dp.message_handler(lambda m: m.text in ["📋 Меню", "📋 Asosiy menyu"], state="*")
async def menu_return(msg: types.Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    kb = make_menu(lang)
    await msg.answer(LANG_TEXT[lang]['reg_done'], reply_markup=kb)
    await state.finish()

# Остальные шаги регистрации будут добавлены в следующей части...