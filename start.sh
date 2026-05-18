#!/usr/bin/env bash
set -o errexit

echo "Aplicando migrations..."
python manage.py migrate --noinput

echo "Criando superusuario inicial, se configurado..."
python manage.py criar_superusuario_env

echo "Iniciando Gunicorn na porta ${PORT:-8000}..."
exec python -m gunicorn sistema_os.wsgi:application --bind 0.0.0.0:${PORT:-8000} --log-file -
