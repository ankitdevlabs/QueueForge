"""Postgres module for dependency injection."""

from injector import Module, provider, singleton

from queueforge.configs.settings import AppSettings
from queueforge.db_connection.sql_connection import SqlConnection


class PostgresModule(Module):
    """Postgres module for dependency injection."""

    def __init__(self, settings: AppSettings):
        self.settings = settings

    @provider
    @singleton
    def provide_db_connection(self) -> SqlConnection:
        """Configure the Postgres module."""

        return SqlConnection(self.settings)
