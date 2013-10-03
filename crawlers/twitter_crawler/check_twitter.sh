#!/bin/bash

procs=`ps aux|grep twitter_crawl|grep -v grep | wc -l`

if [ $procs -gt 0 ]; then
    echo "process running. exit."
else
    echo "no process running. starting new crawl."
    nohup python /home/$USER/citybeat_online/crawlers/twitter_crawler/twitter_crawl.py >> twitter_crawl.log &
fi
