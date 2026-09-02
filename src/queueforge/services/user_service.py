"""User Service."""

from injector import inject

from queueforge.bootstrap.modules.service.service import GenericService
from queueforge.repositories.user_repository import UserRepository


class UserService(GenericService):
    """User Service class that provides business logic for user-related operations."""

    @inject
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
