# Bank Assistant Bot

Telegram-бот для регистрации клиентов, обработки проблем и управления данными.

## Установка

```
pip install -r requirements.txt
```

Создай файл `.env`:

```
BOT_TOKEN=твой_токен
GROUP_CHAT_ID=-123456789
```

## Запуск

```
python main.py
```

## Deploy на Render

1. Подключи GitHub репозиторий
2. Укажи `main.py` как entry point
3. Пропиши переменные окружения в Render:
   - `BOT_TOKEN`
   - `GROUP_CHAT_ID`
