import os
import sys
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Any, TypeVar

import injector
from ariadne import MutationType, QueryType, ScalarType, SubscriptionType
from ariadne.asgi.handlers import GraphQLHTTPHandler
from ariadne.contrib.federation import make_federated_schema
from ariadne.contrib.tracing.opentelemetry import OpenTelemetryExtension
from ariadne.load_schema import read_graphql_file
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from graphql import GraphQLSchema
from loguru import logger
from pydantic import ValidationError
from yaml import safe_load

from queueforge.bootstrap.modules.repository.connection.postgresModule import (
    PostgresModule,
)
from queueforge.bootstrap.modules.service.module import ServiceModule
from queueforge.configs.settings import AppSettings
from queueforge.constants.constants import API_BASE_VERSION, BASE_PATH, ENV_PREFIX
from queueforge.db_connection.sql_connection import SqlConnection
from queueforge.exceptions.exceptions import InvalidSettingException
from queueforge.graphql import GraphQLx
from queueforge.graphql.helper import default_bad_request_handler
from queueforge.graphql.scalar import short_id_scalar
from queueforge.resolvers.user_resolver import UserResolver

T = TypeVar("T")


class QueueForgeStartup:
    def __init__(self, testing: bool = False):
        self._injector = injector.Injector()
        self._property_file_name = "production"
        if testing is True:
            self._property_file_name = "testing"

        self.settings: AppSettings = self.__get_application_settings()
        self._load_app_context()

    def initialize(self) -> FastAPI:
        """Initialize the QueueForge application."""
        logger.info("Initializing QueueForge application...")
        app = FastAPI(title="QueueForge", on_startup=[self._startup_health_check])

        # Initialize routes
        self._routes(app)

        return app

    @property
    def app_context(self) -> injector.Injector:
        """Provide the application context."""
        return self._injector

    def _load_app_context(self):
        # path = self._get_app_path().stem
        self._configure_container(self.app_context.binder)

    def _configure_container(self, binder: injector.Binder) -> None:
        binder.install(PostgresModule(self.settings))
        binder.install(ServiceModule(self.app_context, self.settings))

    async def _startup_health_check(self):
        """Check database connectivity at startup."""
        try:
            db_healthy = self._check_database_connection()
            if not db_healthy:
                logger.error("Database connection failed at startup")
                raise RuntimeError("Database connection unavailable")
            logger.info("Database connection verified at startup")

        except Exception as e:
            logger.error(f"Startup health check failed: {e!s}")
            raise

    def __get_env_prefix(self) -> str:
        return ENV_PREFIX

    def _get_app_path(self) -> Path:
        return Path(__file__).parent.parent

    def __get_application_settings(self) -> AppSettings:
        settings_class = self._get_setting_class()

        if not isinstance(settings_class, type(AppSettings)):
            raise InvalidSettingException()

        return self.__setting_factory(
            settings_class,
            env_prefix=self.__get_env_prefix(),
            app_path=self._get_app_path(),
        )

    def __load_config(self, app_env: str, config_dir: Path) -> dict[Any, Any]:
        config_file = config_dir.joinpath(f"{app_env}.yaml")

        if not config_file.exists():
            raise ValueError(f"Config file {config_file} not found.")

        logger.info(f"Loading configuration ... {config_file}")
        return safe_load(open(config_file).read())

    def __setting_factory(
        self,
        setting_class: type[AppSettings],
        env_prefix: str = ENV_PREFIX,
        app_path: Path = BASE_PATH,
    ):
        app_env = os.getenv(env_prefix + "APP_ENV", self._property_file_name)
        config_dir = os.getenv("CONFIG_DIR")

        if config_dir is not None:
            logger.info(f"ENV config_dir set: {config_dir}")
            config_dir = Path(f"{config_dir}/{app_path.name}")
        else:
            config_dir = app_path

        try:
            settings = setting_class(
                _env_file=f"{app_env}.env",  # type: ignore
                base_path=app_path,
                app_env=app_env,
                **self.__load_config(app_env, config_dir),
            )
        except ValidationError as e:
            logger.error(f"Invalid Config/Settings. Error::  {e!s}")
            sys.exit(-1)
        else:
            return settings

    def _get_setting_class(self) -> type[AppSettings]:
        return AppSettings

    def init_graphql(self) -> GraphQLx:
        return GraphQLx(
            self.get_schema(),
            error_formatter=default_bad_request_handler,
            debug=True,
            introspection=True,
            http_handler=GraphQLHTTPHandler(
                extensions=[OpenTelemetryExtension],
            ),
        )

    def _routes(self, app: FastAPI):
        graphql = self.init_graphql()

        app.add_api_route("/health", self.health_check, methods=["GET"])

        app.mount(f"/api/{API_BASE_VERSION}/graphql", graphql)

    def _get_schema_location(self) -> ModuleType:
        return import_module("queueforge.graphql")

    def get_schema(self) -> GraphQLSchema:
        bindable = []

        if self._load_query_bindable():
            bindable.append(self._load_query_bindable())

        if self._load_mutation_bindable():
            bindable.append(self._load_mutation_bindable())

        if self._load_object_type_bindable():
            bindable.append(self._load_object_type_bindable())

        if self._load_subscription_bindable():
            bindable.append(self._load_subscription_bindable())

        bindable.extend(self._load_scalar_type_bindable())

        return make_federated_schema(
            self._load_schema(),
            bindable,
            convert_names_case=True,
        )

    def __get_schema_locations(self) -> list[Path]:
        locations = []
        schema_location = self._get_schema_location()
        location_path = Path(schema_location.__file__).parent.joinpath("schemas")  # type: ignore

        for file in GRAPHQL_INTEGRATION_FILES:
            locations.append(location_path.joinpath(file))

        logger.debug(f"Available schema locations \n:: {locations!s}")
        return locations

    def _load_schema(self) -> str:
        schema_locations = self.__get_schema_locations()
        schema_list = []

        for path in schema_locations:
            if path.exists():
                schema_list.append(read_graphql_file(path))

        return "\n".join(schema_list)

    async def health_check(self):
        if self._check_database_connection():
            return JSONResponse({"status": "ok", "status_code": 200})
        return JSONResponse({"status": "error", "status_code": 503})

    def _check_database_connection(self) -> bool:
        try:
            db_conn = self.app_context.get(SqlConnection)
            return db_conn.test_connection()
        except Exception as e:  # noqa: BLE001
            logger.error(f"SQL database connection check failed: {e!s}")
            return False

    def _load_query_bindable(self) -> QueryType:
        query = QueryType()

        query.set_field(
            "users",
            lambda *_: [
                {"id": "1", "name": "John Doe", "email": "john.doe@example.com"}
            ],
        )
        return query

    def _load_object_type_bindable(self):
        return

    def _load_subscription_bindable(self) -> SubscriptionType:
        subscription = SubscriptionType()  # noqa: F841
        return  # type: ignore

    def _get_resolver(self, resolver_type: type[T]) -> T:
        """Retrieve the specified resolver instance from the application context."""
        return self.app_context.get(resolver_type)

    def _load_mutation_bindable(self) -> MutationType:
        mutation = MutationType()
        mutation.set_field(
            "registerUser", self._get_resolver(UserResolver).resolve_register_user
        )
        return mutation

    def _load_scalar_type_bindable(self) -> list[ScalarType]:
        return [short_id_scalar]


GRAPHQL_INTEGRATION_FILES = [
    "schema.graphql",
    "mutations.graphql",
    "queries.graphql",
    # "subscription.graphql",
]


def start_app(main: QueueForgeStartup) -> FastAPI:
    """Initializing the main application."""
    return main.initialize()
