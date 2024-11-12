import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

bot = Bot(token='8118173051:AAFgVLf5hULwp8nWrrxi7KT4RJrw1-idZxM')
dp = Dispatcher()

class Form(StatesGroup):
    name = State()
    mail = State()
    course = State()

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
    await state.clear()  # Очищаем состояние


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
