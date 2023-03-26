from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

# from database import sqlite_db
from keyboards import client_kb, cancel_button

class MyStatesGroup(StatesGroup):
    name = State()
    desc = State()
    salary = State()


async def buttons_handlers():
    global button_start, button_cancel

    async def button_start(message : types.Message):
        await MyStatesGroup.name.set()
        await message.answer('Пишіть назву вакансії', reply_markup=cancel_button)

    async def button_cancel(message : types.Message, state : FSMContext):
        current_state = await state.get_state()
        print(f'current_state: {current_state}')
        if current_state is None:
            # print(f'current_state: IS NONE!!!')
            return
        await state.finish()
        await message.reply('OK', reply_markup=client_kb)


async def states_handlers():
    global load_template, load_name, load_desc, load_salary

    async def load_template(message: types.Message, state: FSMContext, load_type: str, text: str='', finish: bool=False, test: bool=False):
        async def state_proxy_with_test():
            if test == True:
                return
            return await state.proxy()
        
        if load_type == 'photo':
            async with state_proxy_with_test() as data:
                data['photo'] = message.photo[0].file_id
        else:
            async with state_proxy_with_test() as data:
                data[f'{load_type}'] = message.text
        if finish == True:
            async with state_proxy_with_test() as data:
                await message.answer(str(data), reply_markup=client_kb)

            # await sqlite_db.sql_add(state=state)
            await state.finish()
        else:
            await MyStatesGroup.next()

    async def load_name(message: types.Message, state: FSMContext):
        await load_template(message=message, state=state, load_type='name', text='Пишіть опис вакансії')

    async def load_desc(message: types.Message, state: FSMContext):
        await load_template(message=message, state=state, load_type='desc', text='Пишіть ЗП')

    async def load_salary(message: types.Message, state: FSMContext):
        await load_template(message=message, state=state, load_type='salary', text='', finish=True)


def reg_handlers_admin(dp: Dispatcher):
    def reg_buttons():
        dp.register_message_handler(button_start, Text(equals='Додати вакансію'), state=None)
        dp.register_message_handler(button_cancel, Text(equals='Відміна'), state="*")

    def reg_states_handlers():
        dp.register_message_handler(load_name, state=MyStatesGroup.name)
        dp.register_message_handler(load_desc, state=MyStatesGroup.desc)
        dp.register_message_handler(load_salary, state=MyStatesGroup.salary)

    reg_buttons()
    reg_states_handlers()

