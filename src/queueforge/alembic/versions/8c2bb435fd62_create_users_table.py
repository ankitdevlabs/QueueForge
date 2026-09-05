"""create users table

Revision ID: 8c2bb435fd62
Revises:
Create Date: 2026-08-08 23:22:48.721287

"""

import uuid
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8c2bb435fd62"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.UUID,
            default=uuid.uuid4,
            primary_key=True,
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password", sa.String(length=225), nullable=False),
        sa.Column("is_verified", sa.Boolean, nullable=False, default=False),
        sa.Column("status", sa.String(length=50), nullable=False, default="Active"),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at",
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
