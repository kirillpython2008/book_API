from fastapi import Request, Response
from typing import Callable


async def middleware(request: Request, call_next: Callable):
    print("middleware")

    result = await call_next(request)
    return result
