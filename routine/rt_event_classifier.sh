#!/bin/sh

procs=`ps aux|grep event_classifier.py |grep -v grep | wc -l`
source /res/users/kx19/.bash_profile
echo $procs
if [ $procs -gt 0 ]; then
    echo "process running. exit."
else
    echo "no process running. starting event classifer."
    (cd /res/users/kx19/citybeat_online/distributed_gp && nohup python /res/users/kx19/citybeat_online/distributed_gp/event_classifier.py >> /grande/local/kx19/citybeat_log/event.log & )
    echo "done"
fi

