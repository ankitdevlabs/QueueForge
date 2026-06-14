from abc import ABC, abstractmethod

from sqlalchemy import Engine
from sqlalchemy.orm import Session


class DatabaseConnection(ABC):
    """Interface for database connections."""

    @abstractmethod
    def get_engine(self) -> Engine:
        """Return the database engine."""
        pass

    @abstractmethod
    def get_session(self) -> Session:
        """Return a database session."""
        pass

    @abstractmethod
    def create_all(self) -> None:
        """Create all database tables."""
        pass

    @abstractmethod
    def drop_all(self) -> None:
        """Drop all database tables."""
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """Test the database connection. Returns True if successful."""
        pass
