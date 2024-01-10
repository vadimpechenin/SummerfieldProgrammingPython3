import unittest

from functional.valid import main


class ValidTest(unittest.TestCase):

    def test_valid(self):
        name = "PMM"
        productid = "AAA0000"
        category = "Hardware"
        price = 1e6
        quantity = 500
        stockItem = main.StockItem(name, productid, category, price, quantity)

        self.assertEqual(stockItem.price, 1e6)

    def test_no_valid(self):
        name = "PMM"
        productid = "AAA0000"
        category = "Hardware"
        price = 1e6
        quantity = 10000
        with self.assertRaises(ValueError):
            stockItem = main.StockItem(name, productid, category, price, quantity)


