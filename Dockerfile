# Используем официальный образ Python как базу
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Указываем порт (опционально, Telegram не требует проброса порта)
EXPOSE 8080

# Команда запуска приложения
CMD ["python", "webhook_server.py"]
