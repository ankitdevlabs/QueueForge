from abc import ABC

from loguru import logger

from queueforge.configs.settings import AppSettings


class GenericService(ABC):
    """Interface for generic services."""

    def __init__(self) -> None:
        super().__init__()
        self._settings = None
        self._app_context = None
        self.logger = logger

    @property
    def settings(self) -> AppSettings | None:
        """Get the application settings."""
        return self._settings

    @settings.setter
    def settings(self, value: AppSettings) -> None:
        """Set the application settings."""
        self._settings = value

    @property
    def app_context(self) -> object | None:
        """Get the application context."""
        return self._app_context

    @app_context.setter
    def app_context(self, value: object) -> None:
        """Set the application context."""
        self._app_context = value

    def get_identifier(self) -> str:
        """Get the identifier for the service."""
        return self.__class__.__name__
