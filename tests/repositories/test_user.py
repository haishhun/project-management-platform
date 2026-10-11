from uuid import UUID

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ResourceDoesNotExistException
from app.repositories import UserRepository


def test_create_and_get_by_id(session):
    repo = UserRepository(session)
    user = repo.create(
        first_name="Test1", last_name="Test2", email="a@test.com", password_hash="x"
    )
    assert repo.get_by_id(user.id).email == "a@test.com"


def test_create_and_get_by_email(session):
    repo = UserRepository(session)
    user = repo.create(
        first_name="Test1", last_name="Test2", email="a@test.com", password_hash="x"
    )
    assert repo.get_by_email(user.email).first_name == "Test1"


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


def test_user_update(session):
    repo = UserRepository(session)
    user = repo.create(
        first_name="Test1",
        last_name="Test2",
        email="a@test.com",
        password_hash="x",
    )

    updated_user = repo.update(
        user.id,
        first_name="Updated1",
        last_name="Updated2",
        email="updated@test.com",
    )

    assert updated_user.id == user.id
    assert updated_user.first_name == "Updated1"
    assert updated_user.last_name == "Updated2"
    assert updated_user.email == "updated@test.com"


def test_user_partial_update(session):
    repo = UserRepository(session)
    user = repo.create(
        first_name="Test1",
        last_name="Test2",
        email="a@test.com",
        password_hash="x",
    )

    updated_user = repo.update(
        user.id,
        first_name="Updated1",
    )

    assert updated_user.first_name == "Updated1"
    assert updated_user.last_name == "Test2"
    assert updated_user.email == "a@test.com"


def test_user_update_not_found(session):
    repo = UserRepository(session)

    with pytest.raises(ResourceDoesNotExistException):
        repo.update(
            UUID("579d2ad8-30a4-4bcd-b98a-484b1faa44e1"),
            first_name="Updated1",
        )


def test_user_delete(session):
    repo = UserRepository(session)
    user = repo.create(
        first_name="Test1", last_name="Test2", email="a@test.com", password_hash="x"
    )
    repo.delete(user.id)

    assert repo.get_by_id(user.id) is None


def test_user_delete_not_found(session):
    repo = UserRepository(session)
    with pytest.raises(ResourceDoesNotExistException):
        repo.delete(UUID("579d2ad8-30a4-4bcd-b98a-484b1faa44e1"))
