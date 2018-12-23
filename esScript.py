# script that continually runs in the batch container and pulls new listings from kafka

from kafka import KafkaConsumer
from kafka.common import NodeNotReadyError
from elasticsearch import Elasticsearch
import urllib.request
import urllib.parse
import time, json

time.sleep(10)
es = Elasticsearch(['es'])

# index everything in database
url = 'http://models-api:8000/api/v1/all_items/'
resp_json = urllib.request.urlopen(url).read().decode('utf-8')
resp = json.loads(resp_json)
items = resp['result']['items']
for item in items:
    es.index(index='items_index', doc_type='item', id=item['id'], body=item)
    es.indices.refresh(index="items_index")
    time.sleep(1)

while True:
    try:
        consumer = KafkaConsumer('new-items-topic', group_id='items-indexer', bootstrap_servers=['kafka:9092'])
        break
    except NodeNotReadyError:
        print('Node not ready')
        continue
while True:
    print('start of loop')
    try:        
        for message in consumer:
            new_item = json.loads((message.value).decode('utf-8'))
            es.index(index='items_index', doc_type='item', id=new_item['id'], body=new_item)
            es.indices.refresh(index="items_index")
            time.sleep(1)
    except:
        print('uhhhh')
        continue
    print('end of loop')
    time.sleep(30)