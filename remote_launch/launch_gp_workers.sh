#!/bin/bash

# TO-DO(Chaolun): replace this whole remote executing thing with some sort of python library such that we could write a configure file and don't have to hard code any shit
while read -r line
do
    array+=($line)
    done < gp_host.txt
    for ((i=0; i < ${#array[*]}; i++))
    do
        echo "${array[i]}"
        current_path=$PWD
        launch_cmd="source ~/.bash_profile; nohup python /grad/users/cx28/citybeat_online/distributed_gp/run_gp_worker.py > /.freespace/gp_worker_log.txt 2> /dev/null < /dev/null &"
        echo "cmd = $launch_cmd"
        ssh "${array[i]}" "$launch_cmd" 
    done

