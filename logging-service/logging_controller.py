from fastapi import Request
from fastapi.responses import JSONResponse

from utils import use_response_template
from init_config import app, MESSAGES_MAP
from logging_service import _add_message


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
    return await _add_message(msg_dict)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8082)
