import uuid
import aiohttp
import asyncio

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from flask import jsonify
from pydantic import BaseModel


class Message(BaseModel):
    message: str


app = FastAPI()
# session = None

# constants
MESSAGES_SERVICE_ADDR = 'http://localhost:8082/message-svc/api/v1.0'
LOGGING_SERVICE_ADDR = 'http://localhost:8081/logging-svc/api/v1.0'
LOGGING_SERVICE_GET_MSGS_ENTRYPOINT = '/get_messages'
LOGGING_SERVICE_ADD_MSG_ENTRYPOINT = '/add_message'
MESSAGES_SERVICE_GET_MSGS_ENTRYPOINT = '/get_messages'
MESSAGES_SERVICE_ADD_MSG_ENTRYPOINT = '/add_message'


# @app.on_event('startup')
# async def startup_event():
#     global session
#     session = aiohttp.ClientSession()
#
#
# @app.on_event('shutdown')
# async def shutdown_event():
#     await session.close()


class HttpClient:
    session: aiohttp.ClientSession = None

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    def __call__(self) -> aiohttp.ClientSession:
        assert self.session is not None
        return self.session


http_client = HttpClient()


@app.on_event("startup")
async def startup():
    http_client.start()


@app.get('/get_messages', response_class=JSONResponse)
async def get_messages(request: Request):
    status = 200
    response = {
        "_status_code": status,
        "response": ''
    }
    return JSONResponse(content=response, status_code=status)


@app.post('/add_message')
async def add_message(msg: Message, new_http_client: aiohttp.ClientSession = Depends(http_client)):
    print('start')
    msg = msg.dict()['message']
    if not isinstance(msg, str):
        status = 400
        response = {
            "_status_code": status,
            "response": "Incorrect input argument"
        }
        return JSONResponse(content=response, status_code=status)

    msg_dict = {repr(uuid.uuid1()): msg}
    print('msg_dict -- ', msg_dict)
    url = LOGGING_SERVICE_ADDR + LOGGING_SERVICE_ADD_MSG_ENTRYPOINT

    response = await new_http_client.post(url, data=jsonify(msg_dict))
    print(response.json())
    # async with session.post(url, data=jsonify(msg_dict)) as response:
    #     resp = await response.json()
    #     print(resp)

    status = 200
    response = {
        "_status_code": status,
        "response": "OK"
    }
    return JSONResponse(content=response, status_code=status)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8080)
