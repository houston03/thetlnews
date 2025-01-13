# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем переменную окружения
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости Poetry
COPY backend/pyproject.toml backend/poetry.lock* /app/

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Устанавливаем зависимости с помощью Poetry
RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi --no-root

# Копируем остальные файлы проекта
COPY backend/. /app/

# Устанавливаем переменную для FastAPI
ENV UVICORN_PORT=8000

# Открываем порт приложения
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]