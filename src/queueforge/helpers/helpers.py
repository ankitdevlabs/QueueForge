from typing import TypeVar

from fastapi import status
from pydantic import BaseModel, ValidationError

from queueforge.exceptions.exceptions import InvalidRequestError
from queueforge.helpers.error_handler import ResponseHandler

T = TypeVar("T", bound=BaseModel)


def validate_model(data: dict, model_class: type[T]) -> T:
    """Validate the input data against the specified model class."""
    try:
        return model_class(**data)
    except ValidationError as e:
        raise InvalidRequestError(get_validation_error(e, model_class)) from e


def get_validation_error(error, modal_class: type) -> str:
    """Get the validation error message for the specified model class."""
    base_message = f"Validation failed for {modal_class.__name__}: {error}"

    if isinstance(error, str):
        return f"{base_message} - {error}"

    if isinstance(error, ValidationError):
        fields = [err["loc"][0] for err in error.errors()]
        return f"{base_message} Fields with issues: {fields}"

    return f"{base_message} Unknown error: {error}"


def create_response(
    data: list[T] | T | None = None,
    error: Exception | None = None,
    status_code: int = status.HTTP_200_OK,
    error_key: str | None = None,
) -> dict:
    handler = ResponseHandler()

    return handler.create_response(
        data=data,
        error=error,
        status_code=status_code,
        error_key=error_key,
    )
