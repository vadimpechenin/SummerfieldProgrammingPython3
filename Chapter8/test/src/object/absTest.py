import unittest

from object.abstractBase.SortedListAbs import SortedList


class ABSTest(unittest.TestCase):

    def test_SortedList(self):
        L = SortedList((5, 8, -1, 3, 4, 22))
        with self.assertRaises(TypeError):
            L[2] = 18

        L.add(5)
        L.add(5)
        L.add(6)
        self.assertEqual(L.index(4), 2)
        self.assertEqual(L.count(5), 3)
        with self.assertRaises(AttributeError):
            L.reverse()
        del L[0]
        self.assertEqual(L.index(4), 1)