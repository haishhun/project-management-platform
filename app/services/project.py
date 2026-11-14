from collections.abc import Sequence
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ForbiddenException,
    ResourceDoesNotExistException,
)
from app.models import Project
from app.models.project_member import ProjectRole
from app.repositories import ProjectMemberRepository, ProjectRepository


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.project_repo = ProjectRepository(db)
        self.project_member_repo = ProjectMemberRepository(db)

    def create(
        self,
        owner_id: UUID,
        name: str,
        description: str | None = None,
    ) -> Project:

        try:
            new_project = self.project_repo.create(
                name=name,
                description=description,
            )
            self.project_member_repo.create(
                project_id=new_project.id, user_id=owner_id, role=ProjectRole.OWNER
            )
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        return new_project

    def get_by_id(self, project_id: UUID, user_id: UUID) -> Project:
        project = self.project_repo.get_by_id(project_id=project_id)
        if project is None:
            raise ResourceDoesNotExistException("The project does not exist.")
        membership = self.project_member_repo.get_by_project_and_member(
            project_id=project_id, user_id=user_id
        )
        if membership is None:
            raise ForbiddenException("Access Forbidden.")
        return project

    def list_by_user(self, user_id: UUID) -> Sequence[Project]:
        return self.project_repo.get_all_by_user(user_id=user_id)
