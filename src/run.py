import asyncio
from operator import contains

import aiogram

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InlineQuery, \
    InlineQueryResultLocation

from InlineModeKeyboards import locationOrCard
from currencyKeyboards import currencyMenu

from database.models import async_main
import database.requests as request
from config import ADMINS
import states
from database.requests import get_locationsByUserID
from inlinekeyboard import post_inline, adminKeys
from states import Currency, Vacancy, Location
from conversionExchange import conversionCurrency
from aiogram.fsm.context import FSMContext
from keyboards import main_menu, verifyKeyboards
from translateTo import translateToSomeLang

bot = Bot(token="8085414300:AAFwDAw72RYKsB9tzoN_AfrLtGRR8bLa8q0")
dp = Dispatcher()


@dp.message(CommandStart())
async def say_hello(message: Message):
    await request.set_user(message.from_user.id)
    msg = (
        f"👋 Salom {message.from_user.first_name}! \n\n"
        f"<b>Yordamchi Kotib</b> biznes yordamchisiman. "
        f"Quyidagi bo'limlardan birini tanlang. "
        f"Botni ishlatish bo'yicha /help buyrug'i orqali ma'lumot olishingiz mumkin."
    )
    await message.reply(text=msg, parse_mode="HTML", reply_markup=main_menu)

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
#
# ################

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

   await message.answer(text=msg, reply_markup=post_inline)

   await state.clear()

##########################################

@dp.message(F.text=="Ma'lumotlarni inlinega saqlash📍")
async def SaveDataToInline(message: Message):
    await message.reply(text="Qanday turdagi ma'lumotni saqlamoqchisiz?:", reply_markup=locationOrCard)

@dp.message(F.text=="Manzil saqlash📍")
async def StartSaveLocation(message: Message, state: FSMContext):
    await message.reply("Manzil nomini kiriting:")
    await state.set_state(Location.Title)

@dp.message(Location.Title)
async def AskLocation(message: Message, state: FSMContext):
    await state.update_data(Title=message.text)
    await message.reply("Manzilni yuboring:")
    await state.set_state(Location.Latitude)

@dp.message(Location.Latitude)
async def GetLocation(message: Message, state: FSMContext):
    if message.location:
        data = await state.get_data()
        title=data.get("Title")
        await request.set_location(message.from_user.id,title,message.location.latitude,message.location.longitude)
        await state.update_data(Latitude=message.location.latitude)
        await state.update_data(Longitude=message.location.longitude)
        await message.reply(f"Bu qayerni manzili? {message.location.latitude} {message.location.longitude}")
    else:
        await message.reply("Bu manzil emas, manzil yuboring")

@dp.inline_query()
async def show_datas(inline_query: InlineQuery):
    locations=await get_locationsByUserID(inline_query.from_user.id)
    print(locations)

    results=[]
    for location in locations:
        results.append(InlineQueryResultLocation(
            id=str(location.id),
            latitude=location.latitude,
            longitude=location.longitude,
            title=location.title
        ))

    # result=[
    #     InlineQueryResultLocation(id="001",latitude=41.332275574486246, longitude=69.27493543669588 ,title="Minor Masjidi"),
    #     InlineQueryResultLocation(id="002",latitude=41.32731276661643, longitude=69.28338975906, title="Minor metrosi")
    # ]
    await bot.answer_inline_query(inline_query.id, results)


# @dp.message(Vacancy.Comment)
# async def VacancyComment(message: Message, state: FSMContext):
#    data = await state.get_data()
#    title = data.get("Title")
#    requirements = data.get("Requirements")
#    salary = data.get("Salary")
#    company = data.get("Company")
#    responsible = data.get("Responsible")
#    comment = message.text
#
#    msg = (
#        f"Lavozim: {title}\n"
#        f"Talablar: {requirements}\n"
#        f"Maosh: {salary}\n"
#        f"Kompaniya: {company}\n"
#        f"Ma'sul shaxs: {responsible}\n"
#        f"Qo'shimcha izoh: {comment}\n\n"
#    )
#
#    await state.update_data(Mention=f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>""")
#    await state.update_data(Post=msg)
#    msg+="Ushbu postni tasdiqlashga yuborasizmi?"
#
#    await message.answer(text=msg, reply_markup=post_inline)

#####################################

# @dp.callback_query(F.data=="action", Vacancy.Comment)
# async def sendPostToAdmin(callback: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     post = data.get("Post")
#     await sendPostToChannel(callback, state)
#
#
# async def sendPostToChannel(callback: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     post = data.get("Post")
#     mention = data.get("Mention")
#     msg = f"Foydalanuvchi {mention} quyidagi postni yubormoqchi:\n\n"
#     msg += post
#     await bot.send_message(chat_id=ADMINS, text=msg, parse_mode="HTML", reply_markup=adminKeys)
#     if(F.data=="accept"):
#         print("Admin tasdiqladi")
#         await bot.send_message(chat_id="@kotib_vakansiyalar",text=post)
#         await callback.answer("Post kanalga joylandi", show_alert=True)

#############################

# @dp.callback_query(F.data == "action", Vacancy.Comment)
# async def sendPostToAdmin(callback: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     post = data.get("Post")
#     mention = data.get("Mention")
#     msg = f"Foydalanuvchi {mention} quyidagi postni yubormoqchi:\n\n"
#     msg += post
#
#     # Send to admin
#     await bot.send_message(chat_id=ADMINS, text=msg, parse_mode="HTML", reply_markup=adminKeys)
#     await callback.answer("Post admin uchun yuborildi. Iltimos, tasdiqlang.")
#
#
# @dp.callback_query(F.data == "accept")
# async def acceptPost(callback: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     post = data.get("Post")
#
#     # Send to channel if accepted
#     await bot.send_message(chat_id="@kotib_vakansiyalar", text=post)
#     await callback.answer("Post kanalga joylandi", show_alert=True)


async def main():
    await async_main()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

