import inspect
from typing import TypeVar

from injector import Binder, Module, SingletonScope

from queueforge.bootstrap.modules.service.service import GenericService
from queueforge.configs.settings import AppSettings

T = TypeVar("T")


class ServiceModule(Module):
    def __init__(self, app_context, settings: AppSettings):
        super().__init__()
        self._app_context = app_context
        self._settings = settings

    def configure(self, binder: Binder) -> None:
        service_classes = self._get_subclasses(GenericService)
        for obj in service_classes:
            if (
                issubclass(obj, GenericService)
                and obj != GenericService
                and not inspect.isabstract(obj)
            ):
                obj.settings = self._settings
                obj.app_context = self._app_context
                binder.bind(GenericService, to=obj, scope=SingletonScope)

    def _get_subclasses(self, cls: type[T], _subclasses=None) -> list[type[T]]:
        if _subclasses is None:
            _subclasses = []
        _subclasses.append(cls)

        for subclass in cls.__subclasses__():
            self._get_subclasses(subclass, _subclasses)
        return _subclasses
