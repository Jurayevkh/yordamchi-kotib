from aiogram.fsm.state import StatesGroup, State

class Currency(StatesGroup):
    amount = State()