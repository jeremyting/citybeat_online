#!/bin/sh

# This file is currently not being used at TA machines.
procs=`ps aux|grep event_classifier.py |grep -v grep | wc -l`
source /grad/users/$USER/.bash_profile
echo $procs
if [ $procs -gt 0 ]; then
    echo "process running. exit."
else
    echo "no process running. starting event classifer."
    (cd /grad/users/$USER/citybeat_online/distributed_gp && nohup python /grad/users/$USER/citybeat_online/distributed_gp/event_classifier.py >> /.freespace/citybeat_logs/instagram_alarm & )
    echo "done"
fi

