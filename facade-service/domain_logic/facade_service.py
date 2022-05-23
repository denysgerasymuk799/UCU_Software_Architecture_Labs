import uuid
import random
import asyncio
import httpx
from fastapi.responses import JSONResponse

from init_config import logger
from domain_logic.constants import *
from domain_logic.utils import get_all_service_urls, get_consul_kv_value
from domain_logic.utils import use_response_template
from domain_logic.kafka.service_producer import ServiceProducer


async def get_request(client: httpx.AsyncClient, url: str):
    """
    Async GET request
    """
    response = await client.get(url)
    logger.info(f'Responses from services for GET request: \nheaders: {response.headers}\ncontext: {response.json()}\n')
    return response.json()


async def post_request(client: httpx.AsyncClient, url: str, msg_dict: dict):
    """
    Async POST request
    """
    response = await client.post(url, json=msg_dict)
    logger.info(f'Responses from services for POST request: \n'
                f'headers: {response.headers}\ncontext: {response.json()}\n')
    return response.json()


async def _get_messages(consul_client):
    """
    Get all messages from logging-service and response on GET request from messages-service

    :return: Concatenated responses from services in JSON format
    """
    logging_service_addresses = get_all_service_urls(consul_client, service_name='logging_service')
    messages_service_addresses = get_all_service_urls(consul_client, service_name='messages_service')
    print('logging_service_addresses -- ', logging_service_addresses)
    print('messages_service_addresses -- ', messages_service_addresses)

    random_logging_svc_addr = random.choice(logging_service_addresses)
    random_message_svc_addr = random.choice(messages_service_addresses)
    logging_svc_url = random_logging_svc_addr + get_consul_kv_value(consul_client, key=LOGGING_SERVICE_GET_MSGS_ENDPOINT_KEY)
    message_svc_url = random_message_svc_addr + get_consul_kv_value(consul_client, key=MESSAGES_SERVICE_GET_MSGS_ENDPOINT_KEY)

    result_str = ""
    try:
        async with httpx.AsyncClient() as client:
            tasks = [get_request(client, url) for url in [logging_svc_url, message_svc_url]]
            responses = await asyncio.gather(*tasks)
    except Exception as err:
        responses = [{"component": 'ANY_COMPONENT', '_status_code': 400, 'error': err}]

    # Concatenate responses
    for resp in responses:
        if resp['_status_code'] == 200:
            result_str += f'Response from {resp["component"]}: {resp["response"]}\n'
        else:
            status = 400
            error_message = ', error: ' + str(resp['error']) if resp.get('error', None) else ''
            response = use_response_template(status=status,
                                             resp_msg=f'Bad request from {resp["component"]}{error_message}')
            return JSONResponse(content=response, status_code=status)

    status = 200
    response = use_response_template(status=status, resp_msg=result_str)
    return JSONResponse(content=response, status_code=status)


async def _add_message_in_logging_svc(consul_client, msg_dict: dict):
    logging_service_addresses = get_all_service_urls(consul_client, service_name='logging_service')
    print('logging_service_addresses -- ', logging_service_addresses)
    random_logging_addr = random.choice(logging_service_addresses)
    url = random_logging_addr + get_consul_kv_value(consul_client, key=LOGGING_SERVICE_ADD_MSG_ENDPOINT_KEY)
    print('url -- ', url)

    try:
        async with httpx.AsyncClient() as client:
            tasks = [post_request(client, url, msg_dict)]
            responses = await asyncio.gather(*tasks)
            logger.info(f'Responses from services for GET request: {responses}')
    except Exception as err:
        responses = [{'_status_code': 400, 'error': err}]
        
    return responses


async def _add_message_in_message_svc(consul_client, msg: str):
    try:
        producer = ServiceProducer("ServiceProducer", kafka_broker_addr=get_consul_kv_value(consul_client, key=KAFKA_BROKER_KEY))
        message_ = {
            "message": msg
        }
        # Send a message to the topic, which is read by consumer group from Message service side
        await producer.send(get_consul_kv_value(consul_client, key=MESSAGE_SVC_TOPIC_KEY), message_)
        return 0
    except Exception as err:
        logger.error(f'kafka producer.send error -- {err}')
        return -1
    

async def _add_message(consul_client, msg: str):
    """
    Add a message to in-memory dict in logging-service.
    Note if input message type is numeric, so it will be casted to string,
     but if it is an object, then you get type error.

    :return: JSON with status and response text
    """
    # Generate message dict for logging-service
    msg_dict = {uuid.uuid1().__str__(): msg}
    logger.debug(f'Generated msg_dict: {msg_dict}')

    logging_svc_responses = await _add_message_in_logging_svc(consul_client, msg_dict)
    message_svc_response = await _add_message_in_message_svc(consul_client, msg)

    print('logging_svc_responses -- ', logging_svc_responses)
    print('message_svc_response -- ', message_svc_response)

    if logging_svc_responses[0]['_status_code'] == 200 and message_svc_response == 0:
        status = 200
        response = use_response_template(status=status, resp_msg="OK")
    else:
        status = 400
        error_message = ', error: ' + str(logging_svc_responses[0]['error']) if logging_svc_responses[0].get('error', None) else ''
        response = use_response_template(status=status,
                                         resp_msg="Incorrect input argument or server does not respond" + error_message)
    return JSONResponse(content=response, status_code=status)
