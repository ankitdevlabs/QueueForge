from typing import Any

from graphql import GraphQLResolveInfo
from injector import inject

from queueforge.services.user_service import UserService


class UserResolver:
    """User Resolver."""

    @inject
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    async def resolve_register_user(self, _: Any, info: GraphQLResolveInfo, data: dict):
        """Resolver for registering a new user."""
        # Implement the logic to register a user using the UserService

        validate_data = data.get("email")

        if validate_data is None or not isinstance(validate_data, str):
            raise ValueError("Invalid email provided")
