from sqlalchemy.orm import Session

from app.repositories import ProjectRepository


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.users = ProjectRepository(db)