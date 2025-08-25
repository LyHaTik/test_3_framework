#!/bin/sh
set -e

# Ждём готовности PostgreSQL
echo "Waiting for PostgreSQL..."
while ! pg_isready -h "$DB_HOST" -p 5432 -U "$POSTGRES_USER" > /dev/null 2>&1; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Применяем миграции
python manage.py makemigrations tasks
python manage.py migrate --noinput

# Можно создать суперпользователя при необходимости
# python manage.py createsuperuser --noinput --username admin --email admin@example.com

# Запускаем CMD
exec "$@"
