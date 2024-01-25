"""
Использование asyncio для асинхронного выполнения кода
Позволяет превзойти глобальную блокировку интерпретатора, который работает в одном потоке в единицу времени
В результате выполнения
1
3
2
"""
import asyncio


#Ключевые слова async - говорит о том, что это асинхронные функции
async def print1():
    print(1)

async def print2():
    #Функция-заглушка
    await asyncio.sleep(1)
    print(2)

async def print3():
    print(3)

async def main():
    if ((option == 1)or(option == 2)):
        task1 = asyncio.create_task(print1())
        task2 = asyncio.create_task(print2())
        task3 = asyncio.create_task(print3())
        #await - аналог yield, может подождать если заснула и другие начнут работу
        if (option == 1):
            await task1
            await task2
            await task3
        #или более универсальный вариант
        elif (option == 2):
            await asyncio.gather(task1, task2, task3)
    #третий вариант, но не работает
    elif (option == 3):
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(print1())
                tg.create_task(print2())
                tg.create_task(print3())
        except:
            pass
#1. Запуск событийного цикла
option = 2
asyncio.run(main())