#!/bin/sh
date
source /grad/users/$USER/.bash_profile
(cd /grad/users/$USER/citybeat_online/distributed_gp && nohup python /grad/users/$USER/citybeat_online/distributed_gp/run_gp.py instagram > /.freespace/instagram_distributed_gp2.log &)
