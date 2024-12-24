# импорт необходимых библиотек
import asyncio


# объявление асинхронной функции (корутины) start_strongman
async def start_strongman(name: str, power: int):
    ball = 5                                       # количество шаров
    print(f'Силач {name} начал соревнования.')     # вывод на консоль начала выступления силача
    for i in range(ball):                          # цикл выступления силача
        """ Оператор await внутри асинхронной функции приостанавливает
        выполнение одной операции до завершения другой асинхронной операции
        и задержка на выполнение операции (asyncio.sleep())"""
        await asyncio.sleep(1 / power)
        print(f'Силач {name} поднял {i + 1} шар')  # вывод на консоль выполненой операции
    print(f'Силач {name} закончил соревнования.')  # вывод на консоль окончания выступления силача


# объявление асинхронной функции (корутины) start_tournament
async def start_tournament():
    # задачи для параллельного выполнения
    task1 = asyncio.create_task(start_strongman('Pasha', 3))
    task2 = asyncio.create_task(start_strongman('Denis', 4))
    task3 = asyncio.create_task(start_strongman('Apollon', 5))
    """ Оператор await внутри асинхронной функции приостанавливает
        выполнение одной операции до завершения другой асинхронной операции"""
    await task1
    await task2
    await task3


# метод для запуска асинхронной функции start_tournament
asyncio.run(start_tournament())
