import logging
import hazelcast
from fastapi import FastAPI

from domain_logic.custom_logger import MyHandler


app = FastAPI(title='Message-service')
MESSAGES_MAP = dict()

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
hz = hazelcast.HazelcastClient(cluster_members=[
    "127.0.0.1:5701",
    "127.0.0.1:5702",
    "127.0.0.1:5703"
])

# Get or create Distributed Queue
queue = hz.get_queue("lab4-distributed-queue").blocking()

logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(MyHandler())
