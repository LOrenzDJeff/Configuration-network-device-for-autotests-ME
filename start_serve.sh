#!/bin/bash

cd ../result_back
days_of_week=("Monday" "Tuesday" "Wednesday" "Thursday" "Friday" "Saturday" "Sunday")

port=33920

for day in "${days_of_week[@]}"; do
    if [ -d "$day" ]; then
        port=$((port + 1))

        echo "Starting Allure report for $day on port $port"
        allure serve -h 192.168.16.115 -p $port "$day" &
        sleep 15
    else
        echo "Directory $day does not exist"
    fi
done