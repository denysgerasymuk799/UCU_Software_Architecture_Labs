import uuid
import argparse
import logging
import consul
import hazelcast
from fastapi import FastAPI

from domain_logic.custom_logger import MyHandler
from domain_logic.utils import get_all_service_urls, add_service_to_consul, get_consul_kv_value


# initial configurations
app = FastAPI(title='Logging-service')

logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(MyHandler())


if __name__ == '__main__':
    import uvicorn

    parser = argparse.ArgumentParser(description='Start logging service.')
    parser.add_argument('service_port', type=int, default=8091,
                        help='a port, on which to start the service')
    args = parser.parse_args()

    # Configure consul values
    consul_client = consul.Consul(
        host='127.0.0.1',
        port=8500
    )

    service_uuid = uuid.uuid1()
    service_key = 'logging_service/logging_service_' + service_uuid.__str__()
    api_root_path = '/logging-svc/api/v1.0'
    host_ip = get_consul_kv_value(consul_client, key='hazelcast/hz_distributed_map')
    add_service_to_consul(consul_client, 'logging_service/logging_service_', service_key,
                          service_address=f'http://{host_ip}:{args.service_port}{api_root_path}')

    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster
    cluster_members_addresses = get_all_service_urls(consul_client, service_name='hazelcast/hz_node')
    hz = hazelcast.HazelcastClient(cluster_members=cluster_members_addresses)

    # Create Distributed Map
    distributed_map_name = get_consul_kv_value(consul_client, key='hazelcast/hz_distributed_map')
    MESSAGES_MAP = hz.get_map(distributed_map_name).blocking()

    uvicorn.run(app, port=args.service_port)
