from domain_logic.utils import get_consul_kv_value
from init_config import consul_client


MESSAGE_SVC_TOPIC = get_consul_kv_value(consul_client, key='kafka/message_svc_topic')
KAFKA_BROKER = get_consul_kv_value(consul_client, key='kafka/kafka_broker_1')
KAFKA_CONSUMER_GROUP = get_consul_kv_value(consul_client, key='kafka/consumer_group')
