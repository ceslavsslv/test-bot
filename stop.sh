#!/bin/bash

if [ -f bot.pid ]; then
    PID=$(cat bot.pid)
    kill $PID
    rm bot.pid
    echo "🛑 Bot process $PID stopped."
else
    echo "⚠️ No bot.pid file found – nothing to stop."
fi
