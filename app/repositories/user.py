from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, email: str, password_hash: str, first_name: str, last_name: str
    ) -> User:
        new_user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
        )
        self.db.add(new_user)
        self.db.flush()
        return new_user

    def get_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where(User.id == user_id)
        result = self.db.execute(query)
        return result.scalar_one_or_none()

    def get_by_email(self, user_email: str) -> User | None:
        query = select(User).where(User.email == user_email)
        result = self.db.execute(query)
        return result.scalar_one_or_none()
