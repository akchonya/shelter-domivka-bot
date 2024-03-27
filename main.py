import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers.user import router as user_router
from bot.utils.config import AppConfig, create_config
from bot.middlewares.config import ConfigMiddleware
from aiogram.utils.callback_answer import CallbackAnswerMiddleware


def register_global_middlewares(dp: Dispatcher, config: AppConfig, session_pool=None):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param config: The configuration object from the loaded configuration.
    :param session_pool: Optional session pool object for the database using SQLAlchemy.
    :return: None
    """
    middleware_types = [
        ConfigMiddleware(config),
        # DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


async def main() -> None:
    config: AppConfig = create_config()
    dp: Dispatcher = Dispatcher()
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.include_routers(user_router)
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(
        token=config.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    register_global_middlewares(dp, config)

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
