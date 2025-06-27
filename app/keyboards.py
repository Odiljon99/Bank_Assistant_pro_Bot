from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.messages import langs

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
