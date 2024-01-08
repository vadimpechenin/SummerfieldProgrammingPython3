"""
Декораторы и аннотации функций и методов
"""
import functools
from structural.decorators.logging_ import logged
import unicodedata
from structural.decorators.strictly_typed import strictly_typed

def positive_result(function):
    # Простой, стандартный декоратор
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result >= 0, function.__name__ + "() result isn't >=0"
        return result

    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    return wrapper


def positive_result_another(function):
    # Более простая запись декоратора
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result >= 0, function.__name__ + "() result isn't >=0"
        return result

    return wrapper


@positive_result
def discriminant(a, b, c):
    return (b ** 2) - (4 * a * c)


def bounded(minimum, maximum):
    # Вложенный декоратор, гарантирующий, что значение функции находится в заданном диапазоне
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if result < minimum:
                result = minimum
            if result > maximum:
                result = maximum
            return result

        return wrapper

    return decorator


@bounded(0, 100)
def percent(amount, total):
    return (amount / total) * 100


@logged
def discounted_price(price, percentage, make_integer=False):
    result = price * ((100 - percentage) / 100)
    if not (0 < result <= price):
        raise ValueError("invalid price")
    return result if not make_integer else int(round(result))


@strictly_typed
def is_unicode_punctuation(s : str) -> bool:
    #Проверяет, содержит ли строка знаки пунктуации (категории, имена которых начинаются с символа P - знаки пунктуации)
    for c in s:
        if unicodedata.category(c)[0] != "P":
            return False
    return True

def main():
    # Факториал
    a = 1
    b = 4
    c = 3
    result = discriminant(a, b, c)
    print("Дискриминант {0}, {1}, {2}: ".format(a, b, c) + str(result))
    amount = 200
    total = 150
    result = percent(amount, total)
    print("Процент {0} от {1}: ".format(amount, total) + str(result))

    print(type(discounted_price))
    res = discounted_price(100, 10)
    print(discounted_price(210, 5))
    print(discounted_price(210, 5, make_integer=True))
    print(discounted_price(210, 14, True))
    #print(discounted_price(210, -8))

    print(is_unicode_punctuation("zebr\a"))
    print(is_unicode_punctuation(s="!@#?"))
    print(is_unicode_punctuation(("!", "@")))

if __name__ == '__main__':
    main()
