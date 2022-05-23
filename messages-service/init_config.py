import uuid
import logging
import asyncio
import consul
import argparse
import hazelcast
from fastapi import FastAPI

from domain_logic.custom_logger import MyHandler
from domain_logic.utils import get_all_service_urls, add_service_to_consul, get_consul_kv_value


app = FastAPI(title='Message-service')
MESSAGES_MAP = dict()

# Create event loop for asynchronous kafka consumer
kafka_loop = asyncio.get_event_loop()

logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(MyHandler())


if __name__ == '__main__':
    import uvicorn

    parser = argparse.ArgumentParser(description='Start message service.')
    parser.add_argument('service_port', type=int, default=8083,
                        help='a port, on which to start the service')
    args = parser.parse_args()

    # Configure consul values
    consul_client = consul.Consul(
        host='127.0.0.1',
        port=8500
    )

    service_uuid = uuid.uuid1()
    service_key = 'messages_service/messages_service_' + service_uuid.__str__()
    host_ip = get_consul_kv_value(consul_client, key='hz_distributed_map')
    add_service_to_consul(consul_client, 'messages_service/messages_service_', service_key,
                          service_address=f'http://{host_ip}:{args.service_port}')

    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster
    cluster_members_addresses = get_all_service_urls(consul_client, service_name='hz_node')
    hz = hazelcast.HazelcastClient(cluster_members=cluster_members_addresses)

    uvicorn.run(app, port=args.service_port)

