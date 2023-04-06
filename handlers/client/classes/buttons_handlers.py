from aiogram import types

from dataclasses import dataclass

from keyboards import admin_kb
from command_menu_handlers import CommandMenuHandlers

@dataclass
class ButtonsHandlers:
    command_menu: CommandMenuHandlers
    
    def __init__(self):
        self.command_menu = CommandMenuHandlers()

    async def admin_panel(self, message: types.Message):
        await message.answer(reply_markup=admin_kb, text='admin panel')
        pass

    async def command_schedule(self, message: types.Message):
        await message.answer('з 08:00 до 17:00')
