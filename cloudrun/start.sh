#!/bin/sh
set -eu

python manage.py migrate --noinput
python manage.py seed_demo

exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-80}" \
  --workers "${GUNICORN_WORKERS:-2}" \
  --timeout "${GUNICORN_TIMEOUT:-60}" \
  --access-logfile - \
  --error-logfile -
