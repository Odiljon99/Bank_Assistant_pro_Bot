from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from app.messages import langs

def get_lang_safe(lang: str) -> str:
    return lang if lang in langs else "ru"

def get_main_menu(lang: str, is_admin: bool = False) -> ReplyKeyboardMarkup:
    lang = get_lang_safe(lang)
    buttons = [
        [KeyboardButton(text=langs[lang]["main_menu_options"][0])],  # Узнать кредитную историю
        [KeyboardButton(text=langs[lang]["main_menu_options"][1])],  # Кредит калькулятор
        [KeyboardButton(text=langs[lang]["main_menu_options"][2])],  # Обратиться к менеджеру
        [KeyboardButton(text=langs[lang]["main_menu_options"][3])],  # Изменить язык
        [KeyboardButton(text=langs[lang]["main_menu_options"][4])],  # Мои данные
    ]
    if is_admin:
        buttons.append([KeyboardButton(text=langs[lang]["admin_panel"])])
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)

def get_language_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇿 O‘zbek")]
        ]
    )

def get_agree_keyboard(lang: str) -> ReplyKeyboardMarkup:
    lang = get_lang_safe(lang)
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="✅ Я согласен" if lang == "ru" else "✅ Men roziman")]
        ]
    )

def get_credit_history_agree_keyboard(lang: str) -> InlineKeyboardMarkup:
    lang = get_lang_safe(lang)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Согласен отправить данные" if lang == "ru" else "✅ Maʼlumotlarni yuborishga roziman",
                    callback_data="agree_send_data"
                )
            ]
        ]
    )

def get_admin_panel_keyboard(lang: str) -> ReplyKeyboardMarkup:
    lang = get_lang_safe(lang)
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="📋 Список пользователей")],
            [KeyboardButton(text="🔎 Найти пользователя")],
            [KeyboardButton(text=langs[lang]["back"])]
        ]
    )

def get_edit_data_menu(lang: str) -> ReplyKeyboardMarkup:
    lang = get_lang_safe(lang)
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="📛 ФИО"), KeyboardButton(text="📞 Телефон")],
            [KeyboardButton(text="📅 Дата рождения"), KeyboardButton(text="🆔 ПИНФЛ")],
            [KeyboardButton(text=langs[lang]["back"])]
        ]
    )
