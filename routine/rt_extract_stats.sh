#!/bin/sh
date
(cd $HOME/citybeat_online/stats && nohup python $HOME/citybeat_online/stats/stats.py > $HOME/citybeat_logs/extract_stats.log &)
