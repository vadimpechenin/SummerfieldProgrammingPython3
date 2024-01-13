import unittest

from object.metaclasses.AutoSlotProperties import Product, Point, PointA
from object.metaclasses.LoadableSaveable import Good


class MetaTest(unittest.TestCase):

    def test_LoadbleSaveable(self):
        g = Good()
        with self.assertRaises(AssertionError):
            from object.metaclasses.Bad import Bad
            b = Bad()

    def test_AutoSlotProperties(self):
        #В классе для одного свойства не реализован set метод
        product = Product("101110110", "8mm Stapler")
        self.assertEqual(product.barcode, "101110110")
        self.assertEqual(product.description, "8mm Stapler")
        with self.assertRaises(AttributeError):
            product.barcode = "XXX"

        product.description = "8mm Stapler (long)"
        self.assertEqual(product.description, "8mm Stapler (long)")

        point = Point(-17, 9181)
        self.assertEqual(point.x, 0)
        point = Point(91, 181)
        self.assertEqual(point.y, 181)

        point = PointA(-17, 9181, -18)
        self.assertEqual(point.y, 1024)
        self.assertEqual(point.a, -18)



