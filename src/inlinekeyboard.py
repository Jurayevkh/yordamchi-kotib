from aiogram.utils.keyboard import InlineKeyboardBuilder

postKeysbuilder = InlineKeyboardBuilder()

# Add buttons
postKeysbuilder.button(text="Yuborish ✅", callback_data="action")
postKeysbuilder.button(text="Bekor qilish ❌", callback_data="rejection")

# Arrange buttons in a row
postKeysbuilder.adjust(2)

# Convert to InlineKeyboardMarkup
post_inline = postKeysbuilder.as_markup()

adminKeysBuilder = InlineKeyboardBuilder()

adminKeysBuilder.button(text="Tasdiqlash ✅", callback_data="accept")
adminKeysBuilder.button(text="Bekor qilish ❌", callback_data="rejectionByAdmin")

adminKeysBuilder.adjust(2)

adminKeys=adminKeysBuilder.as_markup()