import uuid
import argparse
import logging
import asyncio
import consul
import hazelcast
from fastapi import FastAPI

from domain_logic.custom_logger import MyHandler


def add_service_to_consul(consul_client, service_name, service_key, service_address):
    index, data = consul_client.kv.get(service_name, index=None, recurse=True)
    unique_addresses = set()
    if data:
        for item in data:
            addr = item['Value'].decode('utf-8')
            unique_addresses.add(addr)

    if service_address not in unique_addresses:
        consul_client.kv.put(key=service_key, value=service_address)


# initial configurations
app = FastAPI(title='Facade-service')

# Create event loop for asynchronous kafka producer
kafka_loop = asyncio.get_event_loop()

logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(MyHandler())


if __name__ == '__main__':
    import uvicorn

    localhost = '127.0.0.1'
    parser = argparse.ArgumentParser(description='Start facade service.')
    parser.add_argument('service_port', type=int, default=8081,
                        help='a port, on which to start the service')

    args = parser.parse_args()

    # Configure consul values
    consul_client = consul.Consul(
        host=localhost,
        port=8500
    )

    service_uuid = uuid.uuid1()
    service_key = 'facade_service_' + service_uuid.__str__()
    add_service_to_consul(consul_client, 'facade_service', service_key,
                          service_address=localhost + ":" + str(args.service_port))

    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
    hz = hazelcast.HazelcastClient(cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703"
    ])

    uvicorn.run(app, port=args.service_port)
