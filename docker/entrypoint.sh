#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

cd service2
source ../venv/bin/activate
#python manage.py flush --no-input
sleep 30
python manage.py migrate

exec "$@"