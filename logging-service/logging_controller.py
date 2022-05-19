from fastapi import Request
from fastapi.responses import JSONResponse

from init_config import app
from domain_logic.logging_service import _get_messages, _add_message


@app.get('/logging-svc/api/v1.0/get_messages', response_class=JSONResponse)
async def get_messages(request: Request):
    """
    :return: Status code and all messaged without keys from global in-memory dict
    """
    return await _get_messages(request)


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
    uvicorn.run(app, port=8091)
