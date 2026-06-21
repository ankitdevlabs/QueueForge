# queueforge/container.py
from dependency_injector import containers, providers

from queueforge.db_connection.sql_connection import SqlConnection


class QueueForgeContainer(containers.DeclarativeContainer):
    """Dependency injection container for QueueForge"""

    settings = providers.Object(None)

    # Sql Provider
    db = providers.Singleton(SqlConnection, settings=settings)
