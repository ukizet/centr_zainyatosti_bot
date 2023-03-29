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
    # condition = State()


class ChangeVacancy(StatesGroup):
    id = State()
    choice = State()
    new_name = State()
    new_status = State()
    new_desc = State()
    new_salary = State()
    condition = State()


class SearchVacancy(StatesGroup):
    name = State()


def buttons_handlers(function_name: str = None):
    # global button_add, button_cancel, button_delete, button_change, button_show, button_search

    async def button_add(message: types.Message):
        await AddVacancy.name.set()
        await message.answer('Пишіть назву вакансії', reply_markup=cancel_button)

    async def button_change(message: types.Message):
        await message.answer('Ще в розробці', reply_markup=client_kb)
        await ChangeVacancy.id.set()
        # await ChangeVacancy.condition.set()
        await message.answer('Введіть id вакансії яку треба змінити', reply_markup=cancel_button)

    async def button_delete(message: types.Message):
        # await message.answer('Ще в розробці', reply_markup=client_kb)
        await DeleteVacancy.id.set()
        # await DeleteVacancy.condition.set()
        await message.answer('Введіть id вакансії яку треба видалити', reply_markup=cancel_button)
        pass

    async def button_show(message: types.Message):
        # await db.sql_read_admin(message=message)
        for vacancy in await db.db_obj.select_data(message, 'vacancies', '*'):
            await message.answer(f'ID: {vacancy[0]}\nСтатус: {vacancy[1]}\nНазва вакансії: {vacancy[2]}\nОпис: {vacancy[3]}\nЗП: {vacancy[4]}')

    async def button_cancel(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        print(f'current_state: {current_state}')
        if current_state is None:
            # print(f'current_state: IS NONE!!!')
            return
        await state.finish()
        await message.answer('Операція була скасована', reply_markup=client_kb)

    async def button_search(message: types.Message):
        await message.answer('Ще в розробці', reply_markup=client_kb)
        await SearchVacancy.name.set()
        await message.answer('Введіть назву вакансії яку треба знайти', reply_markup=cancel_button)

    if function_name is not None:
        result = eval(function_name)
        return result
    else:
        pass


def addVacancy_states_handlers(function_name: str = None):
    # global load_template, load_name, load_desc, load_salary

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
                await db.db_obj.insert_data(message, 'vacancies',
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

    if function_name is not None:
        result = eval(function_name)
        return result
    else:
        pass


async def del_vacancy(message: types.Message, state: FSMContext):
    try:
        id = int(message.text)
    except:
        await message.answer('Було введено не число. Введіть число')
        return
    await db.sql_delete(message=message)
    await db.db_obj.delete_data(message, 'vacancies', f'id={id}')
    await state.finish()
    await message.answer('Вакансія була видалена', reply_markup=client_kb)
    pass


def changeVacancy_states_handlers(function_name: str = None) -> callable:
    # global handle_id, handle_choice, handle_new_name, handle_new_status, handle_new_desc, handle_new_salary, changeVacancy_handle_condition, handle_name

    async def handle_id(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['id'] = int(message.text)
        # await ChangeVacancy.new_name.set()
        # await message.answer('Введіть нову назву вакансії', reply_markup=cancel_button)
        await ChangeVacancy.choice.set()
        await message.answer('''Введіть\n1 - якщо хочете змінити статус вакансії,\n2 - якщо хочете змінити назву вакансії\n3 - якщо хочете змінити опис вакансії,\n4 - якщо хочете змінити ЗП\n5 - якщо хочете змінити все''',
                             reply_markup=cancel_button)

    async def handle_choice(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            try:
                data['choice'] = int(message.text)
            except:
                await message.answer('Було введено не число. Введіть число')
                return
        if data['choice'] == 1:
            await ChangeVacancy.new_status.set()
            await message.answer('Введіть новий статус вакансії', reply_markup=cancel_button)
        elif data['choice'] == 2:
            await ChangeVacancy.new_name.set()
            await message.answer('Введіть нову назву вакансії', reply_markup=cancel_button)
        elif data['choice'] == 3:
            await ChangeVacancy.new_desc.set()
            await message.answer('Введіть новий опис вакансії', reply_markup=cancel_button)
        elif data['choice'] == 4:
            await ChangeVacancy.new_salary.set()
            await message.answer('Введіть нову ЗП', reply_markup=cancel_button)
        elif data['choice'] == 5:
            await ChangeVacancy.new_status.set()
            await message.answer('Введіть новий статус вакансії', reply_markup=cancel_button)
        else:
            await message.answer('Введено не коректне число', reply_markup=client_kb)
            await state.finish()

    async def handle_new_status(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['status'] = message.text
        if data['choice'] == 5:
            await ChangeVacancy.new_name.set()
            await message.answer('Введіть нову назву вакансії', reply_markup=cancel_button)
        else:
            # await db.sql_change(message=message, state=state)
            await db.db_obj.update_data(message, 'vacancies', f"status='{data['status']}'", f"id={data['id']}")
            await state.finish()
            await message.answer('Вакансія була змінена', reply_markup=client_kb)

    async def handle_new_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['name'] = message.text
        if data['choice'] == 5:
            await ChangeVacancy.new_desc.set()
            await message.answer('Введіть новий опис вакансії', reply_markup=cancel_button)
        else:
            await db.db_obj.update_data(message, 'vacancies', f"name='{data['name']}'", f"id={data['id']}")
            await state.finish()
            await message.answer('Вакансія була змінена', reply_markup=client_kb)

    async def handle_new_desc(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['desc'] = message.text
        if data['choice'] == 5:
            await ChangeVacancy.new_salary.set()
            await message.answer('Введіть нову ЗП', reply_markup=cancel_button)
        else:
            await db.db_obj.update_data(message, 'vacancies', f"desc='{data['desc']}'", f"id={data['id']}")
            await state.finish()
            await message.answer('Вакансія була змінена', reply_markup=client_kb)

    async def handle_new_salary(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['salary'] = message.text
        if data['choice'] == 5:
            await db.db_obj.update_data(message, 'vacancies', f"status='{data['status']}', name='{data['name']}', desc='{data['desc']}',salary='{data['salary']}'", f"id={data['id']}")
            await state.finish()
            await message.answer('Вакансія була змінена', reply_markup=client_kb)
        else:
            await db.db_obj.update_data(message, 'vacancies', f"salary='{data['salary']}'", f"id={data['id']}")
            await state.finish()
            await message.answer('Вакансія була змінена', reply_markup=client_kb)

    if function_name is not None:
        result = eval(function_name)
        return result
    else:
        pass


async def searchVacancy_handle_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    # res = await db.db_obj.select_data(message, 'vacancies', '*', f'name LIKE "%{data["name"]}%"')
    print(data["name"])
    # print(res)
    for vacancy in await db.db_obj.select_data(message, 'vacancies', '*', f'name LIKE "%{data["name"]}%"'):
        await message.answer(f'ID: {vacancy[0]}\nСтатус: {vacancy[1]}\nНазва вакансії: {vacancy[2]}\nОпис: {vacancy[3]}\nЗП: {vacancy[4]}')
    await state.finish()


# addVacancy_states_handlers()
# changeVacancy_states_handlers()


def reg_handlers_admin(dp: Dispatcher):
    def reg_buttons():
        dp.register_message_handler(
            buttons_handlers('button_cancel'), Text(equals='Відміна'), state="*")

        dp.register_message_handler(buttons_handlers('button_add'), Text(
            equals='Додати вакансію'), state=None)
        dp.register_message_handler(
            buttons_handlers('button_change'), Text(equals='Змінити вакансію'))
        dp.register_message_handler(
            buttons_handlers('button_delete'), Text(equals='Видалити вакансію'))
        dp.register_message_handler(
            buttons_handlers('button_show'), Text(equals='Показати вакансії'))
        dp.register_message_handler(buttons_handlers(
            'button_search'), Text(equals='Пошук вакансій'))

    reg_buttons()

    def reg_addVacancy_handlers():
        dp.register_message_handler(addVacancy_states_handlers(
            'load_name'), state=AddVacancy.name)
        dp.register_message_handler(addVacancy_states_handlers(
            'load_desc'), state=AddVacancy.desc)
        dp.register_message_handler(addVacancy_states_handlers(
            'load_salary'), state=AddVacancy.salary)

    reg_addVacancy_handlers()

    dp.register_message_handler(del_vacancy, state=DeleteVacancy.id)
    # dp.register_message_handler(del_vacancy, state=DeleteVacancy.condition)

    def reg_changeVacancy_handlers():
        dp.register_message_handler(changeVacancy_states_handlers(
            'handle_id'), state=ChangeVacancy.id)
        dp.register_message_handler(changeVacancy_states_handlers(
            'handle_choice'), state=ChangeVacancy.choice)
        dp.register_message_handler(changeVacancy_states_handlers(
            'handle_new_status'), state=ChangeVacancy.new_status)
        dp.register_message_handler(changeVacancy_states_handlers(
            'handle_new_name'), state=ChangeVacancy.new_name)
        dp.register_message_handler(changeVacancy_states_handlers(
            'handle_new_desc'), state=ChangeVacancy.new_desc)
        dp.register_message_handler(changeVacancy_states_handlers(
            'handle_new_salary'), state=ChangeVacancy.new_salary)
    reg_changeVacancy_handlers()

    dp.register_message_handler(
        searchVacancy_handle_name, state=SearchVacancy.name)
