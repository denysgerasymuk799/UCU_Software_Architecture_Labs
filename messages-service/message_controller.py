import asyncio
from multiprocessing import Process
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from fastapi import BackgroundTasks
from fastapi_utils.tasks import repeat_every

from contextlib import suppress

from init_config import app, MESSAGES_MAP
from domain_logic.utils import use_response_template
from domain_logic.message_service import post_messages


# @app.on_event("startup")
# async def startup_event():
#     background_tasks = BackgroundTasks()
#     background_tasks.add_task(main)
#     # p1 = Process(target=post_messages())
#     # p1.start()
#     # loop = asyncio.new_event_loop()


#     # loop.create_task(post_messages())
#     # loop.create_task(post_messages())
#
#     loop.run_in_executor(None, post_messages)
#
#     asyncio.create_task(post_messages())
#     asyncio.create_task(asyncio.ensure_future(post_messages()))
#     asyncio.ensure_future(post_messages())


# async def main():
#     await run_in_threadpool(lambda: post_messages())


# async def main():
#     t = asyncio.create_task(post_messages())
#     await t
#     print(f't: type {type(t)}')
#     print(f't done: {t.done()}')

# asyncio.Task(post_messages())

# async def main():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(await post_messages())
#
# asyncio.create_task(main())


@app.get('/message-svc/api/v1.0/get_messages', response_class=JSONResponse)
async def get_messages():
    print('Entered GET endpoint')
    if len(MESSAGES_MAP) == 0:
        response_msg = "local instance map is empty"
    else:
        response_msg = ", ".join(list(MESSAGES_MAP.values()))

    status = 200
    response = use_response_template(status=status, resp_msg=response_msg)
    return JSONResponse(content=response, status_code=status)


# loop = asyncio.new_event_loop()
# loop.create_task(post_messages())

# loop.create_task(post_messages())


import uuid
from init_config import queue, logger, MESSAGES_MAP


@repeat_every(seconds=0.1)
async def main():
    print('start post_message')
    head = queue.take()
    print('head -- ', head)
    if isinstance(head, str):
        logger.info(f'Consuming message: {head}')
        # Note that dict in python is thread-safe and not concurrent because of GIL. More details:
        # https://stackoverflow.com/questions/48124257/python-equivalent-of-concurrenthashmap-from-java
        MESSAGES_MAP[uuid.uuid1().__str__()] = head

    # task = asyncio.Task(post_messages())

    # # let script some thime to work:
    # await asyncio.sleep(3)

    # # cancel task to avoid warning:
    # task.cancel()
    # with suppress(asyncio.CancelledError):
    #     await task  # await for task cancellation


# loop = asyncio.get_event_loop()
# task = loop.create_task(post_messages())
#
# try:
#     loop.run_until_complete(task)
# except asyncio.CancelledError:
#     pass
# loop.run_until_complete(main())

# try:
#     loop.run_until_complete(main())
# finally:
#     # loop.run_until_complete(loop.shutdown_asyncgens())
#     loop.close()
