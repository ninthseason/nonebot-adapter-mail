from typing import List

from pydantic import Field, HttpUrl, BaseModel


class HostInfo(BaseModel):
    host: str = Field(alias="host")
    port: int = Field(alias="port")
    tls: bool = Field(alias="tls")


class BotInfo(BaseModel):
    user: str = Field(alias="id")
    password: str = Field(alias="token")
    smtp: HostInfo = Field(alias="smtp")
    imap: HostInfo = Field(alias="imap")


class Config(BaseModel):
    mail_bots: List[BotInfo] = Field(default_factory=list)

    class Config:
        extra = "ignore"
