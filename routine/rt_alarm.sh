#!/bin/sh
date
source /grad/users/$whoami/.bash_profile
(cd /grad/users/$whoami/citybeat_online/distributed_gp && nohup python /grad/users/$whoami/citybeat_online/distributed_gp/run_online_alarm.py instagram >> /.freespace/alarm_db_report2.txt & )
