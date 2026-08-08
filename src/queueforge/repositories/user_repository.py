"""User Repository."""

from queueforge.db_connection.sql_connection import SqlConnection


class UserRepository:
    def __init__(self, db: SqlConnection):
        self.db = db
