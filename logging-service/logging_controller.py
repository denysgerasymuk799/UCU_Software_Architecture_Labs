import uuid
import argparse
import consul
import hazelcast
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from domain_logic.logging_service import _get_messages, _add_message
from domain_logic.utils import get_all_service_urls, get_consul_kv_value


# Initial configurations
app = FastAPI(title='Logging-service')

SERVICE_NAME = 'logging-service'
SERVICE_ID = f'{SERVICE_NAME}_{uuid.uuid1().__str__()}'


@app.get('/logging-svc/api/v1.0/get_messages', response_class=JSONResponse)
async def get_messages(request: Request):
    """
    :return: Status code and all messaged without keys from global in-memory dict
    """
    return await _get_messages(MESSAGES_MAP, request)


@app.post('/logging-svc/api/v1.0/add_message')
async def add_message(msg_dict: dict):
    """
    Add message to global in-memory dict.

    :param msg_dict: dict of format like {'uuid': 'message'}
    :return: JSON with status and response text
    """
    return await _add_message(MESSAGES_MAP, msg_dict)


@app.on_event("shutdown")
def shutdown_event():
    print("Service deregistering ...")
    consul_client.agent.service.deregister(SERVICE_ID)


if __name__ == '__main__':
    import uvicorn

    parser = argparse.ArgumentParser(description='Start logging service.')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='a host, on which to start the service')
    parser.add_argument('--port', type=int, default=8091,
                        help='a port, on which to start the service')
    args = parser.parse_args()

    # Configure consul values
    consul_client = consul.Consul(
        host='127.0.0.1',
        port=8500
    )

    # service_uuid = uuid.uuid1()
    # service_key = 'logging_service/logging_service_' + service_uuid.__str__()
    # host_ip = get_consul_kv_value(consul_client, key='logging_service/host_ip')
    # add_service_to_consul(consul_client, 'logging_service/logging_service_', service_key,
    #                       service_address=f'{host_ip}:{args.service_port}{api_root_path}')

    # host_ip = get_consul_kv_value(consul_client, key='facade_service/host_ip')

    consul_client.agent.service.register(
        name=SERVICE_NAME,
        service_id=SERVICE_ID,
        address=args.host,
        port=args.port,
        # check=consul.Check.http(url=f'{host_ip}:{args.service_port}', interval='30s')
    )

    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster
    cluster_members_addresses = get_all_service_urls(consul_client, service_name='hazelcast/hz_node')
    hz = hazelcast.HazelcastClient(cluster_members=cluster_members_addresses)

    # Create Distributed Map
    distributed_map_name = get_consul_kv_value(consul_client, key='hazelcast/hz_distributed_map')
    MESSAGES_MAP = hz.get_map(distributed_map_name).blocking()

    uvicorn.run(app, port=args.port)
