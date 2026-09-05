"""Generic repository interface for the application."""

from abc import ABCMeta, abstractmethod
from typing import TypeVar

from loguru import logger

from queueforge.bootstrap.modules.repository.data_mapper import DataMapper
from queueforge.entity.entity import Entity as DomainEntity
from queueforge.entity.identifier import UUIDIdentifier

Entity = TypeVar("Entity", bound=DomainEntity)
EntityId = TypeVar("EntityId", bound=UUIDIdentifier)
Base = TypeVar("Base")


class GenericRepository[EntityId: UUIDIdentifier, Entity: DomainEntity](
    metaclass=ABCMeta
):
    """An interface for a generic repository."""

    mapper_class: type[DataMapper[Entity, Base]]  # type: ignore
    _model_class: type[Entity]

    def __init__(self, identity_map=None):
        self.logger = logger
        self._identity_map = identity_map or {}

    @abstractmethod
    async def add(self, entity: Entity):
        raise NotImplementedError()

    @abstractmethod
    async def update(self, entity: Entity):
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self) -> list[Entity]:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, entity_id: EntityId) -> Entity:
        raise NotImplementedError()

    async def __getitem__(self, key: EntityId) -> Entity:
        return await self.get_by_id(key)

    @property
    def model_class(self) -> type[Entity]:
        return self._model_class

    @property
    def data_mapper(self):
        return self.mapper_class()

    def map_entity_to_model(self, entity: Entity):
        assert self.mapper_class is not None, (
            f"No data_mapper attribute in {self.__class__.__name__}. "
            "Make sure to include `mapper_class = MyModel` in the Repository class."
        )

        return self.data_mapper.entity_to_model(entity)  # type: ignore

    def map_model_to_entity(self, instance) -> Entity:
        assert self.data_mapper
        return self.data_mapper.model_to_entity(instance)  # type: ignore

    def _get_entity(self, instance):
        if instance is None:
            return None
        entity = self.map_model_to_entity(instance)

        self._identity_map[entity.id] = entity  # type: ignore
        return entity

    def collect_events(self):
        """Collects all events from entities known to the repository (present in the identity map)."""
        events = []
        for entity in self._identity_map.values():
            events.extend(entity.collect_events())
        return events

    def get_model_class(self):
        assert self.model_class is not None, (
            f"No model_class attribute in in {self.__class__.__name__}. "
            "Make sure to include `model_class = MyModel` in the class."
        )
        return self.model_class

    def get_identifier(self) -> str:
        return self.__class__.__name__
