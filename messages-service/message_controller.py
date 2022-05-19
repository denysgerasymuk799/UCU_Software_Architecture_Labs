import asyncio
from fastapi.responses import JSONResponse

from init_config import app, MESSAGES_MAP
from domain_logic.utils import use_response_template
from domain_logic.message_service import post_messages


loop = asyncio.get_event_loop()
asyncio.create_task(post_messages())


@app.get('/message-svc/api/v1.0/get_messages', response_class=JSONResponse)
async def get_messages():
    if len(MESSAGES_MAP) == 0:
        response_msg = "local instance map is empty"
    else:
        response_msg = ", ".join(list(MESSAGES_MAP.values()))

    status = 200
    response = use_response_template(status=status, resp_msg=response_msg)
    return JSONResponse(content=response, status_code=status)
