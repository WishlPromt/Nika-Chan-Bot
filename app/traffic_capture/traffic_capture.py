_request_limit = 30
_processed_request = 0

from asyncio import sleep

async def process_request():
    global _processed_request
    while _processed_request >= _request_limit:
        await clear_limit()

    _processed_request += 1
    return True


async def clear_limit():
    global _processed_request
    await sleep(1)
    if _processed_request > 0:
        _processed_request -= 1
