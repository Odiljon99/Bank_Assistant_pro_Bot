def get_lang_safe(lang: str) -> str:
    return lang if lang in langs else "ru"

langs = {
    "ru": {
        "menu": "📋 Главное меню:",
        "admin_panel": "🔧 Панель администратора",
        "new_report": "🆕 Новая заявка:",
        "back": "🔙 Назад",
        "start": "Привет! Выберите язык.",
        "warning_text": (
            "⚠️ ВНИМАНИЕ!\n\n"
            "Отправляя свои данные, вы соглашаетесь на их обработку.\n"
            "Мы гарантируем конфиденциальность и безопасность.\n\n"
            "Если вы согласны, нажмите кнопку ниже."
        ),
        "start_registration": "📝 Начнем регистрацию. Пожалуйста, ответьте на следующие вопросы.",
        "ask_full_name": "📛 Введите ваше полное имя:",
        "ask_phone": "📞 Введите ваш номер телефона (только 9 цифр, например: 991112233):",
        "ask_birth_day": "📅 Введите день рождения (число от 1 до 31):",
        "ask_birth_month": "📅 Введите месяц рождения (число от 1 до 12):",
        "ask_birth_year": "📅 Введите год рождения (например: 1995):",
        "ask_pinfl": "🆔 Введите ваш ПИНФЛ:",
        "main_menu_options": [
            "🔍 Узнать кредитную историю",
            "📈 Кредит калькулятор",
            "💬 Обратиться к менеджеру",
            "🌐 Изменить язык",
            "✏️ Мои данные"
        ],
        "send_data_consent": "❗ Чтобы узнать кредитную историю, мы отправим ваши данные менеджеру банка. Вы согласны?",
        "data_sent_to_staff": "✅ Данные отправлены сотрудникам. Ожидайте ответа.",
        "edit_data_prompt": "✏️ Что вы хотите изменить?",
        "choose_problem_prompt": "📋 Выберите свою проблему из списка:",
        "admin_view_header": "👥 Зарегистрированные пользователи:",
        "no_users_found": "🙁 Пока нет пользователей в базе данных.",
        "confirm_send": "✅ Отправить",
        "cancel": "❌ Отмена",
        "answer": "✍️ Ответить",
        "complete": "✅ Завершить",
        "language_changed": "🌐 Язык успешно изменён.",
        "data_updated": "✅ Данные успешно обновлены.",
        "choose_language": "🌐 Выберите язык:"
    },

    "uz": {
        "menu": "📋 Asosiy menyu:",
        "admin_panel": "🔧 Admin panel",
        "new_report": "🆕 Yangi muammo:",
        "back": "🔙 Orqaga",
        "start": "Salom! Tilni tanlang.",
        "warning_text": (
            "⚠️ DIQQAT!\n\n"
            "Maʼlumotlaringizni yuborish orqali siz ularni qayta ishlashga rozilik bildirasiz.\n"
            "Biz maxfiylik va xavfsizlikni kafolatlaymiz.\n\n"
            "Agar rozisiz, quyidagi tugmani bosing."
        ),
        "start_registration": "📝 Ro‘yxatdan o‘tishni boshlaymiz. Iltimos, quyidagi savollarga javob bering.",
        "ask_full_name": "📛 To‘liq ismingizni kiriting:",
        "ask_phone": "📞 Telefon raqamingizni kiriting (faqat 9 ta raqam, masalan: 991112233):",
        "ask_birth_day": "📅 Tug‘ilgan kuningizni kiriting (1 dan 31 gacha son):",
        "ask_birth_month": "📅 Tug‘ilgan oyingizni kiriting (1 dan 12 gacha son):",
        "ask_birth_year": "📅 Tug‘ilgan yilingizni kiriting (masalan: 1995):",
        "ask_pinfl": "🆔 PINFL raqamingizni kiriting:",
        "main_menu_options": [
            "🔍 Kredit tarixini bilish",
            "📈 Kredit kalkulyatori",
            "💬 Menejerga murojaat",
            "🌐 Tilni o‘zgartirish",
            "✏️ Ma’lumotlarim"
        ],
        "send_data_consent": "❗ Kredit tarixini bilish uchun sizning ma’lumotlaringiz bank menejeriga yuboriladi. Rozimisiz?",
        "data_sent_to_staff": "✅ Ma’lumotlar xodimlarga yuborildi. Javobni kuting.",
        "edit_data_prompt": "✏️ Nima ma’lumotni o‘zgartirmoqchisiz?",
        "choose_problem_prompt": "📋 Muammoni tanlang:",
        "admin_view_header": "👥 Ro‘yxatdan o‘tgan foydalanuvchilar:",
        "no_users_found": "🙁 Hozircha foydalanuvchilar yo‘q.",
        "confirm_send": "✅ Yuborish",
        "cancel": "❌ Bekor qilish",
        "answer": "✍️ Javob berish",
        "complete": "✅ Tugatildi",
        "language_changed": "🌐 Til muvaffaqiyatli o‘zgartirildi.",
        "data_updated": "✅ Ma’lumotlar yangilandi.",
        "choose_language": "🌐 Tilni tanlang:"
    }
}
