from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ℹ️ Інформація"), KeyboardButton(text="📍 Локація")],
        [KeyboardButton(text="📞 Контакти"), KeyboardButton(text="🆘 Допомога")],
    ],
    resize_keyboard=True,
)
