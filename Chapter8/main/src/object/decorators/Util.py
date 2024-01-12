def delegate(attribute_name, method_names):
    """Passes the call to the attribute called attribute_name for
    every method listed in method_names.
    (See SortedListP.py for an example.)
    """
    def decorator(cls):
        nonlocal attribute_name
        if attribute_name.startswith("__"):
            attribute_name = "_" + cls.__name__ + attribute_name
        for name in method_names:
            setattr(cls, name, eval("lambda self, *a, **kw: "
                                    "self.{0}.{1}(*a, **kw)".format(
                                    attribute_name, name)))
        return cls
    return decorator

def complete_comparisons(cls): # TODO Superceded by functools.total_ordering
    """A class decorator that completes a class's comparisons operators.

    The decorated class will have the operators <, <=, ==, !=, >=, >,
    assuming it already has <, and ideally == too. If the class doesn't
    even have < an assertion error is raised.

    >>> @complete_comparisons
    ... class AClass(): pass
    Traceback (most recent call last):
    ...
    AssertionError: AClass must define < and ideally ==
    >>> @complete_comparisons
    ... class Lt():
    ...     def __init__(self, x=""):
    ...         self.x = x
    ...     def __str__(self):
    ...         return self.x
    ...     def __lt__(self, other):
    ...         return str(self) < str(other)
    >>> a = Lt("a")
    >>> b = Lt("b")
    >>> b2 = Lt("b")
    >>> (a < b, a <= b, a == b, a !=b, a >= b, a > b)
    (True, True, False, True, False, False)
    >>> (b < b2, b <= b2, b == b2, b != b2, b >= b2, b > b2)
    (False, True, True, False, True, False)
    >>> @complete_comparisons
    ... class LtEq():
    ...     def __init__(self, x=""):
    ...         self.x = x
    ...     def __str__(self):
    ...         return self.x
    ...     def __lt__(self, other):
    ...         return str(self) < str(other)
    ...     def __eq__(self, other):
    ...         return str(self) == str(other)
    >>> a = LtEq("a")
    >>> b = LtEq("b")
    >>> b2 = LtEq("b")
    >>> (a < b, a <= b, a == b, a !=b, a >= b, a > b)
    (True, True, False, True, False, False)
    >>> (b < b2, b <= b2, b == b2, b != b2, b >= b2, b > b2)
    (False, True, True, False, True, False)
    """

    #Сначала сравниваем существующие методы с методами класса Object, на предмет переопределения этих методов
    assert cls.__lt__ is not object.__lt__, (
            "{0} must define < and ideally ==".format(cls.__name__))
    if cls.__eq__ is object.__eq__:
        cls.__eq__ = lambda self, other: (not
                (cls.__lt__(self, other) or cls.__lt__(other, self)))
    #Затем добавляем операции
    cls.__ne__ = lambda self, other: not cls.__eq__(self, other) #логическая операция !=
    cls.__gt__ = lambda self, other: cls.__lt__(other, self) #логическая операция >
    cls.__le__ = lambda self, other: not cls.__lt__(other, self) #логическая операция <=
    cls.__ge__ = lambda self, other: not cls.__lt__(self, other) #логическая операция >=
    return cls