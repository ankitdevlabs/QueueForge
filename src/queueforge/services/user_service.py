"""User Service."""

from injector import inject

from queueforge.bootstrap.modules.service.service import GenericService
from queueforge.command.commands import RegisterUserRequest
from queueforge.dtos.user_dto import UserDTO
from queueforge.exceptions.exceptions import AlreadyExistsError
from queueforge.repositories.user_repository import UserRepository


class UserService(GenericService):
    """User Service class that provides business logic for user-related operations."""

    @inject
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def register_user(self, data: RegisterUserRequest) -> UserDTO | None:
        """Register a new user."""
        # Implement the logic to register a user using the UserRepository
        user = await self._user_repository.get_user_by_email(data.email)
        if user:
            raise AlreadyExistsError(f"User with email {data.email} already exists.")

        user = await self._user_repository.create_user(data)
        # return UserDTO.create(
        #     id=user.id,
        #     name=user.name,
        #     email=user.email,
        #     created_at=user.created_at,
        #     updated_at=user.updated_at,
        # )
