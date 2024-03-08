from aiogram import Router, F, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from core.keyboards.user_kbs import menu_kb


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"{html.bold('👋 Вітаю! Я - бот-помічник Домівки врятованих тварин')}\n\nСкористайтеся кнопками в меню:",
        reply_markup=menu_kb,
    )


@router.message(F.text == "ℹ️ Інформація")
async def info_handler(message: Message):
    await message.answer("тут має бути інформація")


@router.message(F.text == "📍 Локація")
async def location_handler(message: Message):
    await message.answer("тут має бути локація")


@router.message(F.text == "📞 Контакти")
async def contacts_handler(message: Message):
    await message.answer("тут мають бути контакти")


@router.message(F.text == "🆘 Допомога")
async def help_handler(message: Message):
    await message.answer("тут має бути допомога")
