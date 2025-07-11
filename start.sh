#!/bin/bash

# Aktivē virtuālo vidi
source venv/bin/activate

# Startē botu fona režīmā un saglabā PID
nohup python3 main.py > bot.log 2>&1 &

echo $! > bot.pid
echo "✅ Bot started – logs in bot.log"
