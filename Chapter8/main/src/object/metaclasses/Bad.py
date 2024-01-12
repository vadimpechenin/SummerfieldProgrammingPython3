from object.metaclasses.LoadableSaveable import LoadableSaveable


class Bad(metaclass=LoadableSaveable):
    def some_method(self):
        pass