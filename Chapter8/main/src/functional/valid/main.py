import re
from functional.valid.valid import valid_string, valid_number

@valid_string("name", empty_allowed=False)
@valid_string("productid", empty_allowed=False,
              regex=re.compile(r"[A-Z]{3}\d{4}")) #Строка, которая начинается с трех алфавитных символов верхнего регистра и заканчивается четыремя цифрами
@valid_string("category", empty_allowed=False, acceptable=
        frozenset(["Consumables", "Hardware", "Software", "Media"]))
@valid_number("price", minimum=0, maximum=1e6)
@valid_number("quantity", minimum=1, maximum=1000)
class StockItem:

     def __init__(self, name, productid, category, price, quantity):
         self.name = name
         self.productid = productid
         self.category = category
         self.price = price
         self.quantity = quantity

     @property
     def value(self):
         return self.price * self.quantity