from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserDTO(BaseModel):
    """Data Transfer Object for User."""

    id: UUID
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: UUID,
        name: str,
        email: str,
        created_at: datetime,
        updated_at: datetime,
    ) -> "UserDTO":
        """Factory method to create a UserDTO instance."""
        return cls(
            id=id,
            name=name,
            email=email,
            created_at=created_at,
            updated_at=updated_at,
        )
