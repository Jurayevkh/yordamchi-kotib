import asyncio
from operator import contains

import aiogram

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InlineQuery, \
    InlineQueryResultLocation, InputMessageContent, InlineQueryResultArticle

from InlineModeKeyboards import locationOrCard
from currencyKeyboards import currencyMenu

from database.models import async_main
import database.requests as request
from config import ADMINS
import states
from database.requests import get_locationsByUserID, get_cardsByUserID
from inlinekeyboard import post_inline, adminKeys
from states import Currency, Vacancy, Location, Card
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

# @dp.message(F.text=="Uchrashuv belgilash⏰")
# async def TimeManagingStart(message: Message):


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
    await message.reply(text="<b>👨‍💼Xodim:</b>\n\n<i>Qidiralayotgan xodim lavozimi(Misol uchun dasturchi, mobilograf):</i>", parse_mode="HTML")
    await state.set_state(Vacancy.Title)

@dp.message(Vacancy.Title)
async def VacancyTitle(message: Message, state: FSMContext):
   await state.update_data(Title=message.text)
   await message.answer(text="<b>📑Talablar:</b>\n\n<i>Talab qilinadigan soft va hard skillarni kiriting:</i>", parse_mode="HTML")
   await state.set_state(Vacancy.Requirements)

@dp.message(Vacancy.Requirements)
async def VacancyRequirements(message: Message, state: FSMContext):
   await state.update_data(Requirements=message.text)
   await message.answer(text="<b>💵Maosh:</b>\n\n<i>Taklif qilinayotgan maoshni kiriting:</i>", parse_mode="HTML")
   await state.set_state(Vacancy.Salary)

@dp.message(Vacancy.Salary)
async def VacancySalary(message: Message, state: FSMContext):
   await state.update_data(Salary=message.text)
   await message.answer(text="<b>🏢Kompaniya nomini kiriting:</b>", parse_mode="HTML")
   await state.set_state(Vacancy.Company)

@dp.message(Vacancy.Company)
async def VacancyCompany(message: Message, state: FSMContext):
   await state.update_data(Company=message.text)
   await message.answer(text="<b>📞Aloqa:</b>\n\n<i>Murojaat uchun ma'sul shaxs telefon raqami:</i>", parse_mode="HTML")
   await state.set_state(Vacancy.Responsible)

@dp.message(Vacancy.Responsible)
async def VacancyResponsible(message: Message, state: FSMContext):
   await state.update_data(Responsible=message.text)
   await message.answer(text="<b>✍️Qo'shimcha izoh:</b>\n\n<i>Ish, bo'sh ish o'rni, taklif kabilarni yozib qoldiring</i>", parse_mode="HTML")
   await state.set_state(Vacancy.Comment)


@dp.message(F.text=="Ma'lumotlarni inlinega saqlash📍")
async def SaveDataToInline(message: Message):
    await message.reply(text="Qanday turdagi ma'lumotni saqlamoqchisiz?:", reply_markup=locationOrCard)

@dp.message(F.text=="Bosh sahifaga qaytish🔙")
async def BackToMenu(message:Message):
    await message.answer(text="Bosh sahifadasiz!",reply_markup=main_menu)


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
        print("!!!!")
        await state.update_data(Latitude=message.location.latitude)
        await state.update_data(Longitude=message.location.longitude)
        await message.reply("Manzil muvaffaqiyatli saqlandi ✅", reply_markup=main_menu)
        await state.clear()
    else:
        await message.reply("Bu manzil emas, manzil yuboring!")

@dp.inline_query()
async def show_datas(inline_query: InlineQuery):
    locations=await get_locationsByUserID(inline_query.from_user.id)

    results=[]
    for location in locations:
        if (location.user_id == inline_query.from_user.id):
            results.append(InlineQueryResultLocation(
                id=str(location.id),
                latitude=location.latitude,
                longitude=location.longitude,
                description=location.title,
                title=location.title
            ))
        print("-----")

    await bot.answer_inline_query(inline_query.id, results)

@dp.message(F.text=="Karta ma'lumotini saqlash💳")
async def StartSaveCard(message: Message, state: FSMContext):
    await message.reply("Karta nomini kiriting:")
    await state.set_state(Card.CardName)

@dp.message(Card.CardName)
async def AskCardNumber(message:Message, state:FSMContext):
    await state.update_data(CardName=message.text)
    await message.reply("Karta raqamini kiriting:")
    await state.set_state(Card.CardNumber)

@dp.message(Card.CardNumber)
async def AskCardOwner(message:Message, state:FSMContext):
    await state.update_data(CardNumber=message.text)
    await message.reply("Karta egasini kiriting:")
    await state.set_state(Card.CardOwner)

@dp.message(Card.CardOwner)
async def GetCardData(message:Message, state: FSMContext):
    await state.update_data(CardOwner=message.text)
    data = await state.get_data()
    cardName=data.get("CardName")
    cardNumber=data.get("CardNumber")
    cardOwner=message.text
    await request.set_card(message.from_user.id,cardName,cardNumber,cardOwner)
    await message.reply("Karta muvaffaqiyatli saqlandi ✅", reply_markup=main_menu)
    await state.clear()


@dp.message(F.text=="Kartalarim🗂")
async def GetAllCards(message:Message):
    cards=await request.get_cardsByUserID(message.from_user.id)

    if not cards:
        await message.answer(text="Siz hali karta qo'shmagansiz!")
    for card in cards:
        await message.answer(text=f"<b>Karta nomi:</b> {card.cardname}\n\n<b>Karta raqam:</b> {card.cardnumber}\n\n<b>Karda egasi:</b> {card.cardowner}", parse_mode="HTML")


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
       f"<b>Xodim qidirilmoqda!</b>\n\n"
       f"<b>👨‍💼Lavozim:</b> {title}\n"
       f"<b>📑Talablar</b>: {requirements}\n"
       f"<b>💵Maosh:</b> {salary}\n"
       f"<b>🏢Kompaniya:</b> {company}\n"
       f"<b>📞Aloqa:</b>: {responsible}\n"
       f"<b>✍️Qo'shimcha izoh:</b> {comment}\n\n"
       f"@yordamchi_kotib_bot - sizning biznes yordamchingiz\n"
       "@kotib_vakansiyalar - orzuingdagi ishni top"
   )

   await state.update_data(Mention=f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>""")
   await state.update_data(Post=msg)
   msg+="Ushbu postni tasdiqlashga yuborasizmi?"

   await message.answer(text=msg,parse_mode="HTML",reply_markup=post_inline)

@dp.callback_query(F.data == "action", Vacancy.Comment)
async def sendPostToAdmin(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    post = data.get("Post")
    mention = data.get("Mention")
    msg = f"Foydalanuvchi {mention} quyidagi postni yubormoqchi:\n\n"
    msg += post
    await bot.send_message(chat_id=ADMINS, text=msg, parse_mode="HTML", reply_markup=adminKeys)
    await state.set_state(Vacancy.VerifyByAdmin)

@dp.callback_query(F.data=="rejection", Vacancy.Comment)
async def rejectPost(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup()
    await callback.message.answer("Post rad etildi.")

@dp.callback_query(F.data == "accept", Vacancy.VerifyByAdmin)
async def sendtPostToChannel(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    post = data.get("Post")
    await bot.send_message(chat_id="@kotib_vakansiyalar",text=post, parse_mode="HTML")
    await callback.answer("Post kanalga joylandi", show_alert=True)

@dp.callback_query(F.data=="rejectionByAdmin", Vacancy.VerifyByAdmin)
async def rejectPostByAdmin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer("Post rad etildi.", show_alert=True)
    await callback.message.edit_reply_markup()

async def main():
    await async_main()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

