#!/bin/sh
date
source /grad/users/$USER/.bash_profile
(cd /grad/users/$USER/citybeat_online/distributed_gp && nohup python /grad/users/$USER/citybeat_online/distributed_gp/run_online_alarm.py instagram >> /.freespace/citybeat_logs/instagram_alarm & )
