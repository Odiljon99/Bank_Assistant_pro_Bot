from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.messages import langs
from datetime import datetime, timedelta

def get_main_menu(lang):
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text=langs[lang]["menu"])],
            [KeyboardButton(text=langs[lang]["admin_panel"])],
        ]
    )

def get_language_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇿 O‘zbek")],
        ]
    )

def get_agree_keyboard(lang):
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="✅ Я согласен" if lang == "ru" else "✅ Men roziman")],
        ]
    )

# 📅 Календарь для выбора даты
def get_calendar_keyboard(year=None, month=None):
    now = datetime.now()
    year = year or now.year
    month = month or now.month

    days_in_month = (datetime(year + (month // 12), (month % 12) + 1, 1) - timedelta(days=1)).day
    first_day = datetime(year, month, 1).weekday()  # 0 - Monday

    # Заголовок и дни недели
    keyboard = [
        [InlineKeyboardButton(text=f"{year}-{month:02d}", callback_data="ignore")],
        [InlineKeyboardButton(day, callback_data="ignore") for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]]
    ]

    # Пустые ячейки перед 1 числом
    row = []
    for _ in range((first_day + 6) % 7):
        row.append(InlineKeyboardButton(" ", callback_data="ignore"))

    # Дни месяца
    for day in range(1, days_in_month + 1):
        row.append(InlineKeyboardButton(str(day), callback_data=f"calendar:{year}-{month:02d}-{day:02d}"))
        if len(row) == 7:
            keyboard.append(row)
            row = []

    if row:
        while len(row) < 7:
            row.append(InlineKeyboardButton(" ", callback_data="ignore"))
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
