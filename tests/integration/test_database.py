from unittest.mock import Mock

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.main import app


def test_database_connection(session):
    assert session.execute(text("SELECT 1")).scalar_one() == 1


def test_database_health_endpoint_when_db_unavailable(client):
    mock_db = Mock()
    mock_db.execute.side_effect = SQLAlchemyError()

    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.get("/health/db")

    assert response.status_code == 503
    assert response.json() == {"detail": "PostgreSQL is unavailable"}
