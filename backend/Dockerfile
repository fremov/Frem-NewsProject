# Используем легкий образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код бэкенда
COPY . .

# Открываем порт для FastAPI
EXPOSE 8000

# Команда для запуска бэкенда
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]