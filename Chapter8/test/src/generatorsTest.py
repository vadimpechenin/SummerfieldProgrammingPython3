import unittest

from structural.generators import main


class GeneratorsTest(unittest.TestCase):

    def test_quarters(self):
        res = main.five_quarters()
        self.assertEqual(len(res), 5)

    def test_items_in_key_order(self):
        test_dict = {1: "1", 3: "3", 2: "2", 4: "4", 6: "6"}
        generator1 = main.items_in_key_order_yield(test_dict)
        generator2 = main.items_in_key_order(test_dict)
        for (x, y) in zip(generator1, generator2):
            self.assertEqual(x, y)