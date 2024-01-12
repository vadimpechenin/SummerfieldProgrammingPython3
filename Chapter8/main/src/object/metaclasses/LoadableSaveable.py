"""
Метаклас для проверки начилия методов load() и save() у группы классов, реализующих данные методы
Классы, играющие роль метаклассов, должны наследовать общий базовый класс type или один из его подклассов.
Проверки должны выполнять после создания класса (вызов функции super()), поскольку только после этого атрибуты класса будут доступны
Можно было бы проверить, являются ли атрибуты load и save вызываемыми, используя функцию hasattr() для проверки наличия атрибута __call__,
но вместо этого мы предпочли проверить, являются ли они экземплярами класса collections.Callable.
Абстрактный базовый класс collections.Callable обещает, но не гарантирует, что экземпляры его подклассов
(или виртуальных подклассов) смогут вызываться.

После создания класса (вызовом type.__new__() или переопределением метода __new__()) выполняется инициализация метакласса
вызовом метода __init__(). Методу __init__() передаются: в аргументе cls - только что созанный класс;
в аргументе classname - имя класса (доступно так же в виде атрибуты cls.__name__); в аргументе bases - список базовых классов
(кроме класса object, вследствие чего список может быть пустым); в аргументе dictionary - словарь с атрибутами, которые стали атрибутами
класса после создания класса cls при условии, что мы не вмешивались в переопределение метода __new__() метакласса.

>>>class Bad(metaclass=LoadableSaveable.LoadableSaveable):
...     def some_method(self): pass
Traceback (most recent call last):
...
AssertionError: class 'Bad' must provide a load() method

>>>class Good(metaclass=LoadableSaveable.LoadableSaveable):
...     def load(self): pass
...     def save(self): pass
>>>g = Good()
"""

import collections


class LoadableSaveable(type):

    def __init__(cls, classname, bases, dictionary):
        super().__init__(classname, bases, dictionary)
        assert hasattr(cls, "load") and isinstance(getattr(cls, "load"),
                                                   collections.Callable), ("class '" +
                                                                           classname + "' must provide a load() method")
        assert hasattr(cls, "save") and isinstance(getattr(cls, "save"),
                                                   collections.Callable), ("class '" +
                                                                           classname + "' must provide a save() method")

class Good(metaclass=LoadableSaveable):
    def load(self):
       pass
    def save(self):
       pass

