from fastapi import FastAPI
from app.core.config import settings
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    openapi_prefix=settings.API_V1_PREFIX


)

@app.get("/")
def root():
    return "{Hello, World}"