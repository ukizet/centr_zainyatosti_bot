from aiogram.dispatcher.filters.state import State, StatesGroup

class Delete(StatesGroup):
    name = State()
    id = State()