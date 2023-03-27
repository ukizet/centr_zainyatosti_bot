from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import db
from keyboards import client_kb, cancel_button

import random
import string

# Створити список всіх латинських букв
letters = string.ascii_lowercase

class AddVacancy(StatesGroup):
    name = State()
    desc = State()
    salary = State()

class DeleteVacancy(StatesGroup):
    name = State()
    id = State()

def buttons_handlers():
    global button_add, button_cancel, button_delete, button_change

    async def button_add(message : types.Message):
        await AddVacancy.name.set()
        await message.answer('Пишіть назву вакансії', reply_markup=cancel_button)

    async def button_change(message : types.Message):
        await message.answer('Ще в розробці', reply_markup=client_kb)
        pass

    async def button_delete(message : types.Message):
        await message.answer('Ще в розробці', reply_markup=client_kb)
        pass

    async def button_cancel(message : types.Message, state : FSMContext):
        current_state = await state.get_state()
        print(f'current_state: {current_state}')
        if current_state is None:
            # print(f'current_state: IS NONE!!!')
            return
        await state.finish()
        await message.answer('OK', reply_markup=client_kb)



def add_states_handlers():
    global load_template, load_name, load_desc, load_salary

    async def load_template(message: types.Message, state: FSMContext, load_type: str, text: str='', finish: bool=False, test: bool=False):
        def getmsg():
            if test:
                if load_type == 'salary':
                    return random.randint(10000, 99999)
                return ''.join(random.choice(letters) for i in range(5))
            return message.text

        
        # if load_type == 'photo':
        #     async with state.proxy() as data:
        #         data['photo'] = message.photo[0].file_id
        # else:
        async with state.proxy() as data:
            data[f'{load_type}'] = getmsg()
        if finish == True:
            async with state.proxy() as data:
                await message.answer(str(data), reply_markup=client_kb)

            await db.sql_add(state=state)
            await state.finish()
        else:
            await AddVacancy.next()
            if len(text) > 0:
                await message.answer(f'{text}')
            else:
                pass

    async def load_name(message: types.Message, state: FSMContext):
        await load_template(message=message, state=state, load_type='name', text='Пишіть опис вакансії')

    async def load_desc(message: types.Message, state: FSMContext):
        await load_template(message=message, state=state, load_type='desc', text='Пишіть ЗП')

    async def load_salary(message: types.Message, state: FSMContext):
        await load_template(message=message, state=state, load_type='salary', text='', finish=True)

buttons_handlers()
add_states_handlers()

def reg_handlers_admin(dp: Dispatcher):
    def reg_buttons():
        dp.register_message_handler(button_add, Text(equals='Додати вакансію'), state=None)
        dp.register_message_handler(button_change, Text(equals='Змінити вакансію'))
        dp.register_message_handler(button_delete, Text(equals='Видалити вакансію'))

        dp.register_message_handler(button_cancel, Text(equals='Відміна'), state="*")

    def reg_states_handlers():
        dp.register_message_handler(load_name, state=AddVacancy.name)
        dp.register_message_handler(load_desc, state=AddVacancy.desc)
        dp.register_message_handler(load_salary, state=AddVacancy.salary)

    reg_buttons()
    reg_states_handlers()

