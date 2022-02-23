import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from custom_logger import MyHandler
from utils import use_response_template

# initial configurations
app = FastAPI(title='Logging-service')
MESSAGES_MAP = dict()

logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(MyHandler())


@app.get('/logging-svc/api/v1.0/get_messages', response_class=JSONResponse)
async def get_messages(request: Request):
    """
    :return: Status code and all messaged without keys from global in-memory dict
    """
    status = 200
    response = use_response_template(status=status, resp_msg=", ".join(list(MESSAGES_MAP.values())))
    return JSONResponse(content=response, status_code=status)


@app.post('/logging-svc/api/v1.0/add_message')
async def add_message(msg_dict: dict):
    """
    Add message to global in-memory dict.

    :param msg_dict: dict of format like {'uuid': 'message'}
    :return: JSON with status and response text
    """
    # Note that dict in python is not concurrent because of GIL.
    # More details: https://stackoverflow.com/questions/48124257/python-equivalent-of-concurrenthashmap-from-java
    uuid, msg = list(msg_dict.items())[0]
    if isinstance(uuid, str) and isinstance(msg, str):
        MESSAGES_MAP[uuid] = msg
        logger.info(f'Got message: {msg}')

        status = 200
        response = use_response_template(status=status, resp_msg="OK")
    else:
        status = 400
        response = use_response_template(status=status, resp_msg="Incorrect input argument")
    return JSONResponse(content=response, status_code=status)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8081)
