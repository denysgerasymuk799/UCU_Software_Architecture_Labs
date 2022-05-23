import os
import uuid
import consul
import hazelcast
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain_logic.utils import use_response_template, Message, get_all_service_urls
from domain_logic.facade_service import _get_messages, _add_message


# Load env file with PORT and ADDRESS
load_dotenv(dotenv_path='./facade_service.env')

# Initial configurations
app = FastAPI(title='Facade-service')
SERVICE_NAME = 'facade_service'
SERVICE_ID = f'{SERVICE_NAME}_{uuid.uuid1().__str__()}'

# Configure consul values
consul_client = consul.Consul(
    host='127.0.0.1',
    port=8500
)

# Register a new instance of service in Consul
consul_client.agent.service.register(
    name=SERVICE_NAME,
    service_id=SERVICE_ID,
    address=os.getenv('ADDRESS'),
    port=int(os.getenv('PORT')),
)

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster
cluster_members_addresses = get_all_service_urls(consul_client, service_name='hazelcast/hz_node')
hz = hazelcast.HazelcastClient(cluster_members=cluster_members_addresses)


@app.exception_handler(Exception)
def validation_exception_handler(request: Request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.get('/get_messages', response_class=JSONResponse)
async def get_messages():
    """
    Get all messages from logging-service and response on GET request from messages-service

    :return: Concatenated responses from services in JSON format
    """
    return await _get_messages(consul_client)


@app.post('/add_message')
async def add_message(msg: Message):
    """
    Add a message to in-memory dict in logging-service.
    Note if input message type is numeric, so it will be casted to string,
     but if it is an object, then you get type error.

    :return: JSON with status and response text
    """
    msg = msg.dict()['message']
    if not isinstance(msg, str):
        status = 400
        response = use_response_template(status=status, resp_msg="Incorrect input argument")
        return JSONResponse(content=response, status_code=status)

    return await _add_message(consul_client, msg)


@app.on_event("shutdown")
def shutdown_event():
    print("Service deregistering ...")
    consul_client.agent.service.deregister(SERVICE_ID)
