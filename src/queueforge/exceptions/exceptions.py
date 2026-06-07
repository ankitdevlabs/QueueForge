class CoreException(Exception):
    """Base exception class for QueueForge application."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class InvalidSettingException(CoreException):
    """Invalid setting class"""

    def __init__(self) -> None:
        super().__init__("Invalid setting class. Should be instance of CoreSettings.")
