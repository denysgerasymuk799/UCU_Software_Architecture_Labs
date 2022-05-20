from fastapi import Request
from fastapi.responses import JSONResponse

from init_config import app
from domain_logic.utils import use_response_template, Message
from domain_logic.facade_service import _get_messages, _add_message


@app.exception_handler(Exception)
def validation_exception_handler(request: Request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.get('/get_messages', response_class=JSONResponse)
async def get_messages(request: Request):
    """
    Get all messages from logging-service and response on GET request from message-service

    :return: Concatenated responses from services in JSON format
    """
    return await _get_messages(request)


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

    return await _add_message(msg)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8081)
