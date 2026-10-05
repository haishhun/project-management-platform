
from sqlalchemy import text

from app.db.session import SessionLocal


def test_database_connection():
    db = SessionLocal()

    try:
        query = db.execute(text("SELECT 1"))
        result = query.scalar_one()

        assert result == 1

    finally:
        db.close()