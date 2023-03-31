from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

client_kb = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(KeyboardButton('Панель адміна'))\
    .row(KeyboardButton('Інше'))\
    .row(KeyboardButton('Графік роботи'), KeyboardButton('Меню'))


def get_inline_kb(vacancy1: tuple, vacancy2: tuple, vacancy3: tuple, vacancy4: tuple, vacancy5: tuple):
    inline_kb = InlineKeyboardMarkup() \
        .row(InlineKeyboardButton(text=f"Назва вакансії: {vacancy1[2]}<br>ЗП: {vacancy1[4]}", callback_data="vacancy1")) \
        .row(InlineKeyboardButton(text=f"Назва вакансії: {vacancy2[2]}<br>ЗП: {vacancy2[4]}", callback_data="vacancy2")) \
        .row(InlineKeyboardButton(text=f"Назва вакансії: {vacancy3[2]}<br>ЗП: {vacancy3[4]}", callback_data="vacancy3")) \
        .row(InlineKeyboardButton(text=f"Назва вакансії: {vacancy4[2]}<br>ЗП: {vacancy4[4]}", callback_data="vacancy4")) \
        .row(InlineKeyboardButton(text=f"Назва вакансії: {vacancy5[2]}<br>ЗП: {vacancy5[4]}", callback_data="vacancy5")) \
        .row(InlineKeyboardButton(text="◀️", callback_data="back"),
             InlineKeyboardButton(text="1/5", callback_data="page"),
             InlineKeyboardButton(text="▶️", callback_data="next"))
    return inline_kb