#!/usr/bin/bash
pgrep -f atomy_bot.py | xargs sudo kill -9
if [ $? -eq 0 ]; then
	echo "Stopped"
fi
