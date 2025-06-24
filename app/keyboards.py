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
