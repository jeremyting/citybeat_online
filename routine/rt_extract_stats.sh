#!/bin/sh
date
source ~/.bash_profile
(cd $HOME/citybeat_online/stats_pipeline && nohup python $HOME/citybeat_online/stats_pipeline/stats.py > /.freespace/citybeat_logs/extract_stats.log &)
