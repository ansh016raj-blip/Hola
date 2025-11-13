#!/bin/bash

echo "Starting bot..."
while true
do
    python3 bot/main.py
    echo "Bot crashed... restarting in 5 seconds."
    sleep 5
done
