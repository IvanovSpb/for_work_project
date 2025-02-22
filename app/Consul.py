from aiogram.fsm.state import StatesGroup, State

class Consul(StatesGroup):
    name = State()
    number = State()
    account = State()