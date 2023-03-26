from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(KeyboardButton('Додати вакансію'), KeyboardButton('Видалити вакансію'))\
    .row(KeyboardButton('Повернутися назад'))

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Відміна'))