"""Sql Repository."""

from typing import TypeVar

from sqlalchemy.orm import Session

from queueforge.bootstrap.modules.repository.repository import GenericRepository
from queueforge.entity.entity import Entity as DomainEntity
from queueforge.entity.identifier import UUIDIdentifier
from queueforge.exceptions.exceptions import EntityNotFoundException

Entity = TypeVar("Entity", bound=DomainEntity)
EntityId = TypeVar("EntityId", bound=UUIDIdentifier)


class SqlRepository(GenericRepository[EntityId, Entity]):
    """Sql Repository."""

    def __init__(self, session: Session):
        super().__init__()
        self._session = session

    @property
    def session(self) -> Session:
        """Database settion."""
        return self._session

    async def add(self, entity: Entity):
        """Add new entity to model"""
        self._identity_map[entity.id] = entity
        instance = self.map_entity_to_model(entity)
        self.session.add(instance)

    async def update(self, entity: Entity):
        """update entity to model"""
        self._identity_map[entity.id] = entity
        instance = self.map_entity_to_model(entity)
        self.session.merge(instance)

    async def get_by_id(self, entity_id: EntityId) -> Entity:
        """Get entity via id"""
        instance = self.session.query(self.get_model_class()).get(entity_id)
        if instance is None:
            raise EntityNotFoundException(repository=self, entity_id=entity_id)
        return self._get_entity(instance)  # type: ignore

    def persist(self, entity: Entity):
        """Persists all the changes made to the entity.
        Basically, entity is mapped to a model instance using a data_mapper, and then added to sqlalchemy session.
        """
        assert entity.id in self._identity_map, (
            "Cannon persist entity which is unknown to the repo. Did you forget to call repo.add() for this entity?"
        )
        instance = self.map_entity_to_model(entity)
        merged = self.session.merge(instance)
        self.session.add(merged)

    def persist_all(self):
        """Persists all changes made to entities known to the repository (present in the identity map)."""
        for entity in self._identity_map.values():
            self.persist(entity)

    def count(self) -> int:
        """Count data from the table."""
        return self.session.query(self.model_class).count()

    async def get_all(self):
        pass

    async def delete(self, entity_id: EntityId):
        pass
