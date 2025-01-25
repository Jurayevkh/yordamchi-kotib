from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

locationOrCard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Manzil saqlash📍"), KeyboardButton(text="Karta ma'lumotini saqlash💳")]
], resize_keyboard=True)