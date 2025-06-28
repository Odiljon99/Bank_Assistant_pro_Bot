from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from app.messages import langs


def get_main_menu(lang, is_admin=False):
    buttons = [
        [KeyboardButton(text="📊 Узнать кредитную историю")],
        [KeyboardButton(text="📈 Кредит калькулятор")],
        [KeyboardButton(text="💬 Обратиться к менеджеру")],
        [KeyboardButton(text="🌐 Изменить язык")],
        [KeyboardButton(text="📑 Мои данные")]
    ]
    if is_admin:
        buttons.append([KeyboardButton(text=langs[lang]["admin_panel"])])
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


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


def get_credit_history_agree_keyboard(lang):
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


def get_admin_panel_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="📋 Список пользователей")],
            [KeyboardButton(text="🔎 Найти пользователя")],
            [KeyboardButton(text="↩️ Назад")]
        ]
    )


def get_edit_data_menu(lang):
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="📛 ФИО"), KeyboardButton(text="📞 Телефон")],
            [KeyboardButton(text="📅 Дата рождения"), KeyboardButton(text="🆔 ПИНФЛ")],
            [KeyboardButton(text="↩️ Назад")]
        ]
    )
