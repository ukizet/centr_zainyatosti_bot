from aiogram.dispatcher.filters.state import State, StatesGroup

class Change(StatesGroup):
    id = State()
    choice = State()
    name = State()
    status = State()
    desc = State()
    salary = State()
    condition = State()
