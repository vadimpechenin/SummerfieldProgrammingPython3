import unittest

from object.descriptors.externalStorage import Point, Circle
from object.descriptors.property import NameAndExtension
from object.descriptors.xmlShadow import Product, CachedProduct


class DescriptorsTest(unittest.TestCase):

    def test_XmlShadow(self):
        product = Product("Chisel <3cm>", "Chisel & cap", 45.25)
        self.assertEqual(product.name_as_xml, 'Chisel &lt;3cm&gt;')
        self.assertEqual(product.description_as_xml, 'Chisel &amp; cap')

        product = CachedProduct("Chisel <3cm>", "Chisel & cap", 45.25)
        self.assertEqual(product.name_as_xml, 'Chisel &lt;3cm&gt;')
        self.assertEqual(product.description_as_xml, 'Chisel &amp; cap')

    def test_ExternalStorage(self):
        point = Point()
        point.x = 12
        self.assertEqual(point.x, 12)
        a = Point(3, 4)
        b = Point(3, 4)
        self.assertEqual(a, b)
        self.assertNotEqual(a, point)

        circle = Circle(2)
        circle.radius = 3
        circle.x = 12
        self.assertEqual(circle.radius, 3)
        self.assertEqual(circle.x, 12)

        a = Circle(4, 5, 6)
        b = Circle(4, 5, 6)
        self.assertEqual(a, b)
        self.assertNotEqual(a, circle)

    def test_proterty(self):
        contact = NameAndExtension("Joe", 135)
        self.assertEqual(contact.name, "Joe")
        with self.assertRaises(AttributeError):
            contact.name = "Jane"

        contact.extension = 975
        self.assertEqual(contact.extension, 975)



