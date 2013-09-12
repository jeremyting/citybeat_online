#!/bin/bash


while read -r line
do
    array+=($line)
    done < gp_host.txt
    for ((i=0; i < ${#array[*]}; i++))
    do
        echo "${array[i]}"
            # pkill -9 -f kills a job with partial name. So *make sure* that the name here is what you want to kill
            ssh "${array[i]}" "pkill -9 -f run_gp_worker.py"
done

