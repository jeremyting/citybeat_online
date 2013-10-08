#!/bin/sh
date
source /grad/users/$USER/.bash_profile
(cd /grad/users/$USER/citybeat_online/crawlers/instagram_crawler && nohup python /grad/users/$USER/citybeat_online/crawlers/instagram_crawler/run_distributed_crawl.py 67 > /.freespace/citybeat_logs/instagram_crawler &)
