"""
Частично подготовленные функции - создание функций из существующих и некоторых аргументов
"""

import functools
import pathlib


def main():
    enumerate1 = functools.partial(enumerate, start=1)

    lines=['foo', 'baz', 'bar']
    for i, line in enumerate1(lines):
        print(f'{i} {line}')

    #Работа с файлами
    reader = functools.partial(open, mode="rt", encoding="utf8")
    writer = functools.partial(open, mode="wt", encoding="utf8")
    path = pathlib.Path(pathlib.Path(__file__).parent.parent.parent.parent.resolve()).\
        joinpath("data").joinpath("fileForReadWrite.txt").resolve()
    f = reader(path)
    for line in f:
        print(line)
    f.close()
    f = writer(path)
    f.write('Это единственная строка в файле\n')
    f.close()

if __name__ == '__main__':
   main()