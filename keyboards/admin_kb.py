from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(KeyboardButton('Додати вакансію'), KeyboardButton('Змінити вакансію'))\
    .row(KeyboardButton('Повернутися назад'), KeyboardButton('Видалити вакансію'))

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Відміна'))