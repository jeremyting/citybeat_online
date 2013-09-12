#!/bin/bash

IFS=$'\r\n' workers=($(cat gp_host.txt))

COUNT="0"
for i in ${workers[*]};
do 
    echo "SSH to $i"
    ssh $i "source ~/.bash_profile nohup python /grad/users/cx28/citybeat_online/distributed_gp/run_gp_worker.py > /.freespace/gp_
worker_log.txt 2> /dev/null < /dev/null &"
done
