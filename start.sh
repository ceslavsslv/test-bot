#!/bin/bash
source venv/bin/activate
nohup python3 main.py > bot.log 2>&1 &
echo "✅ Bot started – logs in bot.log"
