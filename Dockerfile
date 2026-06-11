FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# DJANGO_SETTINGS_MODULE wordt ingesteld via Railway's Variables-paneel (runtime),
# zodat railway run en de container dezelfde variabelen gebruiken.

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/base.txt requirements/base.txt
COPY requirements/production.txt requirements/production.txt
RUN pip install --no-cache-dir -r requirements/production.txt

COPY . .

EXPOSE 8000

# collectstatic + migrate bij elke deploy, daarna Gunicorn opstarten.
# build_runclub_home is idempotent: vult de startpagina alleen als deze nog
# leeg is (eerste deploy) en doet daarna niets meer.
CMD ["sh", "-c", "python manage.py collectstatic --no-input && python manage.py migrate && python manage.py ensure_superuser && python manage.py build_runclub_home && gunicorn runclub.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120 --access-logfile - --error-logfile - --capture-output --log-level info"]
