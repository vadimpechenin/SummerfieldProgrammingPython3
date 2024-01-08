import unittest

from structural.decorators import main


class DecoratorTest(unittest.TestCase):

    def test_disctiminant(self):
        a = 1
        b = 4
        c = 3
        res = main.discriminant(a, b, c)
        self.assertEqual(res, 4)

    def test_persent(self):
        amount = 200
        total = 150
        res = main.percent(amount, total)
        self.assertEqual(res, 100)

    def test_logger(self):
        res = main.discounted_price(100, 10)
        self.assertEqual(res, 90.0)
        self.assertEqual(main.discounted_price(210, 5), 199.5)
        self.assertEqual(main.discounted_price(210, 5, make_integer=True), 200)
        self.assertEqual(main.discounted_price(210, 14, True), 181)
        with self.assertRaises(ValueError):
            main.discounted_price(210, -8)

    def test_annotation(self):
        self.assertFalse(main.is_unicode_punctuation("zebr\a"))
        self.assertTrue(main.is_unicode_punctuation(s="!@#?"))
        with self.assertRaises(AssertionError):
            main.is_unicode_punctuation(("!", "@"))