from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


button_1 = KeyboardButton(text='⬆ Больше')
button_2 = KeyboardButton(text='Меньше ⬇')
button_3 = KeyboardButton(text='Хочу играть')
button_3_1 = KeyboardButton(text='Играть ещё')
button_4 = KeyboardButton(text='🎉 Угадал 🎉')
button_5 = KeyboardButton(text='Нет')

keyboard_1 = ReplyKeyboardMarkup(keyboard=[[button_3]], resize_keyboard=True)
keyboard_1_1 = ReplyKeyboardMarkup(
    keyboard=[[button_3_1]], resize_keyboard=True)
keyboard_2 = ReplyKeyboardMarkup(
    keyboard=[[button_1, button_2], [button_4]], resize_keyboard=True)
keyboard_3 = ReplyKeyboardMarkup(
    keyboard=[[button_4], [button_5]], resize_keyboard=True)
