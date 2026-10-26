from uuid import UUID, uuid4

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


def test_get_by_id_returns_none_when_missing(session):
    assert (
        UserRepository(session).get_by_id(UUID("579d2ad8-30a4-4bcd-b98a-484b1faa44e1"))
        is None
    )


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


def test_user_update_duplicate_email_fails(session):
    repo = UserRepository(session)

    user1 = repo.create(
        email="first@test.com",
        password_hash="hash1",
        first_name="First",
        last_name="User",
    )
    user2 = repo.create(
        email="second@test.com",
        password_hash="hash2",
        first_name="Second",
        last_name="User",
    )

    with pytest.raises(IntegrityError):
        repo.update(user1.id, email=user2.email)

    session.rollback()


def test_user_update_without_fields_preserves_values(session):
    repo = UserRepository(session)

    user = repo.create(
        email="original@test.com",
        password_hash="original_hash",
        first_name="Original",
        last_name="User",
    )

    updated_user = repo.update(user.id)

    assert updated_user.id == user.id
    assert updated_user.email == "original@test.com"
    assert updated_user.first_name == "Original"
    assert updated_user.last_name == "User"
    assert updated_user.password_hash == "original_hash"


def test_create_can_be_rolled_back(session):
    repo = UserRepository(session)

    user = repo.create(
        email="rollback@test.com",
        password_hash="hash",
        first_name="Rollback",
        last_name="Test",
    )
    user_id = user.id

    session.rollback()

    assert repo.get_by_id(user_id) is None


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


def test_update_email_can_be_found_by_new_email(session):
    repo = UserRepository(session)

    user = repo.create(
        first_name="Test",
        last_name="User",
        email="old@test.com",
        password_hash="hash",
    )

    repo.update(user.id, email="new@test.com")

    assert repo.get_by_email("old@test.com") is None

    updated_user = repo.get_by_email("new@test.com")

    assert updated_user is not None
    assert updated_user.id == user.id


def test_update_does_not_change_password_hash(session):
    repo = UserRepository(session)

    user = repo.create(
        first_name="Test",
        last_name="User",
        email="test@test.com",
        password_hash="original_hash",
    )

    repo.update(
        user.id,
        first_name="Updated",
        email="updated@test.com",
    )

    result = repo.get_by_id(user.id)

    assert result is not None
    assert result.first_name == "Updated"
    assert result.password_hash == "original_hash"


def test_failed_duplicate_email_update_preserves_original_email(session):
    repo = UserRepository(session)

    user1 = repo.create(
        first_name="First",
        last_name="User",
        email="first@test.com",
        password_hash="hash1",
    )
    user1_id = user1.id

    user2 = repo.create(
        first_name="Second",
        last_name="User",
        email="second@test.com",
        password_hash="hash2",
    )

    session.commit()

    with pytest.raises(IntegrityError):
        repo.update(user1_id, email=user2.email)

    session.rollback()

    result = repo.get_by_id(user1_id)

    assert result is not None
    assert result.email == "first@test.com"


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
        repo.delete(uuid4())


def test_delete_does_not_delete_other_users(session):
    repo = UserRepository(session)

    user1 = repo.create(
        first_name="First",
        last_name="User",
        email="first@test.com",
        password_hash="hash1",
    )
    user2 = repo.create(
        first_name="Second",
        last_name="User",
        email="second@test.com",
        password_hash="hash2",
    )

    repo.delete(user1.id)

    assert repo.get_by_id(user1.id) is None

    remaining_user = repo.get_by_id(user2.id)

    assert remaining_user is not None
    assert remaining_user.email == "second@test.com"
