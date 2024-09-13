#!/bin/bash

# Define the path to the Gunicorn configuration file and the application
GUNICORN_CONFIG="gunicorn_config.py"
APP_MODULE="app:app"

# Start Gunicorn
echo "Starting Gunicorn..."
gunicorn -c $GUNICORN_CONFIG $APP_MODULE &
echo $! > gunicorn.pid

echo "Gunicorn started with PID $(cat gunicorn.pid)"

