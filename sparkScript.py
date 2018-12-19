from kafka import KafkaConsumer
from kafka.common import NodeNotReadyError
import os
import time, json

# consume things from kafka and put into access.log
# run recommendation.py every 30 seconds
#       - put results into mysql

time.sleep(10)
while True:
    try:
        consumer = KafkaConsumer('new-recommendations-topic', group_id='recommendations-indexer', bootstrap_servers=['kafka:9092'])
        break
    except NodeNotReadyError:
        print('Node not ready')
        continue
while True:
    print('start of loop')
    try:
        for message in consumer:
            with open('/data/access.log', 'a') as log:
                new_recommendation = json.loads((message.value).decode('utf-8'))
                user_id = new_recommendation['user_id']
                item_id = new_recommendation['item_id']
                log.write(str(user_id) + '\t' + str(item_id) + '\n')
            time.sleep(1)
    except:
        print('uhhhh')
        continue
    print('end of loop')
    time.sleep(30)