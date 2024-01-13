"""
Более боевой пример использования метаклассов
аналог кода обычным методом:


class Women:
    class_dictionary = {'title': 'заголовок', 'content': 'контент', 'photo': 'путь к фото'}
    title = 'заголовок'
    content = 'контент'
    photo = 'путь к фото'
    def __init__(self, *args, **kwargs):
        for key, value in self.class_dictionary.items():
            self.__dict__[key] = value
"""

class Meta(type):
    def create_local_dictionary(self, *args, **kwargs):
        for key, value in self.class_dictionary.items():
            self.__dict__[key] = value

    def __init__(cls, classname, bases, dictionary):
        cls.class_dictionary = dictionary
        cls.__init__ = Meta.create_local_dictionary


class Women(metaclass=Meta):
    title = 'заголовок'
    content = 'контент'
    photo = 'путь к фото'