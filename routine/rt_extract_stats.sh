#!/bin/sh
date
source ~/.bash_profile
(cd $HOME/citybeat_online/stats && nohup python $HOME/citybeat_online/stats/stats.py > /.freespace/citybeat_logs/extract_stats.log &)
