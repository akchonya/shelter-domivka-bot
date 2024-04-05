from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from core_bot.utils.text import MenuButtons

####################
# Common Keyboards #
####################


async def get_main_menu_kb():
    builder = ReplyKeyboardBuilder()
    for button in MenuButtons:
        builder.row(KeyboardButton(text=button))

    builder.adjust(2)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def get_main_menu_button():
    """
    Returns InlineKeyboardBuilder with a Main Menu button
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Головне меню",
        callback_data="menu_main",
    )

    return builder


###############
# Information #
###############


class Information(str, Enum):
    adoption = "✨ Адопція тварин"
    found = "❔ Знайшов тварину"


class MenuInformation(CallbackData, prefix="information"):
    information: Information


async def get_info_ikb():
    builder = InlineKeyboardBuilder()
    for information in Information:
        builder.button(
            text=information.value,
            callback_data=MenuInformation(
                information=information,
            ),
        )
    main_menu_button = await get_main_menu_button()
    builder.attach(main_menu_button)

    return builder.as_markup()


#################
# Location Menu #
#################
class Location(str, Enum):
    main = "м. Львів"
    second = "с. Тичок"


class MenuLocation(CallbackData, prefix="location"):
    location: Location


async def get_location_ikb():
    builder = InlineKeyboardBuilder()
    for location in Location:
        builder.button(
            text=location.value,
            callback_data=MenuLocation(
                location=location,
            ),
        )
    main_menu_button = await get_main_menu_button()
    builder.attach(main_menu_button)

    return builder.as_markup()


#################
# Contacts Menu #
#################

social_networks = {
    "Instagram": "https://www.instagram.com/shelter_domivka?igsh=MXVlbWxkYWo5MjNnMw==",
    "Facebook": "https://www.facebook.com/share/XyBKXWhMnEcLYp5c/?mibextid=K35XfP",
    "Twitter": "https://twitter.com/shelter_domivka",
    "TikTok": "https://www.tiktok.com/@dopomogadomivka?_t=8kVJIb7bPKY&_r=1",
}


async def get_contacts_ikb():
    builder = InlineKeyboardBuilder()

    # Add social network links
    for text, url in social_networks.items():
        builder.row(
            InlineKeyboardButton(text=text, url=url),
            width=1,
        )

    # Add "Connect via bot" button
    # builder.row(
    #     InlineKeyboardButton(
    #         text="[TODO]",
    #         callback_data="none",
    #     )
    # )

    main_menu = await get_main_menu_button()

    # Attach "Back to the main menu" button
    builder.attach(main_menu)

    return builder.as_markup()


class DynamicKbBuilder:
    async def get_dynamic_ikb(self, menu_type):
        if menu_type == "location":
            ikb = await self._get_dynamic_ikb(Location, MenuLocation)
            return ikb
        elif menu_type == "information":
            ikb = await self._get_dynamic_ikb(Information, MenuInformation)
            return ikb
        else:
            raise ValueError("Invalid menu type. Must be 'location' or 'information'.")

    async def _get_dynamic_ikb(self, enum_class, callback_data_class):
        builder = InlineKeyboardBuilder()
        for enum_item in enum_class:
            builder.button(
                text=enum_item.value,
                callback_data=callback_data_class(
                    **{enum_class.__name__.lower(): enum_item}
                ),
            )
        main_menu_button = await get_main_menu_button()
        builder.attach(main_menu_button)
        return builder.as_markup()


###########
# Help Kb #
###########
class Help(str, Enum):
    finance = "Фінансова"
    material = "Матеріальна "
    physical = "Фізична"


class MenuHelp(CallbackData, prefix="help"):
    help: Help


async def get_help_ikb():
    builder = InlineKeyboardBuilder()
    for help in Help:
        builder.button(
            text=help.value,
            callback_data=MenuHelp(
                help=help,
            ),
        )
    main_menu_button = await get_main_menu_button()
    builder.attach(main_menu_button)

    return builder.as_markup()
