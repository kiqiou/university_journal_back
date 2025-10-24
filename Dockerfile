FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "if [ \"$RENDER\" = \"true\" ]; then python manage.py migrate && gunicorn universityjournalback.wsgi:application --bind 0.0.0.0:8000; else python manage.py runserver 0.0.0.0:8000; fi"]

