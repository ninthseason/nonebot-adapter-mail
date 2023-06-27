import asyncio
from typing import Any, List, Optional

from nonebot.drivers import Driver
from nonebot.typing import overrides

from nonebot.adapters import Adapter as BaseAdapter

from .config import Config


class Adapter(BaseAdapter):
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any) -> None:
        super().__init__(driver, **kwargs)
        self.mail_config = Config.parse_obj(self.config)
        self._task: Optional[asyncio.Task] = None
        self.tasks: List["asyncio.Task"] = []
        self.setup()

    @staticmethod
    @overrides(BaseAdapter)
    def get_name() -> str:
        return "Mail"

    def setup(self):
        pass

    async def _start(self) -> None:
        pass

    async def _shutdown(self) -> None:
        pass
