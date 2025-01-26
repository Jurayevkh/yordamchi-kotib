from aiogram.fsm.state import StatesGroup, State

class Currency(StatesGroup):
    which_currency = State()
    to_which_currency= State()
    amount = State()

class Vacancy(StatesGroup):
    Title=State()
    Requirements=State()
    Salary=State()
    Company=State()
    Responsible=State()
    Comment=State()
    Mention=State()
    Post=State()
    VerifyByAdmin=State()

class Location(StatesGroup):
    Title=State()
    Latitude=State()
    Longitude=State()

class Card(StatesGroup):
    CardName=State()
    CardNumber=State()
    CardOwner=State()

class Meeting(StatesGroup):
    Name=State()
    Date=State()
    Time=State()
    Description=State()
    