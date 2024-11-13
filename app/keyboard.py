from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Предложение оставить отзыв после получения расписания с кнопкой "Заполнить анкету"
feedback_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Заполнить анкету')]],
                                        resize_keyboard=True)

answer1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Высокое')],
                                       [KeyboardButton(text='Среднее')],
                                       [KeyboardButton(text='Низкое')]],
                                        resize_keyboard=True)
answer2 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Удобным')],
                                       [KeyboardButton(text='Средним')],
                                       [KeyboardButton(text='Неудобным')]],
                                        resize_keyboard=True)
answer3 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отлично')],
                                       [KeyboardButton(text='Удовлетворительно')],
                                       [KeyboardButton(text='Плохо')]],
                                        resize_keyboard=True)

answer4 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Приветливая команда')],
                                       [KeyboardButton(text='Подача материала')],
                                       [KeyboardButton(text='Нестандартные задания')],
                                        [KeyboardButton(text='Все перечисленное')]],
                                        resize_keyboard=True)
