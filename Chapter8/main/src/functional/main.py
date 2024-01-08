import functools
import operator
import os
import pathlib


def main():
    path = pathlib.Path(pathlib.Path(__file__).parent.parent.parent.resolve()).joinpath("data")
    files = []
    for item in range(3):
        files.append(str(pathlib.Path(path).joinpath("file" + str(item+1) + ".txt")))

    #Поиск общей суммы файлов
    print(functools.reduce(operator.add, (os.path.getsize(x) for x in files)))
    print(functools.reduce(operator.add, map(os.path.getsize, files)))
    print(functools.reduce(operator.add, map(os.path.getsize,
                                             filter(lambda x: x.endswith(".txt"), files))))
    print(functools.reduce(operator.add, map(os.path.getsize,
                                             (x for x in files if x.endswith(".txt")))))
    print(functools.reduce(operator.add, (os.path.getsize(x)
                                             for x in files if x.endswith(".txt"))))

    print(sum(os.path.getsize(x) for x in files if x.endswith(".txt")))


if __name__ == '__main__':
   main()