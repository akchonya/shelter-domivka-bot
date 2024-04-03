from aiogram.filters import BaseFilter
from aiogram.types import Message

from core_bot.utils.config import AppConfig


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message, config: AppConfig) -> bool:
        return (obj.from_user.id in config.core.admin_chat_ids) == self.is_admin
