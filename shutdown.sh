#!/bin/bash

# Define the path to the PID file
PID_FILE="gunicorn.pid"

# Check if PID file exists
if [ -f $PID_FILE ]; then
    # Read the PID
    PID=$(cat $PID_FILE)
    
    # Kill the process
    echo "Stopping Gunicorn with PID $PID..."
    kill $PID

    # Remove the PID file
    rm -f $PID_FILE

    echo "Gunicorn stopped."
else
    echo "PID file not found. Gunicorn might not be running."
fi

