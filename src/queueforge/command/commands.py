from enum import StrEnum

from pydantic import BaseModel


class Command(BaseModel):
    """Abstract base class for commands."""


class RegisterUserRequest(Command):
    """Command for registering a new user."""

    name: str
    email: str
    password: str


class ResourceStatus(StrEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ARCHIVED = "Archived"
