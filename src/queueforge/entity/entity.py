"""Base Entity."""

from abc import abstractmethod
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field

from queueforge.entity.identifier import Identifier


class Entity(BaseModel):
    """Base class for entities."""

    id: Identifier = Field(..., description="Unique identifier for the entity")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        description="Timestamp when the entity was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        description="Timestamp when the entity was last updated",
    )

    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
        validate_assignment=True,
    )

    @abstractmethod
    def generate_id(self) -> Identifier:
        """Generate a unique identifier for the entity."""
        raise NotImplementedError("Subclasses must implement generate_id method")
