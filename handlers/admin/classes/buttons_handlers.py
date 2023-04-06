from aiogram import types
from aiogram.dispatcher import FSMContext

from database import db
from keyboards import client_kb, cancel_button


class ButtonsHandlers:
    async def add(self, message: types.Message):
        await AddVacancy.name.set()
        await message.answer('Пишіть назву вакансії', reply_markup=cancel_button)

    async def change(self, message: types.Message):
        await message.answer('Ще в розробці', reply_markup=client_kb)
        await ChangeVacancy.id.set()
        # await ChangeVacancy.condition.set()
        await message.answer('Введіть id вакансії яку треба змінити', reply_markup=cancel_button)

    async def delete(self, message: types.Message):
        # await message.answer('Ще в розробці', reply_markup=client_kb)
        await DeleteVacancy.id.set()
        # await DeleteVacancy.condition.set()
        await message.answer('Введіть id вакансії яку треба видалити', reply_markup=cancel_button)

    async def show(self, message: types.Message):
        # await db.sql_read_admin(message=message)
        for vacancy in await db.db_obj.select_data(message, 'vacancies', '*'):
            await message.answer(f'ID: {vacancy[0]}\nСтатус: {vacancy[1]}\nНазва вакансії: {vacancy[2]}\nОпис: {vacancy[3]}\nЗП: {vacancy[4]}')

    async def cancel(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        print(f'current_state: {current_state}')
        if current_state is None:
            # print(f'current_state: IS NONE!!!')
            return
        await state.finish()
        await message.answer('Операція була скасована', reply_markup=client_kb)

    async def search(self, message: types.Message):
        await message.answer('Ще в розробці', reply_markup=client_kb)
        await SearchVacancy.name.set()
        await message.answer('Введіть назву вакансії яку треба знайти', reply_markup=cancel_button)
