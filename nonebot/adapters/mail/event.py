from enum import Enum
from typing import Dict, Type, Tuple

from nonebot.typing import overrides
from nonebot.utils import escape_tag

from nonebot.adapters import Event as BaseEvent

from .api import Mail, User
from .message import Message
from .api import Message as MailMessage


class EventType(str, Enum):
    # Init Event
    READY = "READY"
    RESUMED = "RESUMED"

    # MAIL_MESSAGES
    MESSAGE_CREATE = "MESSAGE_CREATE"


class Event(BaseEvent):
    __type__: EventType

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return self.__type__

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return escape_tag(str(self.dict()))

    @overrides(BaseEvent)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no context!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no context!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False


# Meta Event
class MetaEvent(Event):
    @overrides(BaseEvent)
    def get_type(self) -> str:
        return "meta_event"


class ReadyEvent(MetaEvent):
    __type__ = EventType.READY
    version: int
    session_id: str
    user: User
    shard: Tuple[int, int]


class ResumedEvent(MetaEvent):
    __type__ = EventType.RESUMED


# Mail Event
class MailEvent(Event, Mail):
    op_user_id: str

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return "notice"


# Message Event
class MessageEvent(Event, MailMessage):
    to_me: bool = False

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return "message"

    @overrides(Event)
    def get_user_id(self) -> str:
        return str(self.author.id)  # type: ignore

    @overrides(Event)
    def get_session_id(self) -> str:
        return str(self.author.id)  # type: ignore

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return escape_tag(
            f"Message {self.id} from {getattr(self.author, 'username', None)}<{getattr(self.author, 'id', None)}>: {self.get_message()}"
        )

    @overrides(Event)
    def get_message(self) -> Message:
        if not hasattr(self, "_message"):
            setattr(self, "_message", Message.from_mail_message(self))
        return getattr(self, "_message")

    @overrides(Event)
    def is_tome(self) -> bool:
        return self.to_me


class MessageCreateEvent(MessageEvent):
    __type__ = EventType.MESSAGE_CREATE


event_classes: Dict[str, Type[Event]] = {
    EventType.READY.value: ReadyEvent,
    EventType.RESUMED.value: ResumedEvent,
    EventType.MESSAGE_CREATE.value: MessageCreateEvent,
}

__all__ = [
    "EventType",
    "Event",
    "MailEvent",
    "MessageEvent",
    "MessageCreateEvent",
]
