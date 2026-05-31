from ariadne import format_error
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLHTTPHandler, GraphQLWebsocketHandlerBase
from ariadne.types import (
    ContextValue,
    ErrorFormatter,
    RootValue,
    ValidationRules,
)

from graphql import GraphQLSchema


class GraphQLx(GraphQL):
    def __init__(
        self,
        schema: GraphQLSchema,
        *,
        context_value: ContextValue | None = None,
        root_value: RootValue | None = None,
        validation_rules: ValidationRules | None = None,
        introspection: bool = True,
        logger: str | None = None,
        error_formatter: ErrorFormatter = format_error,
        http_handler: GraphQLHTTPHandler | None = None,
        websocket_handler: GraphQLWebsocketHandlerBase | None = None,
    ):
        super().__init__(
            schema,
            context_value=context_value,
            root_value=root_value,
            validation_rules=validation_rules,
            introspection=introspection,
            logger=logger,
            error_formatter=error_formatter,
            http_handler=http_handler,
            websocket_handler=websocket_handler,
        )
