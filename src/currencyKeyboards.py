from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

currencyMenu=ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="🇺🇿UZS"),
        KeyboardButton(text="🇺🇸USD")
    ],
    [
        KeyboardButton(text="🇪🇺EUR"),
        KeyboardButton(text="🇷🇺RUB")
    ],
    [
        KeyboardButton(text="🇰🇿KZT"),
        KeyboardButton(text="🇰🇬KGS")
    ]
], resize_keyboard=True)