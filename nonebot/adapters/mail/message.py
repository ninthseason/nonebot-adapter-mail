from typing import Type, Union, Iterable

from nonebot.typing import overrides

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment

from .api import Message as MailMessage


class MessageSegment(BaseMessageSegment):
    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @overrides(BaseMessageSegment)
    def __add__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return Message(self) + (
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @overrides(BaseMessageSegment)
    def __radd__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return (
            MessageSegment.text(other) if isinstance(other, str) else Message(other)
        ) + self

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        params = ", ".join(
            [f"{k}={str(v)}" for k, v in self.data.items() if v is not None]
        )
        return f"[{self.type}{':' if params else ''}{params}]"

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text"

    @staticmethod
    def text(text: str) -> "Text":
        return Text("text", {"text": text})


class Text(MessageSegment):
    @overrides(MessageSegment)
    def __str__(self) -> str:
        return self.data["text"]


class Html(MessageSegment):
    @overrides(MessageSegment)
    def __str__(self) -> str:
        return f"<html:{self.data['html']}>"


class Attachment(MessageSegment):
    @overrides(MessageSegment)
    def __str__(self) -> str:
        return f"<attachment:{self.data['url']}>"


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @overrides(BaseMessage)
    def __add__(
        self, other: Union[str, MessageSegment, Iterable[MessageSegment]]
    ) -> "Message":
        return super(Message, self).__add__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @overrides(BaseMessage)
    def __radd__(
        self, other: Union[str, MessageSegment, Iterable[MessageSegment]]
    ) -> "Message":
        return super(Message, self).__radd__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: str) -> Iterable[MessageSegment]:
        if msg:
            yield Text("text", {"text": msg})

    @classmethod
    def from_mail_message(cls, message: MailMessage) -> "Message":
        msg = Message()
        if message.content:
            msg.extend(Message(message.content))
        if message.html:
            msg.append(Html("html", data={"html": message.html}))
        if message.attachments:
            msg.extend(
                Attachment("attachment", data={"url": seg.url})
                for seg in message.attachments
                if seg.url
            )
        return msg
