#!/bin/bash

# TO-DO(Eddie): replace this whole remote executing thing with some sort of python library such that we could write a configure file and don't have to hard code any shit
while read -r line
do
    array+=($line)
    done < api_host.txt
    for ((i=0; i < ${#array[*]}; i++))
    do
        echo "${array[i]}"
        current_path=$PWD
        echo "current path = $current_path"
        launch_cmd="source ~/virtual_env/virtualenv-1.9.1/new_env/bin/activate; nohup python /grad/users/kx19/citybeat_smil/citybeat/crawlers/instagram/run_api_worker.py > /.freespace/api_worker_log.txt < /dev/null 2>&1 &"
        echo "cmd = $launch_cmd"
        ssh "${array[i]}" "$launch_cmd" 
    done

