"""
Пример использования асинхронности без специальных модулей
запуск 2 функций: перечисление файловой системы; вывод каждые 5 с. сообщения о том, что они прошли.
Созданы два объекта-генератора, которые запускаются в бесконечном цикле
"""
import os
import time


def clock():
    time0 = round(time.time())
    while True:
        if (round(time.time()) - time0) % 5 == 0:
            yield '5 sec'
        else:
            yield 0

def query():
    for i in os.walk('C:\\'):
        yield i[0]


def main():
    data = query()
    alarm = clock()
    while True:
        d = next(data)
        a = next(alarm)
        while True:
            d = next(data)
            a = next(alarm)
            print(d)
            if a: print(a)
            time.sleep(1)

main()
