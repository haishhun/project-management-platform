from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import EmailAlreadyExistsException
from app.core.security import hash_password
from app.models import User
from app.repositories import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def register(
        self, email: str, password: str, first_name: str, last_name: str
    ) -> User:
        if self.users.get_by_email(email):
            raise EmailAlreadyExistsException()

        password_hash = hash_password(password)

        try:
            user = self.users.create(email, password_hash, first_name, last_name)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise EmailAlreadyExistsException()

        return user
