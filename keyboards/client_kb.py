from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

client_kb = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(KeyboardButton('Панель адміна'))\
    .row(KeyboardButton('Графік роботи'), KeyboardButton('Меню'))