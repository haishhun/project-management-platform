import logging
import time

from fastapi import Request

logger = logging.getLogger(__name__)

QUIET_PATHS = {"/health/live"}


async def request_logger(request: Request, call_next):
    if request.url.path in QUIET_PATHS:
        response = await call_next(request)
        if response.status_code >= 400:
            logger.warning(
                "%s %s -> %s", request.method, request.url.path, response.status_code
            )
        return response

    start = time.perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
    finally:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "%s %s -> %s -> %.0fms",
            request.method,
            request.url.path,
            status_code,
            duration_ms,
        )
    return response
