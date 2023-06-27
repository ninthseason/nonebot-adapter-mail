from typing import TYPE_CHECKING, Any

from nonebot.typing import overrides
from nonebot.message import handle_event

from nonebot.adapters import Bot as BaseBot

from .event import Event
from .config import BotInfo

if TYPE_CHECKING:
    from .adapter import Adapter


class Bot(BaseBot):
    @overrides(BaseBot)
    def __init__(self, adapter: "Adapter", self_id: str, bot_info: BotInfo):
        super().__init__(adapter, self_id)
        self.bot_info: BotInfo = bot_info

    @property
    def type(self) -> str:
        return "Mail"

    @overrides(BaseBot)
    async def send(self) -> Any:
        pass

    async def handle_event(self, event: Event) -> None:
        await handle_event(self, event)
