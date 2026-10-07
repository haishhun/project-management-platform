from unittest.mock import Mock

from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import SessionLocal, get_db
from app.main import app

client = TestClient(app)


def test_database_connection():
    db = SessionLocal()

    try:
        query = db.execute(text("SELECT 1"))
        result = query.scalar_one()

        assert result == 1
    finally:
        db.close()


def test_database_health_endpoint():
    response = client.get("/health/db")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_database_health_endpoint_when_db_unavailable():
    mock_db = Mock()
    mock_db.execute.side_effect = SQLAlchemyError()

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = client.get("/health/db")

        assert response.status_code == 503
        assert response.json() == {"detail": "PostgreSQL is unavailable"}
    finally:
        app.dependency_overrides.clear()


def test_api_health_endpoint():
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_ready_endpoint():
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
