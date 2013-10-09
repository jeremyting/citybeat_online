#!/bin/sh
date
source ~/.bash_profile
(cd $HOME/citybeat_online/system_monitor && nohup python $HOME/citybeat_online/system_monitor/system_monitor.py  > /.freespace/citybeat_logs/rt_update.log & )
