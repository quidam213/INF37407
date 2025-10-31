#!/usr/bin/env bash
set -e

mysql -u root -p -e "CREATE DATABASE `INF37407` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;"
python manage.py makemigrations
python manage.py migrate
python manage.py parser_arcgis
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@example.com \
DJANGO_SUPERUSER_PASSWORD=admin123 \
python manage.py createsuperuser --noinput || true
