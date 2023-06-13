#!/bin/bash

echo "Applying outstanding migrations..."
cd src/candlestick/infrastructure/repositories/alembic/ && \
alembic upgrade head

echo "Starting uwsgi application..."
uvicorn candlestick.interface.api.main:app --app-dir /app/src --host 0.0.0.0 --port 8081 --log-level debug
