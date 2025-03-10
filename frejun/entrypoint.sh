#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python frejun/manage.py migrate

# Start Gunicorn
echo "Starting Gunicorn..."
exec uv run gunicorn frejun.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120 