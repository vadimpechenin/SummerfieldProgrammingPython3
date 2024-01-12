import unittest

from object.multipleInheritance.main import FileStack

import os
import tempfile
class MultipleInheritanceTest(unittest.TestCase):

    def test_FileStack(self):
        filename = os.path.join(tempfile.gettempdir(), "fs.pkl")
        fs = FileStack(filename)
        for x in list(range(-5, 0)) + list(range(5)):
            fs.push(x)
        self.assertEqual(fs.top(), 4)
        total = 0
        for x in range(5):
            total += fs.pop()
        self.assertEqual(total, 10)
        fs.push(909)
        fs.save()
        fs2 = FileStack(filename)
        fs2.push(-32)
        self.assertEqual(os.path.basename(fs.filename),'fs.pkl')
        self.assertTrue(fs2.can_undo)