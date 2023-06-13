#!/bin/sh

# Wait for the database to be ready before running Django
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready"

# Apply database migrations
python manage.py migrate

# Start Django development server
python manage.py runserver 0.0.0.0:8000
