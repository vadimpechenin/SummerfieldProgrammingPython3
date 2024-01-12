"""
Менедржеры контекста.
Позволяют упростить программный код, гарантируя выполнение определенных операций до и после выполнения некоторого блока кода.
Определяют два основных метода
__enter__() - вызывается автоматически при создании менеджера контекста with
__exit__() - вызывается, когда поток выполнения покидает область видимости менеджера контекста
интерпретируются особым образом в области видимости инструкции with
"""
import contextlib
import pathlib

def process(line):
    res = ''
    for i in range(len(line) - 1, -1, -1):
        res += line[i]
    return res

def main():
    filename = pathlib.Path(pathlib.Path(__file__).parent.parent.parent.parent.resolve()).joinpath("data").joinpath("file1.txt")
    #1. Реализация чтения файла без менеджера контекста
    fh = None
    try:
        fh = open(filename)
        for line in fh:
            process(line)
    except EnvironmentError as err:
        print(err)
    finally:
        if fh is not None:
            fh.close()

    #2. Реализация чтения файла с менеджером контекста
    try:
        with open(filename) as fh:
            for line in fh:
                process(line)
    except EnvironmentError as err:
        print(err)

    #3. Использование двух или более менеджеров контекта пример 1
    source = pathlib.Path(pathlib.Path(__file__).parent.parent.parent.parent.resolve()).joinpath("data").joinpath(
        "file1.txt")
    target = pathlib.Path(pathlib.Path(__file__).parent.parent.parent.parent.resolve()).joinpath("data").joinpath(
        "file1_.txt")
    try:
        with open(source) as fin:
            with open(target, "w") as fout:
                for line in fin:
                    fout.write(process(line))
    except EnvironmentError as err:
        print(err)


if __name__ == '__main__':
    main()