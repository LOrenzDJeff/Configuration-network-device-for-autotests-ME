#!/bin/bash

base_port=33921

num_days=7

for ((i=0; i<num_days; i++)); do
    port=$((base_port + i))
    echo "Stopping Allure report on port $port"

    pid=$(lsof -i :$port -t)
    
    if [ -n "$pid" ]; then
        kill $pid
        echo "Allure report on port $port stopped"
    else
        echo "No Allure report running on port $port"
    fi
done
pid=$(lsof -i :33929 -t)
kill $pid