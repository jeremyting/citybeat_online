#!/bin/bash

procs=`ps aux|grep twitter_crawl|grep -v grep | wc -l`

if [ $procs -gt 0 ]; then
    echo "process running. exit."
else
    echo "no process running. starting new crawl."
    nohup python /home/eddie/citybeat_production/crawlers/twitter/twitter_crawl.py >> twitter_crawl.log &
fi
