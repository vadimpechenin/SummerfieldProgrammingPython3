import unittest

from structural.recursion import main


class RecursionTest(unittest.TestCase):

    def test_factorial(self):
        res = main.factorial(10)
        self.assertEqual(res, 3628800)

    def test_indented_list(self):
        before = ["Nonmetals",
                  "    Hydrogen",
                  "    Carbon",
                  "    Nitrogen",
                  "    Oxygen",
                  "Inner Transitionals",
                  "    Lanthanides",
                  "        Cerium",
                  "        Europium",
                  "    Actinides",
                  "        Uranium",
                  "        Curium",
                  "        Plutonium",
                  "Alkali Metals",
                  "    Lithium",
                  "    Sodium",
                  "    Potassium"]

        result1 = main.indented_list_sort(before)
        result2 = main.indented_list_sort_local(before)

        after = ["Alkali Metals",
                 "    Lithium",
                 "    Potassium",
                 "    Sodium",
                 "Inner Transitionals",
                 "    Actinides",
                 "        Curium",
                 "        Plutonium",
                 "        Uranium",
                 "    Lanthanides",
                 "        Cerium",
                 "        Europium",
                 "Nonmetals",
                 "    Carbon",
                 "    Hydrogen",
                 "    Nitrogen",
                 "    Oxygen"]
        self.assertEqual(result1, result2, after)