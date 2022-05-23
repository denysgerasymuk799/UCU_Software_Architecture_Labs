from fastapi import Request
from fastapi.responses import JSONResponse

from init_config import logger
from domain_logic.utils import use_response_template


async def _get_messages(messages_map, request: Request):
    """
    :return: Status code and all messaged without keys from global in-memory dict
    """
    status = 200
    response = use_response_template(status=status, resp_msg=", ".join(list(messages_map.values())))
    return JSONResponse(content=response, status_code=status)


async def _add_message(messages_map, msg_dict: dict):
    """
    Add message to global in-memory dict.

    :param msg_dict: dict of format like {'uuid': 'message'}
    :return: JSON with status and response text
    """
    # Note that dict in python is not concurrent because of GIL.
    # More details: https://stackoverflow.com/questions/48124257/python-equivalent-of-concurrenthashmap-from-java
    uuid, msg = list(msg_dict.items())[0]
    if isinstance(uuid, str) and isinstance(msg, str):
        messages_map.put(uuid, msg)
        logger.info(f'Got message: {msg}')

        status = 200
        response = use_response_template(status=status, resp_msg="OK")
    else:
        status = 400
        response = use_response_template(status=status, resp_msg="Incorrect input argument")
    return JSONResponse(content=response, status_code=status)
