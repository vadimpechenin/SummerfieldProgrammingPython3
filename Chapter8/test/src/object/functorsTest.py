import operator
import unittest

from object.functors.sortKey import Person, SortKey
from object.functors.strip import Strip, make_strip_function


class FunctorsTest(unittest.TestCase):

    def test_strip(self):
        strip_punctuation = Strip(",;:.!?")
        self.assertEqual(strip_punctuation("Land ahoy!"),"Land ahoy")

        strip_punctuation = make_strip_function(",;:.!?")
        self.assertEqual(strip_punctuation("Land ahoy!"), "Land ahoy")

    def test_sort(self):
        list_attr = [["Вадим", "Печенин","4@mail.ru"],["Ермак", "Тимофеевич","5@mail.ru"],["Олег", "Рюрикович","oleg@gmail.com"],["Антон", "Алексеев","anton@gmail.com"]]
        people1 = []
        people2 = []
        for item in list_attr:
            people1.append(Person(item[0], item[1], item[2]))
            people2.append(Person(item[0], item[1], item[2]))
        #Сортировка
        people1.sort(key=SortKey("surname", "forename"))
        people2.sort(key=operator.attrgetter("surname", "forename"))
        self.assertEqual(people1[0].forename, people2[0].forename)
