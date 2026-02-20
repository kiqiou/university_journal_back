#!/bin/sh
set -e

echo "Checking required environment variables..."

required_vars="DJANGO_SECRET_KEY DATABASE_URL DJANGO_ALLOWED_HOSTS DEBUG"

for var in $required_vars; do
    if [ -z "$(eval echo \$$var)" ]; then
        echo "Error: $var is not set!"
        exit 1
    fi
done

echo "All required variables are set."

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting gunicorn..."
exec gunicorn universityjournalback.wsgi:application --bind 0.0.0.0:${PORT:-8000} --log-level debug
