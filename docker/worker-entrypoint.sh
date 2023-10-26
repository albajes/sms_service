#!/bin/sh

until cd /app2/service2
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A service2 worker --loglevel=info
