from typing import TYPE_CHECKING, Collection, List, Literal, Optional, Type, Union

from lonelypsp.compat import fast_dataclass
from lonelypsp.stateful.constants import (
    BroadcasterToSubscriberStatefulMessageType,
    PubSubStatefulMessageFlags,
)
from lonelypsp.stateful.generic_parser import B2S_MessageParser
from lonelypsp.stateful.parser_helpers import parse_simple_headers
from lonelypsp.stateful.serializer_helpers import (
    MessageSerializer,
    int_to_minimal_unsigned,
    serialize_simple_message,
)
from lonelypsp.sync_io import SyncReadableBytesIO


@fast_dataclass
class B2S_ContinueNotify:
    """
    B2S = Broadcaster to Subscriber
    See the type enum documentation for more information on the fields
    """

    type: Literal[BroadcasterToSubscriberStatefulMessageType.CONTINUE_NOTIFY]
    """discriminator value"""

    identifier: bytes
    """an arbitrary identifier for the notification assigned by the subscriber; max 64 bytes
    """

    part_id: int
    """the part id the broadcaster received; they are expecting the next part after this"""

    authorization: Optional[str]
    """the authorization header that shows the confirmation was sent by the broadcaster
    that was contacted

    empty strings are converted to None for consistency with http endpoints
    """

    tracing: bytes
    """the tracing data, which may be empty"""


_headers: Collection[str] = ("x-identifier", "x-part-id", "authorization", "x-tracing")


class B2S_ContinueNotifyParser:
    """Satisfies B2S_MessageParser[B2S_ContinueNotify]"""

    @classmethod
    def relevant_types(cls) -> List[BroadcasterToSubscriberStatefulMessageType]:
        return [BroadcasterToSubscriberStatefulMessageType.CONTINUE_NOTIFY]

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: BroadcasterToSubscriberStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> B2S_ContinueNotify:
        assert type == BroadcasterToSubscriberStatefulMessageType.CONTINUE_NOTIFY

        headers = parse_simple_headers(flags, payload, _headers)
        identifier = headers["x-identifier"]
        if len(identifier) > 64:
            raise ValueError("x-identifier must be at most 64 bytes")

        part_id_bytes = headers["x-part-id"]
        if len(part_id_bytes) > 8:
            raise ValueError("x-part-id must be at most 8 bytes")

        part_id = int.from_bytes(part_id_bytes, "big")

        authorization_bytes = headers["authorization"]
        authorization: Optional[str] = None
        if authorization_bytes != b"":
            try:
                authorization = authorization_bytes.decode("utf-8")
            except UnicodeDecodeError:
                raise ValueError("authorization must be a utf-8 string")

        tracing = headers["x-tracing"]

        return B2S_ContinueNotify(
            type=type,
            identifier=identifier,
            part_id=part_id,
            authorization=authorization,
            tracing=tracing,
        )


if TYPE_CHECKING:
    _: Type[B2S_MessageParser[B2S_ContinueNotify]] = B2S_ContinueNotifyParser


def serialize_b2s_continue_notify(
    msg: B2S_ContinueNotify, /, *, minimal_headers: bool
) -> Union[bytes, bytearray]:
    """Satisfies MessageSerializer[B2S_ContinueNotify]"""
    return serialize_simple_message(
        type=msg.type,
        header_names=_headers,
        header_values=(
            msg.identifier,
            int_to_minimal_unsigned(msg.part_id),
            msg.authorization.encode("utf-8") if msg.authorization is not None else b"",
            msg.tracing,
        ),
        payload=b"",
        minimal_headers=minimal_headers,
    )


if TYPE_CHECKING:
    __: MessageSerializer[B2S_ContinueNotify] = serialize_b2s_continue_notify
