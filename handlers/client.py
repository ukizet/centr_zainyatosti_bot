from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from create_bot import dp
from keyboards import client_kb, admin_kb, get_inline_kb
from database import db


class Buttons_handlers():
    def __init__(self):
        self.page = 1
        self.previous_page = 0
        self.VACANCIES_PER_PAGE = 5
        pass
    async def admin_panel(self, message: types.Message):
        await message.answer(reply_markup=admin_kb, text='admin panel')
        pass

    async def command_schedule(self, message: types.Message):
        await message.answer('з 08:00 до 17:00')

    def command_menu(self):
        async def button_menu(message: types.Message=None, callbackQuery: types.CallbackQuery = None):
            print(f'button_menu')
            print(f'self.page: {self.page}')
            print(f'self.previous_page: {self.previous_page}')

            self.all_vacancies = await db.db_obj.select_data(message, 'vacancies', '*')
            
            self.inline_kb = InlineKeyboardMarkup().row(InlineKeyboardButton(text="◀️", callback_data="back"), InlineKeyboardButton(text=f"{self.page}", callback_data="page"),InlineKeyboardButton(text="▶️", callback_data="next"))

            print(f'self.previous_page*self.VACANCIES_PER_PAGE == {self.previous_page*self.VACANCIES_PER_PAGE} and self.page*self.VACANCIES_PER_PAGE == {self.page*self.VACANCIES_PER_PAGE}')
            self.vacs_list = self.all_vacancies[self.previous_page*self.VACANCIES_PER_PAGE:self.page*self.VACANCIES_PER_PAGE]
            print(f'self.vacs_list: {self.vacs_list}')
            for i, vac in enumerate(self.vacs_list):
                if callbackQuery is None:
                    if i == 4: await message.answer(f'Назва вакансії: {vac[2]}\nОпис: {vac[3]}\nЗП: {vac[4]}', reply_markup=self.inline_kb)
                    else: await message.answer(f'Назва вакансії: {vac[2]}\nОпис: {vac[3]}\nЗП: {vac[4]}')
                else:
                    if i == 4: 
                        
                        print(f'vac: {vac}')
                        # await callbackQuery.answer(f'Назва вакансії: {vac[2]}\nОпис: {vac[3]}\nЗП: {vac[4]}')
                        await callbackQuery.message.answer(f'Назва вакансії: {vac[2]}\nОпис: {vac[3]}\nЗП: {vac[4]}', reply_markup=self.inline_kb)
                    else: await callbackQuery.message.answer(f'Назва вакансії: {vac[2]}\nОпис: {vac[3]}\nЗП: {vac[4]}')
                
        
        async def inline_button_back(callbackQuery: types.CallbackQuery):
            print(f'inline_button_back')
            if len(self.all_vacancies) <= self.VACANCIES_PER_PAGE: 
                print('first if statement')
                return
            if self.page <= 1: 
                print('second if statement')
                return
            self.previous_page = self.page-2
            self.page -= 1
            print(f'self.page: {self.page}')
            print(f'self.previous_page: {self.previous_page}')

            await self.button_menu(callbackQuery=callbackQuery)
        

        async def inline_button_next(callbackQuery: types.CallbackQuery):
            if len(self.all_vacancies) <= self.VACANCIES_PER_PAGE: return
            self.previous_page = self.page
            self.page += 1
            await self.button_menu(callbackQuery=callbackQuery)
        
        
        self.button_menu = button_menu
        self.inline_button_back = inline_button_back
        self.inline_button_next = inline_button_next

        return self
        # for i, vacancy in enumerate(await db.db_obj.select_data(message, 'vacancies', '*'), start=1):
        #     await message.answer(f'Назва вакансії: {vacancy[2]}\nОпис: {vacancy[3]}\nЗП: {vacancy[4]}')

    


async def command_start(message: types.Message):
    await message.answer('Виберіть потрібний розділ нижче👇', reply_markup=client_kb)


def reg_handlers_client(dp: Dispatcher):
    def reg_buttons():
        buttons_handlers_obj = Buttons_handlers()
        dp.register_message_handler(
            buttons_handlers_obj.admin_panel, Text(equals='Панель адміна'))
        dp.register_message_handler(
            buttons_handlers_obj.command_schedule, Text(equals='Графік роботи'))
        dp.register_message_handler(
            buttons_handlers_obj.command_menu().button_menu, Text(equals='Меню'))
        dp.register_callback_query_handler(buttons_handlers_obj.command_menu().inline_button_back, text='back')
        dp.register_callback_query_handler(buttons_handlers_obj.command_menu().inline_button_next, text='next')
    reg_buttons()

    dp.register_message_handler(command_start)

    
