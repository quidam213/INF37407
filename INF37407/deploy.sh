#!/usr/bin/env bash
set -e

python -m uvicorn INF37407.asgi:application --host 0.0.0.0 --port 8000
