from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()

# Add buttons
builder.button(text="Yuborish", callback_data="action")
builder.button(text="Bekor qilish", callback_data="rejection")

# Arrange buttons in a row
builder.adjust(2)

# Convert to InlineKeyboardMarkup
post_inline = builder.as_markup()
