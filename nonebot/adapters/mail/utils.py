import base64
import email.message
import email.encoders
import email.mime.base
import email.mime.text

from nonebot.utils import escape_tag

from .message import Message


def escape_bytelines(s: list[bytearray]) -> str:
    return f'[{escape_tag(", ".join([i.decode() for i in s]))}]'


def extract_mail_parts(message: Message) -> list[email.message.EmailMessage]:
    parts = []
    for segment in message:
        if segment.type == "text":
            parts.append(email.mime.text.MIMEText(segment.data["text"]))
        elif segment.type == "html":
            parts.append(email.mime.text.MIMEText(segment.data["html"], "html"))
        elif segment.type == "attachment":
            part = email.mime.base.MIMEBase(
                segment.data["content_type"].split("/")[0],
                segment.data["content_type"].split("/")[1],
            )
            part.set_payload(
                base64.b64decode(segment.data["content"])
                if segment.data["binary"]
                else segment.data["content"]
            )
            email.encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{segment.data["name"]}"',
            )
            parts.append(part)
    return parts
