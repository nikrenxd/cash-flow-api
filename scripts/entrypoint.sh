#!/usr/bin/env sh
echo "Waiting for database..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 0.1
done
echo "Database started"
python ./src/cash_flow/manage.py migrate
python ./src/cash_flow/manage.py collectstatic --no-input
uv run gunicorn src.cash_flow.root.wsgi:application --bind 0.0.0.0:"$APP_PORT"