import asyncio

import aiogram

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from keyboards import main_menu

bot = Bot(token="8085414300:AAFwDAw72RYKsB9tzoN_AfrLtGRR8bLa8q0")
dp = Dispatcher()

@dp.message(CommandStart())
async def say_hello(message: Message):
    msg = (
        f"👋 Salom {message.from_user.first_name}\\! \n\n"
        f"*Yordamchi Kotib* biznes yordamchisiman\\. "
        f"Quyidagi bo\\'limlardan birini tanlang\\. "
        f"Botni ishlatish bo\\'yicha /help buyrug\\'i orqali ma\\'lumot olishingiz mumkin\\."
    )
    await message.reply(text=msg, parse_mode="MarkdownV2", reply_markup=main_menu)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

