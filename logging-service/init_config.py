import logging
import hazelcast
from fastapi import FastAPI

from domain_logic.custom_logger import MyHandler


# initial configurations
app = FastAPI(title='Logging-service')

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
hz = hazelcast.HazelcastClient(cluster_members=[
    "127.0.0.1:5701",
    "127.0.0.1:5702",
    "127.0.0.1:5703"
])

# Create Distributed Map
MESSAGES_MAP = hz.get_map("lab3_distributed_map1").blocking()

logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(MyHandler())
