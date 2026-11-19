"""set task creator to null when user is deleted

Revision ID: 87c61a247585
Revises: 7e050834af80
Create Date: 2026-11-19 12:20:48.522771

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "87c61a247585"
down_revision: str | Sequence[str] | None = "7e050834af80"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("tasks", "created_by_id", existing_type=sa.UUID(), nullable=True)
    op.drop_constraint("tasks_created_by_id_fkey", "tasks", type_="foreignkey")
    op.create_foreign_key(
        "tasks_created_by_id_fkey",
        "tasks",
        "users",
        ["created_by_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("tasks_created_by_id_fkey", "tasks", type_="foreignkey")
    op.create_foreign_key(
        "tasks_created_by_id_fkey",
        "tasks",
        "users",
        ["created_by_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.alter_column("tasks", "created_by_id", existing_type=sa.UUID(), nullable=False)
