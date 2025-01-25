import asyncio
from operator import contains

import aiogram

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message

import states
from states import Currency
from conversionExchange import conversionCurrency
from aiogram.fsm.context import FSMContext
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




@dp.message(F.text=="Valyuta💱")
async def CurrencyCommand(message: Message, state: FSMContext):
    await message.reply(text="Dollarda qancha bo'lishini bilmoqchi qiymatingizni kiriting:")
    await state.set_state(Currency.amount)

@dp.message(Currency.amount)
async def ConvertCurrencyCommand(message: Message, state: FSMContext):
    amount=message.text
    result=conversionCurrency(float(amount))
    answer_message=f"{amount} dollarda {result} bo'ladi"
    await message.reply(text=answer_message)
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

