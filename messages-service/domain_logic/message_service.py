import uuid
import json
from aiokafka import AIOKafkaConsumer

from init_config import logger, MESSAGES_MAP, kafka_loop
from domain_logic.constants import *


async def post_messages():
    consumer = AIOKafkaConsumer(MESSAGE_SVC_TOPIC,
                                loop=kafka_loop,
                                bootstrap_servers=[KAFKA_BROKER],
                                group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for record in consumer:
            msg = json.loads(record.value)
            msg = msg['message']
            logger.info(f'Consuming msg: {msg}')

            if isinstance(msg, str):
                # Note that dict in python is thread-safe and not concurrent because of GIL. More details:
                # https://stackoverflow.com/questions/48124257/python-equivalent-of-concurrenthashmap-from-java
                MESSAGES_MAP[uuid.uuid1().__str__()] = msg

            await consumer.commit()

    except Exception as err:
        logger.error(f'Consume error: {err}')
    finally:
        await consumer.stop()
