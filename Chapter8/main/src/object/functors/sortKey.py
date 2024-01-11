"""
Универсальный класс функтора SortKey.
Когда создается объект SortKey, он сохраняет кортеж с именами атрибутов, с которыми он был инициализирован.
Когда производится вызов объекта, создается список значений атрибутов для заданного экземпляра,
следующих в том же порядке, в каком они были указаны при инициализации объекта SortKey.
Класс Person для тестирования SortKey
Список people объектов Person, который можно отсортировать по фамилиям людей следующим способом:
people.sort(key=SortKey("surname")).
Если есть одинаковые фамилии, то сначала по фамилиям, потом по именам
people.sort(key=SortKey("surname", "forename")).
аналог реализации - использованием функции operator.attrgetter() из модуля operator, например
people.sort(key=operator.attrgetter("surname"))
"""


class SortKey:

    def __init__(self, *attribute_names):
        self.attribute_names = attribute_names

    def __call__(self, instance):
        values = []
        for attribute_name in self.attribute_names:
            values.append(getattr(instance, attribute_name))
        return values

class Person:

    def __init__(self, forename, surname, email):
        self.forename = forename
        self.surname = surname
        self.email = email