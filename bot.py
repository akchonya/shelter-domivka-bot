import asyncio
import logging
import sys

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from core_bot.handlers import routers_list
from core_bot.middlewares import DatabaseMiddleware
from core_bot.utils.broadcaster import broadcast
from core_bot.utils.config import AppConfig, create_config
from infrastructure.database.setup import create_engine, create_session_pool


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcast(bot, admin_ids, "Бот був запущений")


def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


async def main() -> None:
    setup_logging()

    config: AppConfig = create_config()
    bot: Bot = Bot(
        token=config.core.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp: Dispatcher = Dispatcher(config=config)

    engine = create_engine(config.db, echo=True)
    session_pool = create_session_pool(engine)

    dp.include_routers(*routers_list)

    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.message.outer_middleware(DatabaseMiddleware(session_pool=session_pool))
    dp.callback_query.outer_middleware(DatabaseMiddleware(session_pool=session_pool))

    await on_startup(bot, config.core.admin_chat_ids)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
