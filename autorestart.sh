#!/usr/bin/bash
psres=`sudo /usr/bin/ps -ef | grep a[t]omy_bot.py | wc -l `
#sudo /usr/bin/ps -ef | grep a[t]omy
cd /home/ec2-user/atomy_tgb/
datea=`date '+%Y-%m-%d %H:%M:%S'`
if [ $psres -lt 2 ]; then
        echo "$datea Seems like bot is down, restarting..." >> ./autorestart.log
        sudo ./start.sh
else
	#echo "$datea Bot is running..."  >> ./autorestart.log
	exit
fi
exit
