import unittest

from object.contextManagers.atomicList import AtomicList


class ContextManagerTest(unittest.TestCase):

    def test_AtomicList(self):
        items = [1, 2, 3, 4, 5]
        index = 1
        try:
            with AtomicList(items) as atomic:
                atomic.append(58289)
                del atomic[3]
                atomic[0] = 81738
                atomic[index] = 38172
            self.assertEqual(atomic[4], 58289)
        except (AttributeError, IndexError, ValueError) as err:
            print("no changes applied:", err)
