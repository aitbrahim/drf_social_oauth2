#!/bin/bash
set -e

PROJECT_PATH=/opt/app/project

if [ "$2" = 'migrate-first' ]; then
    python manage.py migrate --no-input
    python manage.py collectstatic --no-input
fi

if [ "$1" = 'api' ]; then
    exec uwsgi --http :8000 \
              --disable-logging \
              --wsgi-file project/wsgi.py \
              --check-static /opt/public_assets \
              --static-map /static=/opt/public_assets \
              --static-map /favicon.ico=/opt/public_assets/favicon.png

fi

exec "$@"
