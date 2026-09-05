"""Base Identifier and UUID Identifier."""

import uuid

from pydantic import BaseModel


class Identifier(BaseModel):
    """Base class for generic identifier."""

    value: object

    @classmethod
    def generate(cls) -> "Identifier":
        raise NotImplementedError(
            "generate method must be implemented in subclasses of Identifier"
        )

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value


class UUIDIdentifier(Identifier):
    """Subclass of Identifier to generate UUID identifiers."""

    value: uuid.UUID

    @classmethod
    def generate(cls) -> "UUIDIdentifier":
        return cls(value=uuid.uuid4())

    @classmethod
    def is_valid(cls, value: uuid.UUID | str) -> bool:
        if isinstance(value, uuid.UUID):
            return True

        if isinstance(value, str):
            try:
                uuid.UUID(value)
            except ValueError:
                return False
            return True

        return False
