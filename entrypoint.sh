#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting gunicorn..."
exec gunicorn universityjournalback.wsgi:application --bind 0.0.0.0:${PORT:-8000} --log-level debug
