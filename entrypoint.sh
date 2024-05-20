#!/bin/sh

python manage.py makemigrations --no-input
python manage.py migrate
python manage.py collectstatic

gunicorn ecommerce_api.wsgi:application --bind 0.0.0.0:8000

