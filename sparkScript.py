from kafka import KafkaConsumer
from kafka.common import NodeNotReadyError
import os
import time, json

# consume things from kafka for spark in recommendation.py
# run recommendation.py every 30 seconds
#       - put results into mysql