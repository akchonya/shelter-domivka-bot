from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from core_bot.utils.broadcaster import broadcast
from core_bot.filters.admin import AdminFilter
from infrastructure.database.repo.requests import RequestsRepo

router = Router()
router.message.filter(AdminFilter())


@router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Вітаю, адміне!")


@router.message(Command("broadcast"))
async def broadcast_handler(message: Message, repo: RequestsRepo):
    async for batch in repo.users.get_all_users():
        user_ids = [user.user_id for user in batch]
        await broadcast(bot=message.bot, users=user_ids, text="test1")
