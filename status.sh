#!/usr/bin/bash
psres=`ps -ef | grep a[t]omy |wc -l `
if [ $psres -eq 3 ]; then
	echo "Running"
else
	echo "Stopped"
fi

