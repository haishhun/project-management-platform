from sqlalchemy.orm import Session


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
