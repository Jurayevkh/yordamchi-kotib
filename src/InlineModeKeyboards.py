from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

locationOrCard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Manzil saqlash📍"), KeyboardButton(text="Karta ma'lumotini saqlash💳")],
    [KeyboardButton(text="Bosh sahifaga qaytish🔙"), KeyboardButton(text="Kartalarim🗂")]
], resize_keyboard=True)