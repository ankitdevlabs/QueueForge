"""DataMapper from one entity to another."""

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from queueforge.entity.entity import Entity

MapperEntity = TypeVar("MapperEntity", bound=Entity)
MapperModel = TypeVar("MapperModel", bound=Any)


class DataMapper[MapperEntity, MapperModel](ABC):
    """Base class to map model to entity and vice versa."""

    entity_class: type[MapperEntity]
    model_class: type[MapperModel]

    @abstractmethod
    def entity_to_model(entity: MapperEntity) -> MapperModel:
        raise NotImplementedError()

    @abstractmethod
    def model_to_entity(model: MapperModel) -> MapperEntity:
        raise NotImplementedError()
