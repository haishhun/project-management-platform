from sqlalchemy.orm import Session

from app.models import Project


class ProjectRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, name: str) -> Project:
        new_project = Project(name=name)
        self.db.add(new_project)
        self.db.flush()
        return new_project
