#!/bin/sh
date
source /grad/users/kx19/.bash_profile
#(cd /grad/users/kx19/CityBeat/distributed_gp && nohup python /grad/users/kx19/CityBeat/distributed_gp/run_distributed_gp.py  > /.freespace/dis_gp.log &)
(cd /grad/users/kx19/citybeat_online/distributed_gp && nohup python /grad/users/kx19/citybeat_online/distributed_gp/run_gp.py instagram > /.freespace/instagram_distributed_gp.log &)
