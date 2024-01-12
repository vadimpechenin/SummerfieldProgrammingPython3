import unittest

from object.abstractBase.SortedListAbs import SortedList
from object.abstractBase.appliance import Cooker, Fridge
from object.abstractBase.textFilter import CharCounter, RunLengthEncode, RunLengthDecode


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

    def test_Appliance(self):
        cooker = Cooker("C412", 895.50, "coal/wood")
        self.assertEqual(cooker.price, 895.50)
        cooker.price = 1265
        self.assertEqual(cooker.price, 1265)
        fridge = Fridge("F31", 426, 290)
        fridge.capacity = 275
        self.assertEqual(fridge.capacity, 275)

    def test_TextFilter(self):
        vowel_counter = CharCounter()
        self.assertEqual(vowel_counter("dog fish and cat fish", "aeiou"), 5)
        text = "The Title\\n=========\\nThe text\\n"
        rle_encoder = RunLengthEncode()
        rle = rle_encoder(text)
        self.assertEqual(len(rle), 26)
        rle_decoder = RunLengthDecode()
        string = rle_decoder(rle)
        self.assertEqual(string, text)

