#!/usr/bin/env bash
set -o errexit

python manage.py migrate
gunicorn sistema_os.wsgi:application --bind 0.0.0.0:${PORT:-8000}
