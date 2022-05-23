import uuid
import argparse
import logging
import asyncio
import consul
import hazelcast
from fastapi import FastAPI
from pprint import pprint

from domain_logic.custom_logger import MyHandler


# initial configurations
# app = FastAPI(title='Facade-service')

# Create event loop for asynchronous kafka producer
kafka_loop = asyncio.get_event_loop()

logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(MyHandler())
