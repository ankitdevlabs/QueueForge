from uuid import UUID

from ariadne import ScalarType
from shortuuid import decode, encode

short_id_scalar = ScalarType("ShortId")


@short_id_scalar.serializer
def serialize_uid(value: UUID | str) -> str:
    try:
        if isinstance(value, str):
            return encode(UUID(value))
        return encode(value)
    except ValueError:
        return str(value)


@short_id_scalar.value_parser
def parse_uuid_value(value: str) -> UUID:
    return decode(value)
