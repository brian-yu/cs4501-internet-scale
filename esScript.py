# script that continually runs in the batch container and pulls new listings from kafka

from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import time, json

time.sleep(10)
es = Elasticsearch(['es'])
consumer = KafkaConsumer('new-items-topic', group_id='items-indexer', bootstrap_servers=['kafka:9092'])
for message in consumer:
    new_item = json.loads((message.value).decode('utf-8'))
    es.index(index='items_index', doc_type='item', id=new_item['id'], body=new_item)
    es.indices.refresh(index="items_index")