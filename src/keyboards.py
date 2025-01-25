from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu=ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Uchrashuv belgilash⏰"),
        KeyboardButton(text="Vakansiya ochish💼")
    ],
    [
        KeyboardButton(text="Valyuta💱"),
        KeyboardButton(text="Ma'lumotlarni inlinega saqlash📍")
    ]
], resize_keyboard=True)