"""
Класс - менеджер контекста
При создании объекта AtomicList мы сохраняем ссылку на оригинальный список.
Флаг shallow_copy определяет, какое копирование будет применяться к списку - поверхностное или глубокое.
Поверхностное - для списков чисел или строк, но если содержатся другие списки или коллекции, поверхностного не достаточно.
Менеджер контекта используется в инструкции with, вызывается его метод __enter__(). В этот момент создается и возвращается копия списка,
чтобы все изменения выполнялись в копии.
"""
import copy


class AtomicList:

    def __init__(self, alist, shallow_copy=True):
        self.original = alist
        self.shallow_copy = shallow_copy

    def __enter__(self):
        self.modified = (self.original[:] if self.shallow_copy
                         else copy.deepcopy(self.original))
        return self.modified

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.original[:] = self.modified