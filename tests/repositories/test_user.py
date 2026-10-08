import pytest
from sqlalchemy.exc import IntegrityError

from app.repositories import UserRepository


def test_create_and_get_by_id(session):
    repo = UserRepository(session)
    user = repo.create(
        first_name="Test1", last_name="Test2", email="a@test.com", password_hash="x"
    )
    assert repo.get_by_id(user.id).email == "a@test.com"


def test_get_by_email_returns_none_when_missing(session):
    assert UserRepository(session).get_by_email("nope@test.com") is None


def test_create_duplicate_email_fails(session):
    repo = UserRepository(session)
    repo.create(
        first_name="Test1", last_name="Test2", email="a@test.com", password_hash="x"
    )
    with pytest.raises(IntegrityError):
        repo.create(
            first_name="Test1", last_name="Test2", email="a@test.com", password_hash="y"
        )
