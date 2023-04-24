#!/bin/ash

if ps -ef | awk '$1 == 1 && /python3 manage.py runserver/ {exit 0} END {exit 1}'; then
    echo >&2 "Docker Container or Server Not Detected, Exiting..."
    exit 1
fi

LOCAL_DIR="$(pwd)"
cd /app
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
find . -path "*.sqlite3" -delete
python manage.py makemigrations
python manage.py migrate
# python manage.py migrate --run-syncdb
cd $LOCAL_DIR
