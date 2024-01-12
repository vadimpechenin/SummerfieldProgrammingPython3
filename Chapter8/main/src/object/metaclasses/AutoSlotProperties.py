"""
Метакласс AutoSlotProperties, который модифицирует классы, использующие его исключительно посредством метода __new__().
Вместр использования декораторов @property и @name.setter мы создаем классы, применяющие простые соглашения об именах,
используемых для идентификации свойств. Например, если класс имеет методы get_name() и set_name(), в соответствии с соглашениями можно
было бы ожидать, что класс имеет частное свойтсво __name, доступное как instance.name.

При вызове метода __new__() метакласса передаются имена метакласса и класса, список базовых классов и словарь класса, который должен быть создан.
Поскольку перед созданием класса нам необходимо изменить словарь, следует переопределить не метод __init__(), а метод __new__().

Реализация метода начинается с копирования коллекции __slots__, с созданием пустой коллекции, если коллекция __slots__ отсутствовала.
Попутно кортеж преобразуется в список, чтобы впоследствии имелась возможность изменять его.
Из всех атрибутов, находящихся в словаре, мы выбираем те, что начинаются с префикса "get_" и являются вызываемыми, то есть те, которые представляют методы чтения.
Для каждого метода чтения в список slots добавляется частное имя атрибута, который будет хранить соответствующие данные, например,
при наличии метода get_name() в список slots добавляется имя __name.
После этого из словаря извлекается и удаляется ссылка на метод чтения по его оригинальному имени (обе эти операции выполняются за
один раз, с помощью вызова метода dict.pop()). То же самое выполняется для метода записи, если таковой присутствует, и затем создается
новый элемент словаря с соответствующим именем свойства в качестве ключа, например, для метода чтения с именем get_name() свойство
получит имя name. Значением элемента будет свойство с методами чтения и записи (который может отсутствовать), которые были найдены
и удалены из словаря.
В конце оригинальный кортеж __slots__ замещается модифицированным списком, в который были включены частные имена для каждого
добавленного свойства, и вызывается метод базового класса, чтобы создать действительный класс, но уже с использованием
модифицированного словаря. Обратите внимание, что в данном случае мы должны
явно передать метакласс методу базового класса – это необходимо делать всегда, когда вызывается метод __new__(), потому что это метод
класса, а не метод экземпляра.
В этом примере нам не потребовалось переопределять метод __init__(),
потому что все необходимое было реализовано в методе __new__(), однако вполне возможно переопределить оба метода: __new__() и __init__()
и в каждом из них выполнить свою часть работы.

>>> point = Point(-17, 9181)
>>> point.x, point.y        # returns: (0, 1024)
(0, 1024)
>>> point.x = -8
>>> point.y = 3918
>>> point.x, point.y        # returns: (0, 1024)
(0, 1024)
>>> point = Point(91, 181)
>>> point.x, point.y        # returns: (91, 181)
(91, 181)
>>> point.x *= 2
>>> point.y //= 3
>>> point.x, point.y        # returns: (182, 60)
(182, 60)

BE:
>>> product = Product("101110110", "8mm Stapler")
>>> product.barcode, product.description
('101110110', '8mm Stapler')
>>> product.barcode = "XXX"
Traceback (most recent call last):
...
AttributeError: can't set attribute

BF:
>>> product.description = "8mm Stapler (long)"
>>> product.barcode, product.description
('101110110', '8mm Stapler (long)')

>>> point = PointA(-17, 9181, -18)
>>> point.x, point.y        # returns: (0, 1024)
(0, 1024)
>>> point.x = -8
>>> point.y = 3918
>>> point.x, point.y        # returns: (0, 1024)
(0, 1024)
>>> point.a
-18
>>> point.a = 7
>>> point.a
7
>>> point = Point(91, 181)
>>> point.x, point.y        # returns: (91, 181)
(91, 181)
>>> point.x *= 2
>>> point.y //= 3
>>> point.x, point.y        # returns: (182, 60)
(182, 60)

"""

import collections


class AutoSlotProperties(type):

    def __new__(mcl, classname, bases, dictionary):
        slots = list(dictionary.get("__slots__", []))
        for getter_name in [key for key in dictionary
                            if key.startswith("get_")]:
            if isinstance(dictionary[getter_name],
                          collections.Callable):
                name = getter_name[4:]
                slots.append("__" + name)
                getter = dictionary.pop(getter_name)
                setter_name = "set_" + name
                setter = dictionary.get(setter_name, None)
                if (setter is not None and
                    isinstance(setter, collections.Callable)):
                    del dictionary[setter_name]
                dictionary[name] = property(getter, setter)
        dictionary["__slots__"] = tuple(slots)
        return super().__new__(mcl, classname, bases, dictionary)


class Product(metaclass=AutoSlotProperties):

    def __init__(self, barcode, description):
        self.__barcode = barcode
        self.description = description


    def get_barcode(self):
        return self.__barcode


    def get_description(self):
        return self.__description


    def set_description(self, description):
        if description is None or len(description) < 3:
            self.__description = "<Invalid Description>"
        else:
            self.__description = description



class Point(metaclass=AutoSlotProperties):

    def __init__(self, x, y):
        self.x = x
        self.y = y


    def get_x(self):
        return self.__x


    def set_x(self, value):
        self.__x = min(max(0, value), 1024)


    def get_y(self):
        return self.__y


    def set_y(self, value):
        self.__y = min(max(0, value), 1024)



class PointA(metaclass=AutoSlotProperties):

    __slots__ = ("a",)

    def __init__(self, x, y, a):
        self.x = x
        self.y = y
        self.a = a


    def get_x(self):
        return self.__x


    def set_x(self, value):
        self.__x = min(max(0, value), 1024)


    def get_y(self):
        return self.__y


    def set_y(self, value):
        self.__y = min(max(0, value), 1024)



if __name__ == "__main__":
    import doctest
    doctest.testmod()