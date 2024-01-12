"""
A simplified version of the built-in property class to show a possible
implementation and illustrate how descriptors work.

>>> contact = NameAndExtension("Joe", 135)
>>> contact.name, contact.extension
('Joe', 135)
>>> contact.X
Traceback (most recent call last):
    ...
AttributeError: 'NameAndExtension' object has no attribute 'X'
>>> contact.name = "Jane"
Traceback (most recent call last):
    ...
AttributeError: 'name' is read-only
>>> contact.name
'Joe'
>>> contact.extension = 975
>>> contact.extension
975

"""
import inspect


class Property:

    def __init__(self, getter, setter=None, deleter=None):
        self.__getter = getter
        self.__setter = setter
        self.__deleter = deleter
        self.__name__ = getter.__name__

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return self.__getter(instance)

    def __set__(self, instance, value):
        if self.__setter is None:
            raise AttributeError("'{0}' is read-only".format(
                self.__name__))
        return self.__setter(instance, value)

    def setter(self, setter):
        self.__setter = setter
        return self

    def deleter(self, deleter):  # 这个是在下面 @extension.deleter  会调用的
        self.__deleter = deleter
        return self

    def __delete__(self, instance):  # 这个函数时描述符的接口要求的
        if self.__deleter is None:
            raise AttributeError("'{0}' is not allowed delete".format(
                self.__name__))
        return self.__deleter(instance)


class NameAndExtension:

    def __init__(self, name, extension):
        self.__name = name
        self.__extension = extension  # self.extension = extension，Реализация del оказывается фатально рекурсивной

    @Property  # Uses the custom Property descriptor
    def name(self):
        return self.__name

    @Property  # Uses the custom Property descriptor
    def extension(self):
        return self.__extension

    @extension.setter  # Uses the custom Property descriptor
    def extension(self, extension):
        self.__extension = extension

    @extension.deleter  # Uses the custom Property descriptor
    def extension(self):
        print('{0} calledBy {1}'.format(inspect.stack()[0][3], inspect.stack()[1][3]))
        del self.__extension  # Ловушка: оно должно отличаться от внешнего имени, иначе будет бесконечный цикл.


if __name__ == "__main__":
    import doctest

    doctest.testmod()