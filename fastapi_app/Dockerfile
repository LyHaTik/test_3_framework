FROM python:3.12-slim

WORKDIR /fastapi_app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Запуск FastAPI через Gunicorn с UvicornWorker
# -w 2: 2 воркера (по числу доступных ядер)
# --threads 2: дополнительные потоки на воркер, чтобы обрабатывать больше одновременных запросов
# --timeout 30: таймаут обработки запроса
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--threads", "2", "--bind", "0.0.0.0:8000", "--timeout", "30", "app.main:app"]
