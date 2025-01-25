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

