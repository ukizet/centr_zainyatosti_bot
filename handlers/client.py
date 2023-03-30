from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from create_bot import dp
from keyboards import client_kb, admin_kb
from database import db


class Buttons_handlers():
    async def admin_panel(self, message: types.Message):
        await message.answer(reply_markup=admin_kb, text='admin panel')
        pass

    async def command_schedule(self, message: types.Message):
        await message.answer('з 08:00 до 17:00')

    async def command_menu(self, message: types.Message):
        # await db.sql_read(message=message)
        # await message.answer('Ще в розробці', reply_markup=client_kb)
        for vacancy in await db.db_obj.select_data(message, 'vacancies', '*'):
            await message.answer(f'Назва вакансії: {vacancy[2]}\nОпис: {vacancy[3]}\nЗП: {vacancy[4]}')


buttons_handlers_obj = Buttons_handlers()


async def command_start(message: types.Message):
    await message.answer('Виберіть потрібний розділ нижче👇', reply_markup=client_kb)


def reg_handlers_client(dp: Dispatcher):
    def reg_buttons():
        dp.register_message_handler(
            buttons_handlers_obj.admin_panel, Text(equals='Панель адміна'))
        dp.register_message_handler(
            buttons_handlers_obj.command_schedule, Text(equals='Графік роботи'))
        dp.register_message_handler(
            buttons_handlers_obj.command_menu, Text(equals='Меню'))

    reg_buttons()

    dp.register_message_handler(command_start)
