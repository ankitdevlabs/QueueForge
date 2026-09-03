from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from queueforge.command.commands import ResourceStatus
from queueforge.models.models import BaseModel


class UserModel(BaseModel):
    """User model that defines the structure of the user data."""

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(225), nullable=False)
    email: Mapped[str] = mapped_column(String(225), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(225), nullable=False)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=ResourceStatus.ACTIVE,
    )
