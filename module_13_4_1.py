from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api =''
bot = Bot(token=api)
dp = Dispatcher(bot,storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()
@dp.message_handler(commands=['start'])
async def start_message(message):
     await message.answer('Привет! Я бот помогающий твоему здоровью.'
                          '\nВведите слово Calories, чтобы начать подсчёт.')

@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост в сантиметрах:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес в килограммах:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=int(message.text))
    await message.answer('Укажите свой пол М или Ж')
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def send_calories (message, state):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    if data["gender"] == 'Ж':
        calories = (10 * data['weight']) + (6.25 * data['growth']) - (5 * data['age']) - 161
    else:
        calories = (10 * data['weight']) + (6.25 * data['growth']) - (5 * data['age']) + 5

    await message.answer(f"Ваша норма калорий в день составляет- {calories}")
    await state.finish()
@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')
if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=True)


