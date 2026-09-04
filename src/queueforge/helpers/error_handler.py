"""Error Handler module that provides a ResponseHandler class for creating standardized responses for API endpoints."""

from typing import TypeVar

from fastapi import status
from pydantic import BaseModel

from queueforge.bootstrap.modules.service.service import GenericService

T = TypeVar("T", bound=BaseModel)


class Error(BaseModel):
    """Error class that defines the structure of the error message for API responses."""

    code: int
    message: str
    error_key: str | None = None


class ResponseModel[T](BaseModel):
    """Response Model class that defines the structure of the response for API endpoints."""

    status: int
    data: list[T] | T | None = None
    error: Error | None = None


class ResponseHandler(GenericService):
    """Response Handler class that provides methods for creating standardized responses for API endpoints."""

    def create_response(
        self,
        data: list[T] | T | None = None,
        error: Exception | str | None = None,
        status_code: int = status.HTTP_200_OK,
        error_key: str | None = None,
    ) -> dict:
        """Create a standardized response for API endpoints.

        Args:
            data (dict | None): The data to include in the response. Defaults to None.
            error (Exception | None): The exception to include in the response. Defaults to None.
            status_code (int): The HTTP status code for the response. Defaults to 200.
            error_key (str | None): The key to use for the error message in the response. Defaults to None.
        Returns:
            dict: A dictionary containing the standardized response for the API endpoint.
        """
        if isinstance(error, Exception):
            self.logger.error(error)
            error_response = Error.model_construct(
                message=error.__dict__.get("message")
                or error.__dict__.get("_message")
                or str(error)
                or "Invalid input",
                code=status_code,
                error_key=error_key,
            )
            return ResponseModel(status=status_code, error=error_response).model_dump()

        if isinstance(error, str):
            error_response = Error.model_construct(
                message=error, code=status_code, error_key=error_key
            )
            return ResponseModel(status=status_code, error=error_response).model_dump()

        return ResponseModel(data=data, status=status_code).model_dump(mode="json")
