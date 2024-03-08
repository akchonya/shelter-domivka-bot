import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from core.handlers.user import router as user_router
from core.utils.config import AppConfig, create_config


async def main() -> None:
    config: AppConfig = create_config()
    dp: Dispatcher = Dispatcher()
    dp.include_routers(user_router)
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(
        token=config.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
