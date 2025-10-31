#!/usr/bin/env bash
set -e

python manage.py makemigrations
python manage.py migrate
python manage.py parser_arcgis
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@example.com \
DJANGO_SUPERUSER_PASSWORD=admin123 \
python manage.py createsuperuser --noinput || true
