#!/bin/bash

# Define the path to the Gunicorn configuration file and the application
GUNICORN_CONFIG="gunicorn_config.py"
APP_MODULE="app:app"
PID_FILE="gunicorn.pid"
LOG_FILE="gunicorn.log"

# Function to start Gunicorn
start_gunicorn() {
    echo "Starting Gunicorn..." | tee -a $LOG_FILE
    gunicorn -c $GUNICORN_CONFIG $APP_MODULE >> $LOG_FILE 2>&1 &
    echo $! > $PID_FILE
    echo "Gunicorn started with PID $(cat $PID_FILE)" | tee -a $LOG_FILE
}

# Function to stop Gunicorn
stop_gunicorn() {
    if [ -f $PID_FILE ]; then
        PID=$(cat $PID_FILE)
        echo "Stopping Gunicorn with PID $PID..." | tee -a $LOG_FILE
        kill $PID
        rm -f $PID_FILE
        echo "Gunicorn stopped." | tee -a $LOG_FILE
    else
        echo "PID file not found. Gunicorn might not be running." | tee -a $LOG_FILE
    fi
}

# Check if Gunicorn is running
if [ -f $PID_FILE ]; then
    PID=$(cat $PID_FILE)
    if ps -p $PID > /dev/null; then
        echo "Gunicorn is already running with PID $PID." | tee -a $LOG_FILE
        read -p "Do you want to restart it? (y/n): " RESTART
        if [ "$RESTART" == "y" ]; then
            stop_gunicorn
            start_gunicorn
        else
            echo "Gunicorn will continue running." | tee -a $LOG_FILE
        fi
    else
        echo "PID file exists but Gunicorn is not running. Starting Gunicorn..." | tee -a $LOG_FILE
        start_gunicorn
    fi
else
    echo "Gunicorn is not running. Starting Gunicorn..." | tee -a $LOG_FILE
    start_gunicorn
fi

