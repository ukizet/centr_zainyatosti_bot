from aiogram.dispatcher.filters.state import State, StatesGroup

class Add(StatesGroup):
    name = State()
    desc = State()
    salary = State()
