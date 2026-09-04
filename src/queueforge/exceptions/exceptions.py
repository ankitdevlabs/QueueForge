class CoreException(Exception):
    """Base exception class for QueueForge application."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class InvalidSettingException(CoreException):
    """Invalid setting class"""

    def __init__(self) -> None:
        super().__init__("Invalid setting class. Should be instance of CoreSettings.")


class InvalidRequestError(CoreException):
    def __init__(self, message: str = "Invalid Input"):
        super().__init__(message)


class AlreadyExistsError(CoreException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message)
