from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from keyboards import client_kb
from classes.buttons_handlers import ButtonsHandlers


async def command_start(message: types.Message):
    await message.answer('Виберіть потрібний розділ нижче👇', reply_markup=client_kb)


def reg_handlers(dp: Dispatcher):
    def reg_buttons():
        buttons_handlers_obj = ButtonsHandlers()
        dp.register_message_handler(
            buttons_handlers_obj.admin_panel, Text(equals='Панель адміна'))
        dp.register_message_handler(
            buttons_handlers_obj.command_schedule, Text(equals='Графік роботи'))
        dp.register_message_handler(
            buttons_handlers_obj.command_menu.display_menu, Text(equals='Меню'))
        dp.register_callback_query_handler(
            buttons_handlers_obj.command_menu.inline_button_back, text='back')
        dp.register_callback_query_handler(
            buttons_handlers_obj.command_menu.inline_button_next, text='next')
    reg_buttons()

    dp.register_message_handler(command_start)
