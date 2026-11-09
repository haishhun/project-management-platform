from uuid import UUID

from sqlalchemy.orm import Session

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
