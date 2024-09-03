# Используем официальный Python образ в качестве базового
FROM python:3.11-slim

LABEL authors="UdoChudo"

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы зависимостей в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в рабочую директорию
COPY main.py .

# Устанавливаем переменную окружения для токена API
ENV API_TOKEN=your_api_token_here

# Команда для запуска бота
CMD ["python", "main.py"]
