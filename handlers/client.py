from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from create_bot import dp
from keyboards import client_kb, admin_kb
# from database import sqlite_db

def buttons_handlers():
    global command_when_we_work, command_menu, admin_panel

    async def admin_panel(message: types.Message):
        await message.answer(reply_markup=admin_kb, text='admin panel')
        pass

    async def command_when_we_work(message: types.Message):
        await message.answer('з 08:00 до 17:00')

    async def command_menu(message: types.Message):
        # await sqlite_db.sql_read(message=message)
        await message.answer('Ще в розробці', reply_markup=client_kb)
        pass


buttons_handlers()

async def command_start(message: types.Message):
    await message.answer('Виберіть потрібний розділ нижче👇', reply_markup=client_kb)

def reg_handlers_client(dp: Dispatcher):
    def reg_buttons():
        dp.register_message_handler(admin_panel, Text(equals='Панель адміна'))
        dp.register_message_handler(command_when_we_work, Text(equals='Графік роботи'))
        dp.register_message_handler(command_menu, Text(equals='Меню'))
    
    
    reg_buttons()
    
    dp.register_message_handler(command_start)