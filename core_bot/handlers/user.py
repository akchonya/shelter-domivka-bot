from aiogram import F, Router, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types.callback_query import CallbackQuery

from core_bot.keyboards import (
    Location,
    MenuLocation,
    get_contacts_ikb,
    get_location_ikb,
    Information,
    MenuInformation,
    MenuHelp,
    Help,
)
from core_bot.keyboards.user_kbs import (
    get_main_menu_kb,
    DynamicKbBuilder,
    get_info_ikb,
    get_help_ikb,
)
from core_bot.utils.text import (
    MenuButtons,
    contact_text,
    info_text,
    location_main_pic,
    location_main_text,
    location_second_text,
    adoption_text,
    found_text,
    help_text,
    help_finance,
    help_material,
    help_physical,
)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    kb = await get_main_menu_kb()

    await message.answer(
        f"{html.bold('👋 Вітаю! Я - бот-помічник Домівки врятованих тварин')}\n\nСкористайтеся кнопками в меню:",
        reply_markup=kb,
    )


# Information Handlers
@router.message(F.text == MenuButtons.information.value)
async def info_handler(message: Message):
    ikb = await get_info_ikb()
    await message.answer(info_text, reply_markup=ikb)


@router.callback_query(MenuInformation.filter(F.information == Information.adoption))
async def adoption_handler(query: CallbackQuery, callback_data: MenuLocation):
    kb = await get_main_menu_kb()
    await query.message.answer(adoption_text, reply_markup=kb)


@router.callback_query(MenuInformation.filter(F.information == Information.found))
async def found_handler(query: CallbackQuery, callback_data: MenuLocation):
    kb = await get_main_menu_kb()
    await query.message.answer(found_text, reply_markup=kb)


# Location handlers
@router.message(F.text == MenuButtons.locations.value)
async def location_handler(message: Message):
    ikb = await get_location_ikb()

    await message.answer(f"{html.bold('Наші локації:')}", reply_markup=ikb)


@router.callback_query(MenuLocation.filter(F.location == Location.main))
async def location_main_handler(query: CallbackQuery, callback_data: MenuLocation):
    kb = await get_main_menu_kb()
    await query.message.answer_photo(
        photo=location_main_pic, caption=location_main_text, reply_markup=kb
    )


@router.callback_query(MenuLocation.filter(F.location == Location.second))
async def location_second_handler(query: CallbackQuery, callback_data: MenuLocation):
    kb = await get_main_menu_kb()
    await query.message.answer(location_second_text, reply_markup=kb)


@router.message(F.text == MenuButtons.contacts.value)
async def contacts_handler(message: Message):
    ikb = await get_contacts_ikb()
    await message.answer(text=contact_text, reply_markup=ikb)


# Help handlers
@router.message(F.text == MenuButtons.help_.value)
async def help_handler(message: Message):
    ikb = await get_help_ikb()
    await message.answer(text=help_text, reply_markup=ikb)


@router.callback_query(MenuHelp.filter(F.help == Help.finance))
async def finance_handler(query: CallbackQuery, callback_data: MenuHelp):
    kb = await get_main_menu_kb()
    await query.message.answer(help_finance, reply_markup=kb)


@router.callback_query(MenuHelp.filter(F.help == Help.material))
async def material_handler(query: CallbackQuery, callback_data: MenuHelp):
    kb = await get_main_menu_kb()
    await query.message.answer(help_material, reply_markup=kb)


@router.callback_query(MenuHelp.filter(F.help == Help.physical))
async def physical_handler(query: CallbackQuery, callback_data: MenuHelp):
    kb = await get_main_menu_kb()
    await query.message.answer(help_physical, reply_markup=kb)


@router.callback_query(F.data == "menu_main")
async def main_menu_handler(query: CallbackQuery):
    kb = await get_main_menu_kb()
    await query.message.answer(text="📝 Головне меню:", reply_markup=kb)
