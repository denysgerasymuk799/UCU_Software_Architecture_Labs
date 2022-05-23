import os
import uuid
import asyncio
import consul
import hazelcast

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from init_config import MESSAGES_MAP
from domain_logic.utils import use_response_template
from domain_logic.messages_service import post_messages
from domain_logic.utils import get_all_service_urls


load_dotenv(dotenv_path='./messages_service.env')

app = FastAPI(title='Messages-service')
SERVICE_NAME = 'messages-service'
SERVICE_ID = f'{SERVICE_NAME}_{uuid.uuid1().__str__()}'

# Configure consul values
consul_client = consul.Consul(
    host='127.0.0.1',
    port=8500
)

consul_client.agent.service.register(
    name=SERVICE_NAME,
    service_id=SERVICE_ID,
    address=os.getenv('ADDRESS'),
    port=int(os.getenv('PORT')),
    # check=consul.Check.http(url=f'{host_ip}:{args.service_port}', interval='30s')
)

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster
cluster_members_addresses = get_all_service_urls(consul_client, service_name='hazelcast/hz_node')
hz = hazelcast.HazelcastClient(cluster_members=cluster_members_addresses)

# Start async task to consume from topic
asyncio.create_task(post_messages(consul_client))


@app.get('/message-svc/api/v1.0/get_messages', response_class=JSONResponse)
async def get_messages():
    if len(MESSAGES_MAP) == 0:
        response_msg = "local instance map is empty"
    else:
        response_msg = ", ".join(list(MESSAGES_MAP.values()))

    status = 200
    response = use_response_template(status=status, resp_msg=response_msg)
    return JSONResponse(content=response, status_code=status)


@app.on_event("shutdown")
def shutdown_event():
    print("Service deregistering ...")
    consul_client.agent.service.deregister(SERVICE_ID)
