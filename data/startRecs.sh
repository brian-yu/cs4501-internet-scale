#!/bin/bash
# run this shell script after docker-compose up
while :
do
    python recommendation.py
    sleep 60
done
