"""User Repository."""

from injector import inject

from queueforge.db_connection.sql_connection import SqlConnection


class UserRepository:
    """User Repository class that provides data access methods for user-related operations."""

    @inject
    def __init__(self, db: SqlConnection):
        self._db = db

    async def get_user_by_email(self, email: str):
        """Retrieve a user by email."""

    async def create_user(self, data):
        """Create a new user."""
