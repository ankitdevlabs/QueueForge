from fastapi import FastAPI
from loguru import logger


class QueueForgeStartup:
    def initialize(self) -> FastAPI:
        """Initialize the QueueForge application."""
        logger.info("Initializing QueueForge application...")
        app = FastAPI(title="QueueForge")
        # Additional setup can be done here (e.g., include routers, middleware, etc.)
        return app


def start_app(main: QueueForgeStartup) -> FastAPI:
    """Initializing the main application."""
    return main.initialize()
