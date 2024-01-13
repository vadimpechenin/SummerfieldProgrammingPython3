import unittest

from object.baseOfMetaclasses.base import Point, PointM, Point2M
from object.baseOfMetaclasses.workExample import Women


class BaseMetaTest(unittest.TestCase):

    def test_Point(self):
        pt = Point()
        self.assertEqual(pt.MAX_COORD, 100)
        self.assertEqual(pt.get_coords(), (0, 0))

        ptm = PointM()
        self.assertEqual(ptm.MAX_COORD, 100)
        self.assertEqual(ptm.get_coords(), (0, 0))

        pt2m = Point2M()
        self.assertEqual(pt2m.MAX_COORD, 100)
        self.assertEqual(pt2m.get_coords(), (0, 0))

    def test_Women(self):
        w = Women()
        self.assertEqual(w.__dict__['title'],'заголовок')
