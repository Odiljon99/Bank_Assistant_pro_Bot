from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.messages import langs

def get_main_menu(lang):
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(langs[lang]["menu"])],
            [KeyboardButton(langs[lang]["admin_panel"])],
        ]
    )

def get_language_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton("🇷🇺 Русский"), KeyboardButton("🇺🇿 O‘zbek")],
        ]
    )

def get_agree_keyboard(lang):
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton("✅ Я согласен" if lang == "ru" else "✅ Men roziman")],
        ]
    )
