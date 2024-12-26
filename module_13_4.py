# импорт необходимых библиотек и методов
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

""" api ключ, который мы получили в «BotFather». Переменная бота,
    хранящая объект бота, «token» будет равен вписанному ключу"""
api = ""  # ввод вашего api полученный в @BotFather
bot = Bot(token=api)
""" Переменная dp объекта «Dispatcher», у него наш бот в
    качестве аргументов. В качестве «Storage» будет «MemoryStorage»"""
dp = Dispatcher(bot, storage=MemoryStorage())


# объявление класса состояния UserState наследованный от StatesGroup
class UserState(StatesGroup):
    # объявление объектов класса age, growth, weight
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес
    gender = State()  # пол


# обработчик ожидания сообщения от пользователя на слово Calories
@dp.message_handler(text=['Калории', 'к', 'К'])
# функция получения возраста пользователя
async def set_age(message):
    # ожидание сообщения Calories и вывод текста
    await message.answer('Введите свой возраст (Полных лет):')
    # ожидание ввода возраста
    await UserState.age.set()


# обработчик ожидания окончания статуса UserState.age
@dp.message_handler(state=UserState.age)
# функция получения роста пользователя
async def set_growth(message, state):
    # ожидание сохранение сообщения возраста от пользователя в базе данных состояния
    await state.update_data(age_=message.text)
    # ожидание вывода текста
    await message.answer('Введите свой рост (см):')
    # ожидание ввода роста
    await UserState.growth.set()


# обработчик ожидания окончания статуса UserState.growth
@dp.message_handler(state=UserState.growth)
# функция получения веса пользователя
async def set_weight(message, state):
    # ожидание сохранение сообщения роста от пользователя в базе данных состояния
    await state.update_data(growth_=message.text)
    # ожидание вывода текста
    await message.answer('Введите свой вес (кг):')
    # ожидание ввода веса
    await UserState.weight.set()


# обработчик ожидания окончания статуса UserState.weight
@dp.message_handler(state=UserState.weight)
# функция получения пола пользователя
async def set_gender(message, state):
    # ожидание сохранение сообщения веса от пользователя в базе данных состояния
    await state.update_data(weight_=message.text)
    # ожидание вывода текста
    await message.answer('Введите свой пол (м / ж):')
    # ожидание ввода пола
    await UserState.gender.set()


# обработчик ожидания окончания статуса UserState.man
@dp.message_handler(state=UserState.gender)
# функция расчета суточного рациона пользователя в калориях
async def set_calories(message, state):
    # ожидание сохранение сообщения пола от пользователя в базе данных состояния
    await state.update_data(gender_=message.text)
    # сохранение полученных данных в переменной data
    data = await state.get_data()
    # условие анализа пола пользователя
    if str(data['gender_']) == 'м' or 'М':
        # Расчет по формуле Миффлина-Сан Жеора для мужчин
        calories = int(data['weight_']) * 10 + int(data['growth_']) * 6.25 - int(data['age_']) * 5 + 5
        # ожидание вывода текста результатов расчета
        await message.answer(f'Ваша норма калорий {calories} в день')
    elif str(data['gender_']) == 'ж' or 'Ж':
        # Расчет по формуле Миффлина-Сан Жеора для женщин
        calories = int(data['weight_']) * 10 + int(data['growth_']) * 6.25 - int(data['age_']) * 5 - 161
        # ожидание вывода текста результатов расчета
        await message.answer(f'Ваша норма калорий {calories} к в день')
    else:
        await message.answer(f'Введены неверные данные, начните ввод с начала')
    # print(f'{data}, {calories}')  # Вывод данных в консоль
    # завершение работы машины состояния
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий вашему здоровью.\n'
                         'Введите слово "Калории" или "к", чтобы узнать вашу суточную норму'
                         ' потребления калорий')


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    # запуск бота (dp - аргумент через что стартовать)
    executor.start_polling(dp, skip_updates=True)
