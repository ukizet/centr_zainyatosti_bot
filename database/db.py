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
        await message.answer(f'Назва вакансії: {ret[1]}\nОпис: {ret[2]}\nЗП: {ret[3]}')
        