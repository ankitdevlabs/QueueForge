import uvicorn
from loguru import logger


class QueueForgeCliCommand:
    def serve(self, host: str = "127.0.0.1", port: int = 8080) -> None:
        logger.info(f"Serving on {host}:{port}")
        uvicorn.run(
            self._get_app_runner(), host=host, port=port, log_level="info", reload=True
        )

    def _get_app_runner(self) -> str:
        return "queueforge.bootstrap.runner:app"
