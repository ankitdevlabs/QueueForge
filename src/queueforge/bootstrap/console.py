from pathlib import Path

import uvicorn
from alembic import command
from alembic.config import Config
from loguru import logger

from queueforge.bootstrap.main import QueueForgeStartup


class QueueForgeCliCommand:
    def __init__(self):
        self.startup = QueueForgeStartup(testing=False)
        self.alembic = AlembicCommand(self.get_alembic_config())

    def serve(self, host: str = "127.0.0.1", port: int = 8080) -> None:
        logger.info(f"Serving on {host}:{port}")
        uvicorn.run(
            self._get_app_runner(), host=host, port=port, log_level="info", reload=True
        )

    def get_alembic_config(self):
        app_path = Path(__file__).resolve().parent.parent
        config = Config(f"{app_path.parent.parent}/alembic.ini")
        config.set_main_option("sqlalchemy.url", self.startup.settings.pg_dsn)  # type: ignore
        config.set_main_option("database_schema", "public")
        config.set_main_option("script_location", f"{app_path}/alembic")
        return config

    def _get_app_runner(self) -> str:
        return "queueforge.bootstrap.runner:app"


class AlembicCommand:
    """alembic migration commands."""

    def __init__(self, alembic_config: Config):
        self.alembic_cfg = alembic_config

    def current(self) -> None:
        """Show current revision"""
        command.current(self.alembic_cfg)

    def heads(self, verbose: bool = False) -> None:
        """Show current head revision"""
        command.heads(self.alembic_cfg, verbose=verbose)

    def history(self) -> None:
        """Show revision history."""
        command.history(self.alembic_cfg)

    def init_revision(
        self,
        message: str,
        branch_label: str,
        version_path: str,
        head: str = "base",
    ) -> None:
        """Initialize a branch."""
        command.revision(
            self.alembic_cfg,
            message=message,
            autogenerate=False,
            head=head,
            branch_label=branch_label,
            version_path=version_path,
        )

    def make_migrations(
        self,
        message: str,
        branch_label: str | None = None,
        depends: str | None = None,
        auto: bool = False,
    ) -> None:
        """Create migration script."""
        # _head = f"{branch_label}@head"
        command.revision(
            self.alembic_cfg,
            autogenerate=auto,
            message=message,
            # head=_head,
            depends_on=depends,
        )

    def downgrade(self, revision: str) -> None:
        """Downgrade revision."""
        command.downgrade(self.alembic_cfg, revision=revision)

    def branches(self, verbose: bool = False) -> None:
        """List all branches."""
        command.branches(self.alembic_cfg, verbose=verbose)

    def show(self, rev: str) -> None:
        """Show revision info."""
        command.show(self.alembic_cfg, rev=rev)

    def migrate(self, revision: str = "head", sql: bool = False) -> None:
        """Upgrade to a revision."""
        command.upgrade(self.alembic_cfg, revision=revision, sql=sql, tag=None)

    def merge(self, rev1: str, rev2: str, message: str = "merge heads") -> None:
        """Merge two heads together."""
        command.merge(self.alembic_cfg, revisions=(rev1, rev2), message=message)
