import unittest

from object.decorators.FuzzyBool import FuzzyBool
from object.decorators.SortedListDelegate import SortedList


class DecoratorsTest(unittest.TestCase):

    def test_SortedList(self):
        L = SortedList((5, 8, -1, 3, 4, 22))
        with self.assertRaises(TypeError):
            L[2] = 18

        L.add(5)
        L.add(5)
        L.add(6)
        self.assertEqual(L.index(4),2)
        self.assertEqual(L.count(5),3)
        with self.assertRaises(AttributeError):
            L.reverse()
        del L[0]
        self.assertEqual(L.index(4), 1)

    def test_FuzzyBool(self):
        f = FuzzyBool()
        g = FuzzyBool(.5)
        h = FuzzyBool(3.75)
        self.assertEqual(g, FuzzyBool(0.5))
        self.assertTrue(g.__ge__(FuzzyBool(0.4))) #>=
        self.assertTrue(h.__eq__(FuzzyBool(0))) #==
        h = ~h
        self.assertEqual(h, FuzzyBool(1))
        f = FuzzyBool(0.2)
        self.assertTrue(f<g)
        with self.assertRaises(TypeError):
            f + g
        self.assertEqual(int(h) + int(g), 1)