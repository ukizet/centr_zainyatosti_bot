from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

import inspect

from dataclasses import dataclass

from ButtonsHandlers import ButtonsHandlers


@dataclass
class RegHandlers:
    dp: Dispatcher
    buttons_handlers_obj: ButtonsHandlers

    def __init__(self, dp: Dispatcher):
        self.dp = dp

    def reg_all(self):
        methods = [method for method in dir(self.__class__.__name__) if callable(
            getattr(self.__class__.__name__, method)) and not method.startswith("__")]
        for method in methods:
            if method != inspect.currentframe().f_code.co_name:
                getattr(self, method)()

    def buttons(self):
        button = ButtonsHandlers()
        self.dp.register_message_handler(
            button.button_cancel, Text(equals='Відміна'), state="*")

        self.dp.register_message_handler(button.add, Text(
            equals='Додати вакансію'), state=None)
        self.dp.register_message_handler(
            button.change, Text(equals='Змінити вакансію'))
        self.dp.register_message_handler(
            button.delete, Text(equals='Видалити вакансію'))
        self.dp.register_message_handler(
            button.show, Text(equals='Показати вакансії'))
        self.dp.register_message_handler(
            button.search, Text(equals='Пошук вакансій'))

    def add(self):
        addVacancy_states_handlers_obj = AddVacancyStatesHandlers()
        self.dp.register_message_handler(
            addVacancy_states_handlers_obj.load_name, state=AddVacancy.name)
        self.dp.register_message_handler(
            addVacancy_states_handlers_obj.load_desc, state=AddVacancy.desc)
        self.dp.register_message_handler(
            addVacancy_states_handlers_obj.load_salary, state=AddVacancy.salary)

    def delete(self):
        self.dp.register_message_handler(del_vacancy, state=DeleteVacancy.id)

    def change(self):
        change_obj = ChangeVacancyStatesHandlers()
        self.dp.register_message_handler(
            change_obj.id, state=ChangeVacancy.id)
        self.dp.register_message_handler(
            change_obj.choice, state=ChangeVacancy.choice)
        self.dp.register_message_handler(
            change_obj.status, state=ChangeVacancy.status)
        self.dp.register_message_handler(
            change_obj.name, state=ChangeVacancy.name)
        self.dp.register_message_handler(
            change_obj.desc, state=ChangeVacancy.desc)
        self.dp.register_message_handler(
            change_obj.salary, state=ChangeVacancy.salary)

    def search(self):
        self.dp.register_message_handler(
            searchVacancy_handle_name, state=SearchVacancy.name)
