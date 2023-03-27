import sqlite3 as sq
from create_bot import bot
from aiogram import types
from aiogram.dispatcher import FSMContext

def sql_start():
    global conn, cur 
    conn = sq.connect('database/vacancies.db')
    cur = conn.cursor()
    if conn: print('Database connected')
    conn.execute('''CREATE TABLE IF NOT EXISTS vacancies(
                    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                    status TEXT DEFAULT "active", 
                    name TEXT, 
                    desc TEXT, 
                    salary REAL
                    )''')
    conn.commit()

async def sql_add(state: FSMContext):
    async with state.proxy() as data:
        cur.execute('INSERT INTO vacancies (name, desc, salary) VALUES (?, ?, ?)', tuple(data.values()))
        conn.commit()

async def sql_read(message: types.Message):
    for ret in cur.execute('SELECT * FROM vacancies').fetchall():
        # await bot.send_photo(message.from_user.id, ret[0], f'Назва: {ret[1]}\nОпис: {ret[2]}\nЦіна: {ret[3]}')
        await message.answer(f'Назва вакансії: {ret[2]}\nОпис: {ret[3]}\nЗП: {ret[4]}')

async def sql_read_admin(message: types.Message):
    for vacancy in cur.execute('SELECT * FROM vacancies').fetchall():
        await message.answer(f'ID: {vacancy[0]}\nСтатус: {vacancy[1]}\nНазва вакансії: {vacancy[2]}\nОпис: {vacancy[3]}\nЗП: {vacancy[4]}')

async def sql_delete(message: types.Message):
    cur.execute('DELETE FROM vacancies WHERE ID = ?', (message.text,))
    conn.commit()
        