from ariadne import MutationType, QueryType, ScalarType, SubscriptionType
from ariadne.contrib.federation import make_federated_schema
from fastapi import FastAPI
from graphql import GraphQLSchema
from loguru import logger

from queueforge.graphql.scalar import short_id_scalar


class QueueForgeStartup:
    def initialize(self) -> FastAPI:
        """Initialize the QueueForge application."""
        logger.info("Initializing QueueForge application...")
        app = FastAPI(title="QueueForge")
        # Additional setup can be done here (e.g., include routers, middleware, etc.)
        return app

    def _routes(self) -> None:
        """Load application routes."""
        pass

    def init_graphql(self):
        pass

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
        return ""


def start_app(main: QueueForgeStartup) -> FastAPI:
    """Initializing the main application."""
    return main.initialize()
