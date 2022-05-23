import uuid
import json
from aiokafka import AIOKafkaConsumer

from init_config import logger, MESSAGES_MAP, kafka_loop
from domain_logic.constants import *
from domain_logic.utils import get_consul_kv_value


async def post_messages(consul_client):
    consumer = AIOKafkaConsumer(get_consul_kv_value(consul_client, key=MESSAGE_SVC_TOPIC_KEY),
                                loop=kafka_loop,
                                bootstrap_servers=[get_consul_kv_value(consul_client, key=KAFKA_BROKER_KEY)],
                                group_id=get_consul_kv_value(consul_client, key=KAFKA_CONSUMER_GROUP_KEY))
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
