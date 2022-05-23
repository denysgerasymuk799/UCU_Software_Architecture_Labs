import logging
import asyncio

from domain_logic.custom_logger import MyHandler


MESSAGES_MAP = dict()

# Create event loop for asynchronous kafka consumer
kafka_loop = asyncio.get_event_loop()

logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(MyHandler())

