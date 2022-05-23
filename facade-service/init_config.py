import logging
import asyncio

from domain_logic.custom_logger import MyHandler


# Create event loop for asynchronous kafka producer
kafka_loop = asyncio.get_event_loop()

logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(MyHandler())
