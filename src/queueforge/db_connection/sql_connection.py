from loguru import logger
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from queueforge.configs.settings import AppSettings
from queueforge.db_connection.db_connection import DatabaseConnection


class SqlConnection(DatabaseConnection):
    def __init__(self, settings: AppSettings):
        self.engine = create_engine(
            url=settings.pg_dsn,  # type: ignore
            pool_pre_ping=True,
            pool_size=settings.pg_min_size,  # Maximum persistent connections
            max_overflow=settings.pg_max_size,  # Additional connections when needed
            pool_timeout=settings.pg_pool_timeout,  # Timeout when getting connection from pool
            pool_recycle=settings.pg_pool_recycle,  # Recycle connections after 1 hour
        )
        self.session = sessionmaker(bind=self.engine)

    def get_engine(self) -> Engine:
        return self.engine

    def get_session(self) -> Session:
        session = self.session()
        return session

    def create_all(self):
        pass

    def drop_all(self):
        pass

    def test_connection(self) -> bool:
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                return True
        except Exception as e:  # noqa: BLE001
            logger.error(f"Database connection failed: {e}")
            return False
