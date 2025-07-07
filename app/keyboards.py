from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from app.messages import langs, get_lang_safe


def get_main_menu(lang: str, is_admin: bool = False) -> ReplyKeyboardMarkup:
    texts = get_lang_safe(lang)
    buttons = [
        [KeyboardButton(text=texts["main_menu_options"][0])],
        [KeyboardButton(text=texts["main_menu_options"][1])],
        [KeyboardButton(text=texts["main_menu_options"][2])],
        [KeyboardButton(text=texts["main_menu_options"][3])],
        [KeyboardButton(text=texts["main_menu_options"][4])],
    ]
    if is_admin:
        buttons.append([KeyboardButton(text=texts["admin_panel"])])
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def get_language_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇿 O‘zbek")]
        ]
    )


def get_agree_keyboard(lang: str) -> ReplyKeyboardMarkup:
    texts = get_lang_safe(lang)
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="✅ Я согласен" if lang == "ru" else "✅ Men roziman")]
        ]
    )


def get_credit_history_agree_keyboard(lang: str) -> InlineKeyboardMarkup:
    texts = get_lang_safe(lang)
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
    texts = get_lang_safe(lang)
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="📋 Список пользователей" if lang == "ru" else "📋 Foydalanuvchilar ro‘yxati")],
            [KeyboardButton(text="🔎 Найти пользователя" if lang == "ru" else "🔎 Foydalanuvchini qidirish")],
            [KeyboardButton(text=texts["back"])]
        ]
    )


def get_edit_data_menu(lang: str) -> ReplyKeyboardMarkup:
    texts = get_lang_safe(lang)
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="📛 ФИО" if lang == "ru" else "📛 Ism sharifi"),
                KeyboardButton(text="📞 Телефон" if lang == "ru" else "📞 Telefon")
            ],
            [
                KeyboardButton(text="📅 Дата рождения" if lang == "ru" else "📅 Tug‘ilgan sana"),
                KeyboardButton(text="🆔 ПИНФЛ" if lang == "ru" else "🆔 JSHSHIR")
            ],
            [KeyboardButton(text=texts["back"])]
        ]
    )


def get_back_keyboard(lang: str) -> ReplyKeyboardMarkup:
    texts = get_lang_safe(lang)
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text=texts["back"])]
        ]
    )
