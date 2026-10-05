import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import health_router
from app.core.logging import setup_logging
from app.core.request_logging import request_logger

setup_logging()

logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)
app.middleware("http")(request_logger)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(health_router)
logger.info("Application started")


# app.include_router(api_router, prefix=settings.API_V1_PREFIX)
@app.get("/")
def root():
    return {"message": "This is root path of the project"}
