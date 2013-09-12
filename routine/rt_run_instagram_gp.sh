#!/bin/sh
date
source /grad/users/$whoami/.bash_profile
(cd /grad/users/$whoami/citybeat_online/distributed_gp && nohup python /grad/users/$whoami/citybeat_online/distributed_gp/run_gp.py instagram > /.freespace/instagram_distributed_gp2.log &)
