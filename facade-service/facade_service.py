import random
import uuid
import asyncio
import httpx
from fastapi import Request
from fastapi.responses import JSONResponse

from constants import *
from init_config import logger
from utils import use_response_template


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


async def _get_messages(request: Request):
    """
    Get all messages from logging-service and response on GET request from message-service

    :return: Concatenated responses from services in JSON format
    """
    random_logging_addr = random.choice([LOGGING_SERVICE_ADDR_1, LOGGING_SERVICE_ADDR_2, LOGGING_SERVICE_ADDR_3])
    logging_svc_url = random_logging_addr + LOGGING_SERVICE_GET_MSGS_ENTRYPOINT
    message_svc_url = MESSAGES_SERVICE_ADDR + MESSAGES_SERVICE_GET_MSGS_ENTRYPOINT

    result_str = ""
    try:
        async with httpx.AsyncClient() as client:
            tasks = [get_request(client, url) for url in [logging_svc_url, message_svc_url]]
            responses = await asyncio.gather(*tasks)
    except Exception as err:
        responses = [{"component": 'ANY_COMPONENT', '_status_code': 400, 'error': err}]

    # concatenate responses
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


async def _add_message(msg: str):
    """
    Add a message to in-memory dict in logging-service.
    Note if input message type is numeric, so it will be casted to string,
     but if it is an object, then you get type error.

    :return: JSON with status and response text
    """
    # generate message dict for logging-service
    msg_dict = {uuid.uuid1().__str__(): msg}
    logger.debug(f'Generated msg_dict: {msg_dict}')

    random_logging_addr = random.choice([LOGGING_SERVICE_ADDR_1, LOGGING_SERVICE_ADDR_2, LOGGING_SERVICE_ADDR_3])
    url = random_logging_addr + LOGGING_SERVICE_ADD_MSG_ENTRYPOINT

    try:
        async with httpx.AsyncClient() as client:
            tasks = [post_request(client, url, msg_dict)]
            responses = await asyncio.gather(*tasks)
            logger.info(f'Responses from services for GET request: {responses}')
    except Exception as err:
        responses = [{'_status_code': 400, 'error': err}]

    if responses[0]['_status_code'] == 200:
        status = 200
        response = use_response_template(status=status, resp_msg="OK")
    else:
        status = 400
        error_message = ', error: ' + str(responses[0]['error']) if responses[0].get('error', None) else ''
        response = use_response_template(status=status,
                                         resp_msg="Incorrect input argument or server does not respond" + error_message)
    return JSONResponse(content=response, status_code=status)