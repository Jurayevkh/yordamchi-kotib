from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

currencyMenu=ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="🇺🇿UZS"),
        KeyboardButton(text="🇺🇸USD")
    ],
    [
        KeyboardButton(text="🇪🇺EUR"),
        KeyboardButton(text="🇷🇺RUB")
    ]
], resize_keyboard=True)