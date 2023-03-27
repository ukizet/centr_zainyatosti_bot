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


class ChangeVacancy(StatesGroup):
    id = State()
    name = State()


def buttons_handlers():
    global button_add, button_cancel, button_delete, button_change, button_show

    async def button_add(message: types.Message):
        await AddVacancy.name.set()
        await message.answer('Пишіть назву вакансії', reply_markup=cancel_button)

    async def button_change(message: types.Message):
        await message.answer('Ще в розробці', reply_markup=client_kb)
        await ChangeVacancy.id.set()
        await message.answer('Введіть id вакансії яку треба змінити', reply_markup=cancel_button)

    async def button_delete(message: types.Message):
        # await message.answer('Ще в розробці', reply_markup=client_kb)
        await DeleteVacancy.id.set()
        await message.answer('Введіть id вакансії яку треба видалити', reply_markup=cancel_button)
        pass

    async def button_show(message: types.Message):
        await db.sql_read_admin(message=message)

    async def button_cancel(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        print(f'current_state: {current_state}')
        if current_state is None:
            # print(f'current_state: IS NONE!!!')
            return
        await state.finish()
        await message.answer('Операція була скасована', reply_markup=client_kb)


def addVacancy_states_handlers():
    global load_template, load_name, load_desc, load_salary

    async def load_template(message: types.Message, state: FSMContext, load_type: str, text: str = '', finish: bool = False, test: bool = False):
        def getmsg():
            if test:
                if load_type == 'salary':
                    return random.randint(10000, 99999)
                return ''.join(random.choice(letters) for i in range(5))
            return message.text

        async with state.proxy() as data:
            data[f'{load_type}'] = getmsg()
        if finish == True:
            async with state.proxy() as data:
                await message.answer(str(data), reply_markup=client_kb)

            await db.sql_add(state=state)
            async with state.proxy() as data:
                db.db_obj.insert_data('vacancies', 
                                   'name, desc, salary', f"'{data['name']}', '{data['desc']}', '{data['salary']}'")
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


async def del_vacancy(message: types.Message, state: FSMContext):
    await db.sql_delete(message=message)
    await state.finish()
    await message.answer('Вакансія була видалена', reply_markup=client_kb)
    pass


async def changeVacancy_get_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = int(message.text)
    await ChangeVacancy.name.set()
    await message.answer('Введіть нову назву вакансії', reply_markup=cancel_button)


async def changeVacancy_get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await db.sql_change(message=message, state=state)
    await state.finish()
    await message.answer('Вакансія була змінена', reply_markup=client_kb)

buttons_handlers()
addVacancy_states_handlers()


def reg_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        button_cancel, Text(equals='Відміна'), state="*")

    def reg_buttons():
        dp.register_message_handler(button_add, Text(
            equals='Додати вакансію'), state=None)
        dp.register_message_handler(
            button_change, Text(equals='Змінити вакансію'))
        dp.register_message_handler(
            button_delete, Text(equals='Видалити вакансію'))
        dp.register_message_handler(
            button_show, Text(equals='Показати вакансії'))

    def reg_addVacancy_handlers():
        dp.register_message_handler(load_name, state=AddVacancy.name)
        dp.register_message_handler(load_desc, state=AddVacancy.desc)
        dp.register_message_handler(load_salary, state=AddVacancy.salary)

    dp.register_message_handler(del_vacancy, state=DeleteVacancy.id)

    dp.register_message_handler(changeVacancy_get_id, state=ChangeVacancy.id)
    dp.register_message_handler(
        changeVacancy_get_name, state=ChangeVacancy.name)

    reg_buttons()
    reg_addVacancy_handlers()
