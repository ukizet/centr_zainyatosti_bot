import sqlite3 as sq
from create_bot import bot
from aiogram import types
from aiogram.dispatcher import FSMContext

def sql_start():
    global base, cur 
    base = sq.connect('database/vacancies.db')
    cur = base.cursor()
    if base: print('Database connected')
    base.execute('CREATE TABLE IF NOT EXISTS vacancies(id INTEGER PRIMARY KEY, name TEXT, desc TEXT, salary REAL)')
    base.commit()

async def sql_add(state: FSMContext):
    async with state.proxy() as data:
        cur.execute('INSERT INTO vacancies VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(message: types.Message):
    for ret in cur.execute('SELECT * FROM vacancies').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'Назва: {ret[1]}\nОпис: {ret[2]}\nЦіна: {ret[3]}')
        