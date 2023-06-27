from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Mail(BaseModel):
    id: Optional[str] = None


class User(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None


class MessageAttachment(BaseModel):
    url: Optional[str] = None


class MessageHtml(BaseModel):
    content: Optional[str] = None


class Message(BaseModel):
    id: Optional[int] = None
    timestamp: Optional[datetime] = None
    author: Optional[User] = None
    content: Optional[str] = None
    html: Optional[MessageHtml] = None
    attachments: Optional[List[MessageAttachment]] = None
    seq: Optional[int] = None
