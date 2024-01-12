"""
Пример, демонстрирующий организацию работы со свойствами, доступными для чтения и для записи. Класс используется для представления бытовых приборов.
Каждый объект класса, представляющий прибор должен содержать строку с названием модели, доступную только для чтения, и цену, доступную для чтения и для записи.
Необходимо гарантировать переопределение метода __init__() базового абстрактного класса в классах-наследниках.
Базовый абстрактный класс Appliance.

>>> cooker = Cooker("C412", 895.50, "coal/wood")
>>> cooker.model, cooker.price, cooker.fuel
('C412', 895.5, 'coal/wood')
>>> cooker.price = 1265
>>> cooker.price
1265
>>> fridge = Fridge("F31", 426, 290)
>>> fridge.model, fridge.price, fridge.capacity
('F31', 426, 290)
>>> fridge.price = 399
>>> fridge.capacity = 275
>>> fridge.model, fridge.price, fridge.capacity
('F31', 399, 275)
"""

import abc


class Appliance(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, model, price):
        self.__model = model
        self.price = price


    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    price = abc.abstractproperty(get_price, set_price)


    @property
    def model(self):
        return self.__model


class Cooker(Appliance):

    def __init__(self, model, price, fuel):
        super().__init__(model, price)
        self.fuel = fuel

    price = property(lambda self: super().price,
                     lambda self, price: super().set_price(price))


class Fridge(Appliance):

    def __init__(self, model, price, capacity):
        super().__init__(model, price)
        self.capacity = capacity

    price = property(lambda self: super().price,
                     lambda self, price: super().set_price(price))


if __name__ == "__main__":
    import doctest
    doctest.testmod()