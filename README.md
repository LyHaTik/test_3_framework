# test_3_framework
Тестирование 3х популярных фреймворков на python: FastApi, Flask, Django.
# Сравнение FastAPI, Flask и Django

## 📌 Описание
Этот проект поднимает три веб-приложения (FastAPI, Flask и Django), которые работают с общей базой данных PostgreSQL 15, также запущенной в отдельном контейнере.
Все сервисы управляются через Docker Compose под WSL2 (2 CPU, 4 GB RAM).
Цель — сравнить производительность разных фреймворков при одинаковых условиях.

## ⚙️ Стек
- Python 3.12
- FastAPI + Uvicorn/Gunicorn +asyncpg
- Flask + Gunicorn + psycopg2-binary
- Django + Gunicorn +psycopg2-binary
- PostgreSQL 15
- Docker + Docker Compose
- gauge

## 🗂️ Структура проекта

.
├── docker-compose.yml
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── pg_data/                # данные Postgres
├── fastapi_app/            # код FastAPI-приложения
│   ├── Dockerfile
│   ├── app/
│   │   ├── main.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── repositories.py
│   │   ├── services.py
│   │   └── routes.py
│   └── requirements.txt
├── flask_app/              # код Flask-приложения
│   ├── app/
│   │   ├── main.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── services.py
│   │   └── routes.py
│   ├── Dockerfile
│   └── requirements.txt
├── django_app/             # код Django-приложения
│   ├── Dockerfile
│   ├── django_app/
│   └── requirements.txt
└── tests/                  
    └── gauge/




## 🚀 Запуск проекта

### 1. Склонировать репозиторий
git@github.com:LyHaTik/test_3_framework.git
cd test_3_framework```

### 2. Запустить сервисы
docker compose up --build -d

### 3. Доступ к сервисам
FastAPI → http://localhost:8011/docs
Flask → http://localhost:8012/tasks
Django → http://localhost:8013/tasks
PostgreSQL → localhost:5442 (логин/пароль: postgres/postgres, база: tasks_db)

### 4. Принимаемые команды:
GET	"/tasks/"	- Список задач
POST	"/tasks/" - Создать задачу
GET	"/tasks/<id>/"	- Получить задачу
PUT	"/tasks/<id>/"	- Обновить задачу
DELETE	"/tasks/<id>/"	- Удалить задачу

## Тест
python -m venv venv
source venv/scripts/activate
pip install -r requirements.txt
gauge install python

cd tests/gauge/
gauge run specs/

Результаты сохраняются в results.csv
