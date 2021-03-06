#!/bin/sh

# This file is currently not being used at TA machines.
procs=`ps aux|grep event_classifier.py |grep -v grep | wc -l`
echo $procs
if [ $procs -gt 0 ]; then
    echo "process running. exit."
else
    echo "no process running. starting event classifer."
    (cd $HOME/citybeat_online/distributed_gp && nohup python $HOME/citybeat_online/distributed_gp/event_classifier.py > $HOME/citybeat_logs/classifier_monitor_log & )
    echo "done"
fi

