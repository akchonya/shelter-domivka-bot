from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from core_bot.utils.broadcaster import broadcast
from infrastructure.database.repo.requests import RequestsRepo

router = Router()


@router.message(Command("test"))
async def test_handler(message: Message, bot: Bot):
    print("done")
