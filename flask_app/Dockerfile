FROM python:3.12-slim

WORKDIR /flask_app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# Запуск Flask через Gunicorn с 2 воркерами и 2 потоками
CMD ["gunicorn", "-w", "2", "--threads", "2", "-b", "0.0.0.0:5000", "app.main:app"]
