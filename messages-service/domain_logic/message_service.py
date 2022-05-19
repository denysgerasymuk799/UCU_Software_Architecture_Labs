import uuid

from init_config import queue, logger, MESSAGES_MAP


async def post_messages():
    # while True:
    head = queue.take()
    if isinstance(head, str):
        logger.info(f'Consuming message: {head}')
        # Note that dict in python is thread-safe and not concurrent because of GIL. More details:
        # https://stackoverflow.com/questions/48124257/python-equivalent-of-concurrenthashmap-from-java
        MESSAGES_MAP[uuid.uuid1().__str__()] = head
