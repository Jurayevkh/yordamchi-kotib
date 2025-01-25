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

verifyKeyboards=ReplyKeyboardMarkup(keyboard=[
    [ KeyboardButton(text="Chop etishga tasdiqlash ✅"),
        KeyboardButton(text="Bekor qilish ❌")]
], resize_keyboard=True)