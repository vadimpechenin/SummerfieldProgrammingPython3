import collections
import os
import pathlib
import tempfile
import unittest

from object.accessToAttributes.ord import Ord
from object.accessToAttributes.const import Const
from object.accessToAttributes.image import Image

class AccessTest(unittest.TestCase):

    def test_ord(self):
        ord = Ord()
        self.assertEqual(ord.a, 97)

    def test_const(self):
        const = Const()
        const.limit = 591
        with self.assertRaises(ValueError):
            const.limit = 400

        #Константы с использованием именованных кортежей
        Const_ = collections.namedtuple("_", "min max")(191, 591)
        self.assertEqual(Const_.min, 191)
        Offset = collections.namedtuple("_", "id name desctiption")(*range(3))
        self.assertEqual(Offset.id, 0)

    def test_image(self):
        red = "#FF0000"
        blue = "#0000FF"
        path = pathlib.Path(pathlib.Path(__file__).parent.parent.parent.resolve()).joinpath("data")
        img = pathlib.Path(path).joinpath("test.img")
        image = Image(10, 8, img)
        for x, y in ((0, 0), (0, 7), (1, 0), (1, 1), (1, 6), (1, 7), (2, 1),
                     (2, 2), (2, 5), (2, 6), (2, 7), (3, 2), (3, 3), (3, 4),
                     (3, 5), (3, 6), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4),
                     (5, 5), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (7, 1),
                     (7, 2), (7, 5), (7, 6), (7, 7), (8, 0), (8, 1), (8, 6),
                     (8, 7), (9, 0), (9, 7)):

            image[x, y] = blue
        for x, y in ((3, 1), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2),
                          (6, 1)):

            image[(x, y)] = red
        print(image.width, image.height, len(image.colors), image.background)
        border_color = "#FF0000"
        square_color = "#0000FF"
        width, height = 240, 60
        midx, midy = width // 2, height // 2
        image = Image(width, height, img, "#F0F0F0")
        for x in range(width):
            for y in range(height):
                if x < 5 or x >= width - 5 or y < 5 or y >= height - 5:
                    image[x, y] = border_color
                elif midx - 20 < x < midx + 20 and midy - 20 < y < midy + 20:
                    image[x, y] = square_color
        print(image.width, image.height, len(image.colors), image.background)
        image.save()