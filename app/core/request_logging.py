import logging
import time

from fastapi import Request

logger = logging.getLogger(__name__)


async def request_logger(request: Request, call_next):
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