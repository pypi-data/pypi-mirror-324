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
class B2S_ConfirmNotify:
    """
    B2S = Broadcaster to Subscriber
    See the type enum documentation for more information on the fields
    """

    type: Literal[BroadcasterToSubscriberStatefulMessageType.CONFIRM_NOTIFY]
    """discriminator value"""

    identifier: bytes
    """an arbitrary identifier for the notification assigned by the subscriber; max 64 bytes
    """

    subscribers: int
    """how many subscribers were successfully notified"""

    authorization: Optional[str]
    """the authorization header that shows the confirmation was sent by the broadcaster
    that was contacted
    
    empty strings are converted to None for consistency with http endpoints
    """

    tracing: bytes
    """the tracing data, which may be empty"""


_headers: Collection[str] = (
    "x-identifier",
    "x-subscribers",
    "authorization",
    "x-tracing",
)


class B2S_ConfirmNotifyParser:
    """Satisfies B2S_MessageParser[B2S_ConfirmNotify]"""

    @classmethod
    def relevant_types(cls) -> List[BroadcasterToSubscriberStatefulMessageType]:
        return [BroadcasterToSubscriberStatefulMessageType.CONFIRM_NOTIFY]

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: BroadcasterToSubscriberStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> B2S_ConfirmNotify:
        assert type == BroadcasterToSubscriberStatefulMessageType.CONFIRM_NOTIFY

        headers = parse_simple_headers(flags, payload, _headers)
        identifier = headers["x-identifier"]
        if len(identifier) > 64:
            raise ValueError("x-identifier must be at most 64 bytes")

        subscriber_bytes = headers["x-subscribers"]
        if len(subscriber_bytes) > 8:
            raise ValueError("x-subscribers must be at most 8 bytes")

        subscribers = int.from_bytes(subscriber_bytes, "big")

        authorization_bytes = headers["authorization"]
        authorization: Optional[str] = None
        if authorization_bytes != b"":
            try:
                authorization = authorization_bytes.decode("utf-8")
            except UnicodeDecodeError:
                raise ValueError("authorization must be a utf-8 string")

        tracing = headers["x-tracing"]

        return B2S_ConfirmNotify(
            type=type,
            identifier=identifier,
            subscribers=subscribers,
            authorization=authorization,
            tracing=tracing,
        )


if TYPE_CHECKING:
    _: Type[B2S_MessageParser[B2S_ConfirmNotify]] = B2S_ConfirmNotifyParser


def serialize_b2s_confirm_notify(
    msg: B2S_ConfirmNotify, /, *, minimal_headers: bool
) -> Union[bytes, bytearray]:
    """Satisfies MessageSerializer[B2S_ConfirmNotify]"""
    return serialize_simple_message(
        type=msg.type,
        header_names=_headers,
        header_values=(
            msg.identifier,
            int_to_minimal_unsigned(msg.subscribers),
            msg.authorization.encode("utf-8") if msg.authorization is not None else b"",
            msg.tracing,
        ),
        payload=b"",
        minimal_headers=minimal_headers,
    )


if TYPE_CHECKING:
    __: MessageSerializer[B2S_ConfirmNotify] = serialize_b2s_confirm_notify
