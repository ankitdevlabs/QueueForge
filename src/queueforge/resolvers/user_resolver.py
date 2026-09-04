from typing import Any

from fastapi import status
from graphql import GraphQLResolveInfo
from injector import inject
from pydantic import ValidationError

from queueforge.command.commands import RegisterUserRequest
from queueforge.exceptions import exceptions
from queueforge.helpers.helpers import create_response, validate_model
from queueforge.services.user_service import UserService


class UserResolver:
    """User Resolver."""

    @inject
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    async def resolve_register_user(self, _: Any, info: GraphQLResolveInfo, data: dict):
        """Resolver for registering a new user."""
        # Implement the logic to register a user using the UserService
        try:
            validated_data = validate_model(data, RegisterUserRequest)
            result = await self._user_service.register_user(validated_data)
            return create_response(
                data=result,
                status_code=status.HTTP_201_CREATED,
            )
        except (exceptions.InvalidRequestError, ValidationError) as e:
            return create_response(
                error=e,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except exceptions.AlreadyExistsError as e:
            return create_response(
                error=e,
                status_code=status.HTTP_409_CONFLICT,
            )
        except Exception as e:  # noqa: BLE001
            # Handle exceptions and return an appropriate error response
            return create_response(
                error=e,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
