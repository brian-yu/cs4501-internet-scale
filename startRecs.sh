#!/bin/bash
# run this shell script after docker-compose up
while :
do
    docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/recommendation.py
    sleep 60
done