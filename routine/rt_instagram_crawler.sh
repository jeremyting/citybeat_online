#!/bin/sh
date
source /grad/users/$USER/.bash_profile
(cd /grad/users/$USER/citybeat_online/crawlers/instagram_crawler && nohup python /grad/users/$USER/citybeat_online/crawlers/instagram_crawler/run_distributed_crawl.py 200 citybeat_production > /.freespace/citybeat_instagram_crawler.log &)
