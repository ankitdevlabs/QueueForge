from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings


class CoreSettings(BaseSettings):
    """Core settings for the QueueForge application."""

    app_id: str | None = None
    app_name: str 
    base_path: Path
    testing: bool = False

    # runtime information
    app_env: Literal["development", "testing", "production"]
    database_log_file: str | None
    debug: bool
    introspection: bool = True

    # Cors
    cors_allow_origins: list[str] = ["*"]
    cors_allow_methods: tuple[str, ...] = (
        "GET",
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
        "HEAD",
        "OPTIONS",
    )
    cors_allow_credentials: bool = False
    cors_expose_headers: list[str] = []
    cors_allow_headers: list[str] = ["*"]
    cors_max_age: int = 600


class PostgresSettings(BaseSettings):
    """postgres database related settings."""

    database_log_file: str | None = "core_database.log"

    # postgres settings
    pg_dsn: str | None = None
    pg_schema: str | None = "public"
    pg_min_size: int | None = 5
    pg_max_size: int | None = 10
    pg_use_ssl: bool | None = True
    casbin_pg_dsn: str | None = None
    pg_pool_timeout: int | None = 30
    pg_pool_recycle: int | None = 3600


class AppSettings(CoreSettings):
    """Application settings for the QueueForge application."""

    pass
