import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["health"])


@router.get("/db")
def check_database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.exception("Database health check failed")
        raise HTTPException(status_code=503, detail="PostgreSQL is unavailable")
    return {"status": "ok"}


@router.get("/live")
def check_api_health():
    return {"status": "ok"}


@router.get("/ready")
def check_application_readiness(db: Session = Depends(get_db)):
    check_database_health(db)
    return {"status": "ready"}
