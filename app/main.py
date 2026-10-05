from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import health_router
from app.core.logging import setup_logging
import logging

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)
app.include_router(health_router)
logger.info("Application started")


# app.include_router(api_router, prefix=settings.API_V1_PREFIX)
@app.get("/")
def root():
    return {"message": "This is root path of the project"}
