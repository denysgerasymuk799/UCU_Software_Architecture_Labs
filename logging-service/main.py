from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI()
MESSAGES_MAP = dict()


@app.get('/logging-svc/api/v1.0/get_messages', response_class=JSONResponse)
async def get_messages(request: Request):
    status = 200
    response = {
        "_status_code": status,
        "response": ", ".join(list(MESSAGES_MAP.values()))
    }
    return JSONResponse(content=response, status_code=status)


@app.post('/logging-svc/api/v1.0/add_message')
async def add_message(msg_dict: dict):
    # https://stackoverflow.com/questions/48124257/python-equivalent-of-concurrenthashmap-from-java
    uuid, msg = list(msg_dict.items())[0]
    if isinstance(uuid, str) and isinstance(msg, str):
        MESSAGES_MAP[uuid] = msg
        status = 200
        response = {
            "_status_code": status,
            "response": "OK"
        }
    else:
        status = 400
        response = {
            "_status_code": status,
            "response": "Incorrect input argument"
        }
    return JSONResponse(content=response, status_code=status)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8081)
