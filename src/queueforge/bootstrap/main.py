from importlib import import_module
from pathlib import Path
from types import ModuleType

from ariadne import MutationType, QueryType, ScalarType, SubscriptionType
from ariadne.asgi.handlers import GraphQLHTTPHandler
from ariadne.contrib.federation import make_federated_schema
from ariadne.contrib.tracing.opentelemetry import OpenTelemetryExtension
from ariadne.load_schema import read_graphql_file
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from graphql import GraphQLSchema
from loguru import logger

from queueforge.constants.constants import API_BASE_VERSION
from queueforge.graphql import GraphQLx
from queueforge.graphql.helper import default_bad_request_handler
from queueforge.graphql.scalar import short_id_scalar


class QueueForgeStartup:
    def initialize(self) -> FastAPI:
        """Initialize the QueueForge application."""
        logger.info("Initializing QueueForge application...")
        app = FastAPI(title="QueueForge")

        # Initialize routes
        self._routes(app)

        return app

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

        app.mount(f"api/{API_BASE_VERSION}/graphql", graphql)

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

        locations.append(location_path)
        logger.debug(f"Available schema locations \n:: {str(locations)}")
        return locations

    async def health_check(self):
        return JSONResponse({"status": "ok", "status_code": 200})

    def _load_query_bindable(self) -> QueryType:
        query = QueryType()
        return query

    def _load_object_type_bindable(self):
        return

    def _load_subscription_bindable(self) -> SubscriptionType:
        subscription = SubscriptionType()
        return subscription

    def _load_mutation_bindable(self) -> MutationType:
        mutation = MutationType()
        return mutation

    def _load_scalar_type_bindable(self) -> list[ScalarType]:
        return [short_id_scalar]

    def _load_schema(self) -> str:
        schema_locations = self.__get_schema_locations()
        schema_list = []

        for folder in schema_locations:
            if folder.exists() and folder.is_dir():
                for file in folder.glob("*.graphql"):
                    schema_list.append(read_graphql_file(file))

        return "\n".join(schema_list)


def start_app(main: QueueForgeStartup) -> FastAPI:
    """Initializing the main application."""
    return main.initialize()
