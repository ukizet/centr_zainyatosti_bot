from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from create_bot import dp
from keyboards import client_kb, admin_kb, get_inline_kb
from database import db

class ButtonsHandlers():
    def __init__(self):
        self.command_menu = CommandMenuHandlers()

    async def admin_panel(self, message: types.Message):
        await message.answer(reply_markup=admin_kb, text='admin panel')
        pass

    async def command_schedule(self, message: types.Message):
        await message.answer('з 08:00 до 17:00')

class CommandMenuHandlers:
    def __init__(self):
        # self.Buttons_handlers_obj = Buttons_handlers_obj
        self.page = 1
        self.previous_page = 0
        self.VACANCIES_PER_PAGE = 5
        self.inline_kb = InlineKeyboardMarkup().row(InlineKeyboardButton(text="◀️", callback_data="back"), InlineKeyboardButton(
            text=f"{self.page}", callback_data="page"), InlineKeyboardButton(text="▶️", callback_data="next"))
        
    async def display_menu(self, message: types.Message = None, callbackQuery: types.CallbackQuery = None):
            self.all_vacancies = await db.db_obj.select_data(message, 'vacancies', '*')

            self.inline_kb = InlineKeyboardMarkup().row(InlineKeyboardButton(text="◀️", callback_data="back"), InlineKeyboardButton(
                text=f"{self.page}", callback_data="page"), InlineKeyboardButton(text="▶️", callback_data="next"))

            self.vacs_list = self.all_vacancies[self.previous_page *
                                                self.VACANCIES_PER_PAGE:self.page*self.VACANCIES_PER_PAGE]
            for i, vac in enumerate(self.vacs_list):
                if callbackQuery is None:
                    if i == 4:
                        await message.answer(f'Назва вакансії: {vac[2]}\nОпис: {vac[3]}\nЗП: {vac[4]}', reply_markup=self.inline_kb)
                    else:
                        await message.answer(f'Назва вакансії: {vac[2]}\nОпис: {vac[3]}\nЗП: {vac[4]}')
                else:
                    if i == 4:
                        await callbackQuery.message.answer(f'Назва вакансії: {vac[2]}\nОпис: {vac[3]}\nЗП: {vac[4]}', reply_markup=self.inline_kb)
                    else:
                        await callbackQuery.message.answer(f'Назва вакансії: {vac[2]}\nОпис: {vac[3]}\nЗП: {vac[4]}')

    async def inline_button_back(self, callbackQuery: types.CallbackQuery):
            if len(self.all_vacancies) <= self.VACANCIES_PER_PAGE:
                return
            if self.page <= 1:
                return
            self.previous_page = self.page-2
            self.page -= 1

            await self.button_menu(callbackQuery=callbackQuery)

    async def inline_button_next(self, callbackQuery: types.CallbackQuery):
            if len(self.all_vacancies) <= self.VACANCIES_PER_PAGE:
                return
            self.previous_page = self.page
            self.page += 1
            await self.button_menu(callbackQuery=callbackQuery)