#!/bin/bash

set -e

# Export environment variables
export DJANGO_AUTH0_AUDIENCE="${DJANGO_AUTH0_AUDIENCE}"
export DJANGO_AUTH0_DOMAIN="${DJANGO_AUTH0_DOMAIN}"
export DATABASE_URL="${DATABASE_URL}"
export DJANGO_TIME_ZONE="${DJANGO_TIME_ZONE}"
export DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY}"
export POSTGRES_DB="${POSTGRES_DB}"
export POSTGRES_USER="${POSTGRES_USER}"
export POSTGRES_PASSWORD="${POSTGRES_PASSWORD}"

echo "DATABASE_URL: $DATABASE_URL"


#echo "Waiting for PostgreSQL..."
#while ! nc -z $DATABASE_URL; do
#  sleep 2.5
#done
echo "PostgreSQL started"

# Apply database migrations
echo "Applying database migrations..."
python backend/manage.py migrate

# Collect static files
#echo "Collecting static files..."
#python manage.py collectstatic --noinput

# Start server
echo "Starting server..."
# Start Daphne
#exec daphne -p 8000 backend.asgi:application
exec daphne -p 8000 backend.asgi:application --bind 0.0.0.0

