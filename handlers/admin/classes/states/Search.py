from aiogram.dispatcher.filters.state import State, StatesGroup

class Search(StatesGroup):
    name = State()