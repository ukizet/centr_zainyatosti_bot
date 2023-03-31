import sqlite3 as sq
from create_bot import bot

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import client_kb


class Database:
    def __init__(self, db_name: str):
        """
        :db_name: назва бази даних з крапкою, як тут 'database.db'
        """
        self.conn = sq.connect(f'database/{db_name}')
        self.cursor = self.conn.cursor()
        if self.conn:
            print('Database connected(class Database)')

    def create_table(self, table_name: str, columns: str):
        """
        :param table_name: назва таблиці
        :param columns: назви стовпців приблизно такого формату: 'ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, status TEXT DEFAULT "active", name TEXT, desc TEXT, salary REAL'
        """

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f'Помилка при створенні таблиці: {e}')

    async def insert_data(self, message: types.Message, table_name: str, columns: str, data: str):
        """
        :param table_name: назва таблиці
        :param columns: назви стовпців приблизно такого формату: 'name, desc, salary'
        :param data: данні які треба вставити приблизно такого формату: '"Вакансія 1", "Опис вакансії 1", 1000'
        """

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({data})"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f'Помилка при вставці даних: {e}')
            await message.answer(f'Помилка при вставці даних: {e}', reply_markup=client_kb)

    async def select_data(self, message: types.Message, table_name: str, columns: str = None, condition: str=None):
        """
        Цей метод повертає список кортежів, де кожен кортеж це рядок з таблиці

        :param table_name: назва таблиці
        :param columns: назви стовпців приблизно такого формату: 'name, desc, salary'
        :param condition: умова вибору даних приблизно такого формату: 'salary > 1000'
        """

        if columns is None:
            columns = '*'
        query = f"SELECT {columns} FROM {table_name}"
        if condition is not None:
            query += f" WHERE {condition}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f'Помилка при виборці даних: {e}')
            await message.answer(f'Помилка при виборці даних: {e}', reply_markup=client_kb)

    async def update_data(self, message: types.Message, table_name: str, set_values: str, condition: str=None):
        """
        :param table_name: назва таблиці
        :param set_values: данні які треба вставити приблизно такого формату: 'name = "Вакансія 1", desc = "Опис вакансії 1", salary = 1000'
        :param condition: умова вибору даних приблизно такого формату: 'salary > 1000'
        """

        query = f"UPDATE {table_name} SET {set_values}"
        if condition is not None:
            query += f" WHERE {condition}"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f'Помилка при оновленні даних: {e}')
            await message.answer(f'Помилка при оновленні даних: {e}', reply_markup=client_kb)

    async def delete_data(self, message: types.Message, table_name: str, condition: str = None):
        """
        :param table_name: назва таблиці
        :param condition: умова вибору даних приблизно такого формату: 'salary > 1000' або 'id = 1'
        """

        query = f"DELETE FROM {table_name}"
        if condition is not None:
            query += f" WHERE {condition}"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f'Помилка при видаленні даних: {e}')
            await message.answer(f'Помилка при видаленні даних: {e}', reply_markup=client_kb)

    def close_connection(self):
        self.conn.close()


def sql_start():
    print('db.py started')
    global db_obj
    # conn = sq.connect('database/vacancies.db')
    # cur = conn.cursor()
    # if conn:
    #     print('Database connected')
    # conn.execute('''CREATE TABLE IF NOT EXISTS vacancies(
    #                 ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    #                 status TEXT DEFAULT "active", 
    #                 name TEXT, 
    #                 desc TEXT, 
    #                 salary REAL
    #                 )''')
    # conn.commit()
    db_obj = Database('vacancies.db')
    db_obj.create_table('vacancies',
                        '''ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                        status TEXT DEFAULT "active", 
                        name TEXT, 
                        desc TEXT, 
                        salary REAL''')


# async def sql_add(state: FSMContext):
#     async with state.proxy() as data:
#         cur.execute('INSERT INTO vacancies (name, desc, salary) VALUES (?, ?, ?)', tuple(
#             data.values()))
#         conn.commit()


# async def sql_read(message: types.Message):
#     for ret in cur.execute('SELECT * FROM vacancies').fetchall():
#         # await bot.send_photo(message.from_user.id, ret[0], f'Назва: {ret[1]}\nОпис: {ret[2]}\nЦіна: {ret[3]}')
#         await message.answer(f'Назва вакансії: {ret[2]}\nОпис: {ret[3]}\nЗП: {ret[4]}')


# async def sql_read_admin(message: types.Message):
#     for vacancy in cur.execute('SELECT * FROM vacancies').fetchall():
#         await message.answer(f'ID: {vacancy[0]}\nСтатус: {vacancy[1]}\nНазва вакансії: {vacancy[2]}\nОпис: {vacancy[3]}\nЗП: {vacancy[4]}')


# async def sql_delete(message: types.Message):
#     try:
#         cur.execute('DELETE FROM vacancies WHERE ID = ?', (message.text,))
#         conn.commit()
#     except Exception as e:
#         await message.answer(f'Помилка при оновленні запису: {e}')


# async def sql_change(message: types.Message, state: FSMContext):
#     try:
#         async with state.proxy() as data:
#             cur.execute(
#                 f"UPDATE vacancies SET name = '{data['name']}' WHERE id = {data['id']}")
#             conn.commit()
#     except Exception as e:
#         await message.answer(f'Помилка при оновленні запису: {e}')

#     async with state.proxy() as data:
#         try:
#             cur.execute(
#                 f"UPDATE vacancies SET name = '{data['name']}' WHERE id = {data['id']}")
#             conn.commit()
#             await message.answer('Запис успішно оновлено')
#         except Exception as e:
#             await message.answer(f'Помилка при оновленні запису: {e}')


