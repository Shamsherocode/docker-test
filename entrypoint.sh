#!/bin/sh

# python manage.py makemigrations --no-input
# python manage.py migrate --no-input
python manage.py migrate  --run-syncdb --no-input
python manage.py collectstatic --no-input

gunicorn hututoo.wsgi:application --bind 0.0.0.0:8000