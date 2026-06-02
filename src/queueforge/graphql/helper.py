import loguru
from ariadne import format_error
from fastapi import status

from graphql import GraphQLError

logger = loguru.logger


def default_bad_request_handler(error: GraphQLError, debug: bool = False) -> dict:
    if debug:
        return format_error(error, debug)
    logger.warning(f"Sending {status.HTTP_400_BAD_REQUEST} due to bad graphql schema")
    return {"message": "Bad Request", "error_status": status.HTTP_400_BAD_REQUEST}
