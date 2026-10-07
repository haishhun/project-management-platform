import logging
from contextlib import asynccontextmanager

from fastapi import Request
from fastapi.responses import JSONResponse

from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from app.core.config import settings
from app.api.routes import health_router
from app.core.logging import setup_logging
from app.core.request_logging import request_logger
from asgi_correlation_id import CorrelationIdMiddleware, correlation_id
from sqlalchemy import text
from app.db.session import engine

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except OperationalError:
        logger.exception("Database connection failed at startup")
        raise
    logger.info("Startup complete.")
    try:
        yield
    finally:
        logger.info("Shutting down...")
        engine.dispose()
        logger.info("Shutdown complete.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)
app.middleware("http")(request_logger)
app.add_middleware(CorrelationIdMiddleware, header_name="X-Request-ID")


def _rid_headers() -> dict[str, str]:
    return {"X-Request-ID": correlation_id.get() or ""}


@app.exception_handler(OperationalError)
async def database_connection_exception_handler(
    request: Request, exc: OperationalError
):
    logger.exception(
        "Database connection failed on %s %s", request.method, request.url.path
    )
    return JSONResponse(
        status_code=503,
        content={"detail": "Service temporarily unavailable."},
        headers=_rid_headers(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
        headers=_rid_headers(),
    )


app.include_router(health_router)


# app.include_router(api_router, prefix=settings.API_V1_PREFIX)
@app.get("/")
def root():
    return {"message": "This is root path of the project"}
