import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

import app.keyboard as kb

bot = Bot(token='8118173051:AAFgVLf5hULwp8nWrrxi7KT4RJrw1-idZxM')
dp = Dispatcher()

class Form(StatesGroup):
    name = State()
    mail = State()
    course = State()
    contract_review = State()  # Новое состояние для просмотра договора
    feedback = State()  # Состояние для сбора обратной связи
    feedback_question_1 = State()  # Состояние для первого вопроса анкеты
    feedback_question_2 = State()  # Состояние для второго вопроса анкеты
    feedback_question_3 = State()
    feedback_question_4 = State()

# Словарь для хранения зарегистрированных студентов и их курсов
registered_students = {}

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать! Я виртуальный ассистент онлайн-школы LearnSphere. '
                         'Чтобы подать заявку на обучение введите /apply')

@dp.message(Command('apply'))
async def cmd_apply(message: Message, state: FSMContext):
    await message.answer('Итак, начнём!')
    await state.set_state(Form.name) #Состояние для имени
    await message.answer('Введите Ваше имя')

@dp.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text) #Сохраняем имя в состоянии
    await state.set_state(Form.mail)  # Состояние для почты
    await message.answer('Введите Вашу электронную почту')

@dp.message(Form.mail)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(mail=message.text) #Сохраняем почту в состоянии
    await state.set_state(Form.course)  # Состояние для курса
    await message.answer('Введите название курса, который вы хотели бы изучать')

@dp.message(Form.course)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(course=message.text) #Сохраняем название курса в состоянии
    data = await state.get_data()
    # Формируем ответ с собранной информацией
    await message.answer(f"Спасибо за вашу заявку!\n\n"
                         f"Имя: {data['name']}\n"
                         f"Почта: {data['mail']}\n"
                         f"Курс: {data['course']}\n\n"
                         "Ваша заявка успешно подана!")
    #await state.clear()  # Очищаем состояние

    # Сохраняем информацию о зарегистрированном студенте
    registered_students[message.from_user.id] = {
        'name': data['name'],
        'mail': data['mail'],
        'course': data['course'],
        'chat_id': message.from_user.id,
        'start_date': datetime.now() + timedelta(weeks=1),  # Курс начинается через неделю
        'contract_signed': False,  # Статус подписания договора
        'feedback_submitted': False  # Статус заполнения обратной связи
    }

    await state.set_state(Form.contract_review) # Устанавливаем состояние для просмотра договора
    contract_text = "Вот проект вашего договора:\n\n" \
                    "1. Образовательные услуги предоставляются на основании данной заявки.\n" \
                    "2. Стоимость обучения составляет X рублей.\n" \
                    "3. Договор вступает в силу после подписания.\n\n" \
                    "Пожалуйста, подтвердите согласие с условиями договора (да/нет)."

    await message.answer(contract_text)

@dp.message(Form.contract_review)
async def process_contract_review(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        data = await state.get_data()

        # Обновляем статус подписания договора в словаре студентов
        registered_students[message.from_user.id]['contract_signed'] = True

        await message.answer("Спасибо! Ваше согласие зафиксировано.")
        # Здесь можно добавить логику для уведомления менеджера (например, отправка сообщения)
        manager_message = (f"Студент {data['name']} согласился с условиями договора.\n"
                           f"Почта: {data['mail']}\n"
                           f"Курс: {data['course']}")
        await bot.send_message(chat_id='6300119200', text=manager_message)  # Замените на ID Вашего менеджера

        # Рассылка расписания занятий сразу после подписания договора
        start_date = registered_students[message.from_user.id]['start_date']
        schedule_message = (f"Курс {data['course']} начинается {start_date.strftime('%d.%m.%Y')}.\n"
                            "Расписание занятий:\n"
                            "1. Занятие 1 - дата и время\n"
                            "2. Занятие 2 - дата и время\n"
                            "3. Занятие 3 - дата и время")

        await bot.send_message(chat_id=message.from_user.id, text=schedule_message)

        await message.answer("Прошли наши курсы? Поделитесь мнением!", reply_markup=kb.feedback_keyboard)


    elif message.text.lower() == 'нет':
        data = await state.get_data()
        manager_message = (f"Студент {data['name']} отклонил условия договора.\n"
                           f"Контакт: {data['mail']}\n"
                           f"Курс: {data['course']}")
        await bot.send_message(chat_id='6300119200', text=manager_message)
        # Укажите ссылку на менеджера (например, на его Telegram-аккаунт)
        manager_contact_link = "[Связаться с менеджером](https://t.me/kinoe141)"
        await message.answer(
            "Вы отклонили условия договора. Если у вас есть вопросы, пожалуйста, свяжитесь с менеджером по телефону +7 (123) 456-78-90.\n"
            f"{manager_contact_link}", parse_mode='Markdown')  # Используйте Markdown для активной ссылки

    else:
        await message.answer("Пожалуйста, ответьте 'да' или 'нет'.")

    await state.clear()  # Завершаем состояние

@dp.message(F.text == 'Заполнить анкету')
async def question(message: Message, state:FSMContext):
#await message.answer('Ознакомьтесь с вопросами анкеты', reply_markup=kb.question)
    await state.set_state(Form.feedback_question_1)  # Устанавливаем состояние для первого вопроса анкеты
    await message.answer('1. Как вы оцениваете качество материалов курса?', reply_markup=kb.answer1)

@dp.message(Form.feedback_question_1)
async def feedback_question_1(message: Message, state: FSMContext):
    # Переход к следующему вопросу
    await state.set_state(Form.feedback_question_2)
    await message.answer('2. Насколько удобным было взаимодействие с преподавателями?', reply_markup=kb.answer2)

@dp.message(Form.feedback_question_2)
async def feedback_question_2(message: Message, state: FSMContext):
    await state.set_state(Form.feedback_question_3)
    await message.answer('3. Как вы оцениваете свою успеваемость в курсе?', reply_markup=kb.answer3)

@dp.message(Form.feedback_question_3)
async def feedback_question_3(message: Message, state: FSMContext):
    await state.set_state(Form.feedback_question_4)
    await message.answer('4. Что вам понравилось больше всего в обучении?', reply_markup=kb.answer4)

@dp.message(Form.feedback_question_4)
async def feedback_question_4(message: Message, state: FSMContext):
    # Здесь можно сохранить ответ на последний вопрос если нужно

    # Финальное сообщение после всех вопросов анкеты
    await message.answer("Спасибо за Ваше мнение! Будем ждать вас снова в онлайн-школе Learn Sphere!")
    registered_students[message.from_user.id]['feedback_submitted'] = True
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')