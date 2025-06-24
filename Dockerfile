# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Указываем команду запуска
CMD ["python", "webhook_server.py"]
