﻿FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && exec gunicorn universityjournalback.wsgi:application --bind 0.0.0.0:${PORT:-8000} --log-level debug"]
