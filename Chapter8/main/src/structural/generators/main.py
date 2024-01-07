import sys


def items_in_key_order_yield(d):
    #Генератор для возспроизведения списка элементов "ключ-значение"
    for key in sorted(d):
        yield key, d[key]

def items_in_key_order(d):
    # Вторая версия генератора для возспроизведения списка элементов "ключ-значение"
    return ((key, d[key]) for key in sorted(d))

def quarters(next_quarter=0.0):
    #Бесконечный генератор
    #Воспроизводит последовательность с текущего значения
    while True:
        received = (yield next_quarter)
        if received is None:
            next_quarter += 0.25
        else:
            next_quarter = received

def five_quarters():
    result = []
    generator = quarters()
    while len(result)<5:
        x = next(generator)
        if abs(x-0.5) < sys.float_info.epsilon:
            x = generator.send(1.0) #переданное значение принято функцией-генератором в качестве результата выражения yield
        result.append(x)
    return result

def main():
    #1. Печать квадратов
    result = five_quarters()
    print(result)
    #2. Возврат отсортированного словаря
    test_dict = {1: "1", 3: "3", 2: "2", 4: "4", 6: "6"}
    generator1 = items_in_key_order_yield(test_dict)
    generator2 = items_in_key_order(test_dict)
    for x, y in zip(generator1, generator2):
        print("1: "+ str(x) + "; 2: " + str(y))


if __name__ == '__main__':
   main()