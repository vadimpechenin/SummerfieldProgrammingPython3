"""
Основы метаклассов, самые азы
Все булевы значения, списки, словари, строки - это объекты, образованные от соответствующих классов типов данных.
но эти классы так же являются и объектами, а то что их создают метаклассы. Метаклассы это тоже объекты, но которые нельзя
 породить каким-нибудь другим мета мета классом

type(classname, bases, dictionary) - в нем название создаваемого класса, базовые классы, словарь атрибутов и методов

Сначала с использованием type формируем
class Point(B1, B2):
...MAX_COORD = 100
...MIN_COORD = 0
...def method1(self):
    print(self.__dict__)
"""


class B1:
    pass

class B2:
    pass

def method1(self):
    print(self.__dict__)

def main():
    #1. Базовая основа. Использование type напрямую
    A = type('Point', (B1, B2), {'MAX_COORD': 100, 'MIN_COORD': 0, 'method1': method1})
    print(A.__mro__)

    pt = A()
    print(pt.method1())

#2. Создание метакласса-функции
def create_class_point(classname, bases, dictionary):
    dictionary.update({'MAX_COORD': 100, 'MIN_COORD': 0, 'method1': method1})
    return type(classname, bases, dictionary)

class Point(metaclass=create_class_point):
    def get_coords(self):
        return (0, 0)

#3. Создание полноценного метакласса в виде отдельного класса
#Добавляется cls - ссылка на созданный класс
class Meta(type):
    def __init__(cls, classname, bases, dictionary):
        super().__init__(classname, bases, dictionary)
        cls.MAX_COORD = 100
        cls.MIN_COORD = 0

class PointM(metaclass=Meta):
    def get_coords(self):
        return (0, 0)

#4. Создание полноценного метакласса в виде отдельного класса
#Используется метод __new__ - метод, перед созданием самого класса
class Meta2(type):
    def __new__(cls, classname, bases, dictionary):
        dictionary.update({'MAX_COORD': 100, 'MIN_COORD': 0, 'method1': method1})
        return type.__new__(cls, classname, bases, dictionary)

class Point2M(metaclass=Meta2):
    def get_coords(self):
        return (0, 0)

main()


