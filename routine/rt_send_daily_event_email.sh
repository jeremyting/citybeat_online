#!/bin/sh
date
source /grad/users/$USER/.bash_profile
(cd /grad/users/$USER/citybeat_online/system_monitor && nohup python /grad/users/$USER/citybeat_online/system_monitor/event_daily_notification.py > /.freespace/citybeat_logs/daily_event_email &)
