from aiogram.fsm.state import StatesGroup, State

class UserRegister(StatesGroup):
    name = State()
    number = State()
    account = State()