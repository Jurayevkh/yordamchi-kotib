import asyncio
from operator import contains

import aiogram

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message

from currencyKeyboards import currencyMenu
import states
from inlinekeyboard import post_inline
from states import Currency, Vacancy
from conversionExchange import conversionCurrency
from aiogram.fsm.context import FSMContext
from keyboards import main_menu
from translateTo import translateToSomeLang

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
    await message.reply(text="Qiymatni kiritmoqchi bo'lgan valyutangizni tanlang", reply_markup=currencyMenu)
    await state.set_state(Currency.which_currency)

@dp.message(Currency.which_currency)
async def getCurrency(message: Message, state: FSMContext):
    if(message.text not in ["🇺🇿UZS","🇺🇸USD","🇪🇺EUR","🇷🇺RUB"]):
        await message.reply(text="Noto'g'ri ma'lumot yubordingiz, quyidagi valyutalardan birini tanlang:", reply_markup=currencyMenu)
        return
    currency = message.text[2:]
    await state.update_data(which_currency=currency)
    await state.set_state(Currency.to_which_currency)
    await message.answer(text="Qaysi valyutada hisoblamoqchisiz")

    # result=conversionCurrency(float(amount))
    # answer_message=f"{amount} dollarda ${result} bo'ladi"
    # await message.reply(text=answer_message)
    # await state.clear()
@dp.message(Currency.to_which_currency)
async def getToWhichCurrency(message: Message, state: FSMContext):
    if(message.text not in ["🇺🇿UZS","🇺🇸USD","🇪🇺EUR","🇷🇺RUB"]):
        await message.reply(text="Noto'g'ri ma'lumot yubordingiz, quyidagi valyutalardan birini tanlang:", reply_markup=currencyMenu)
        return
    currency = message.text[2:]
    await state.update_data(to_which_currency=currency)
    await state.set_state(Currency.amount)
    await message.answer(text="Hisoblamoqchi bo'lgan qiymatingizni kiriting:")

@dp.message(Currency.amount)
async def getAmount(message: Message, state:FSMContext):
    if(message.text.isdigit()==False):
        await message.reply(text="Noto'g'ri ma'lumot kiritdingiz! Summa kiriting")
        return
    data= await state.get_data()
    which_currency= data.get("which_currency")
    to_which_currency= data.get("to_which_currency")
    result = conversionCurrency(which_currency,to_which_currency,float(message.text))
    answer_msg=f"{message.text} {which_currency} = {result} {to_which_currency}"
    await message.answer(text=answer_msg, reply_markup=main_menu)
    await state.clear()

################

@dp.message(F.text=="Vakansiya ochish💼")
async def CreateVacancy(message: Message, state: FSMContext):
    await message.reply(text="Qidiralayotgan xodim lavozimi:")
    await state.set_state(Vacancy.Title)

@dp.message(Vacancy.Title)
async def VacancyTitle(message: Message, state: FSMContext):
   await state.update_data(Title=message.text)
   await message.answer(text="Talablarni kiriting:")
   await state.set_state(Vacancy.Requirements)

@dp.message(Vacancy.Requirements)
async def VacancyRequirements(message: Message, state: FSMContext):
   await state.update_data(Requirements=message.text)
   await message.answer(text="Taklif qilinayotgan maoshni kiriting:")
   await state.set_state(Vacancy.Salary)

@dp.message(Vacancy.Salary)
async def VacancySalary(message: Message, state: FSMContext):
   await state.update_data(Salary=message.text)
   await message.answer(text="Kompaniya nomini kiriting:")
   await state.set_state(Vacancy.Company)

@dp.message(Vacancy.Company)
async def VacancyCompany(message: Message, state: FSMContext):
   await state.update_data(Company=message.text)
   await message.answer(text="Murojaat uchun ma'sul shaxs ma'lumotalari(telefon raqam/telegram hisob):")
   await state.set_state(Vacancy.Responsible)

@dp.message(Vacancy.Responsible)
async def VacancyResponsible(message: Message, state: FSMContext):
   await state.update_data(Responsible=message.text)
   await message.answer(text="Qo'shimcha izoh:")
   await state.set_state(Vacancy.Comment)

@dp.message(Vacancy.Comment)
async def VacancyComment(message: Message, state: FSMContext):
   data = await state.get_data()
   title = data.get("Title")
   requirements = data.get("Requirements")
   salary = data.get("Salary")
   company = data.get("Company")
   responsible = data.get("Responsible")
   comment = message.text

   msg = (
       f"Lavozim:{title}\n"
       f"Talablar:{requirements}\n"
       f"Maosh:{salary}\n"
       f"Kompaniya:{company}\n"
       f"Ma'sul shaxs:{responsible}\n"
       f"Qo'shimcha izoh:{comment}\n"
   )

   # russian=translateToSomeLang(msg,"ru")
   # english=translateToSomeLang(msg,"en")
   # msg+=russian
   # msg+=english

   await message.answer(text=msg, reply_markup=post_inline)

   await state.clear()






async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

