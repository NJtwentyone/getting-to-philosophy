import unittest
from data_struct import PeekQueue

class TestPeekQueue(unittest.TestCase):
    def setUp(self):
        self.queue = PeekQueue()

    def test_isEmpty(self):
        self.assertTrue(self.queue.isEmpty())

        self.queue.add('A')
        self.assertFalse(self.queue.isEmpty())

        self.queue.add('B')
        self.queue.add('C')
        self.assertFalse(self.queue.isEmpty())

        self.queue.remove()
        self.assertFalse(self.queue.isEmpty())

        self.queue.remove()
        self.assertFalse(self.queue.isEmpty())

        self.queue.remove()
        self.assertTrue(self.queue.isEmpty())

    def test_FIFO(self):

        item1 = 'A'
        item2 = 'B'
        item3 = 'C'

        self.queue.add(item1)
        self.assertEqual(self.queue.peek(), item1)

        self.queue.add(item2)
        self.assertEqual(self.queue.peek(), item1)

        remove1 = self.queue.remove()
        self.assertEqual(remove1, item1)
        self.assertEqual(self.queue.peek(), item2)

        self.queue.add(item3)
        remove2 = self.queue.remove()
        remove3 = self.queue.remove()

        self.assertEqual(remove1, item1)
        self.assertEqual(remove2, item2)

    def test_Size(self):

        self.assertEqual(self.queue.size(), 0)

        self.queue.add('A')
        self.assertEqual(self.queue.size(), 1)

        self.queue.add('B')
        self.assertEqual(self.queue.size(), 2)

        self.queue.add('C')
        self.assertEqual(self.queue.size(), 3)

        self.queue.add('B')
        self.assertEqual(self.queue.size(), 4)

        self.queue.remove()
        self.assertEqual(self.queue.size(), 3)

        self.queue.add('D')
        self.queue.remove()
        self.assertEqual(self.queue.size(), 3)

        self.queue.remove()
        self.queue.remove()
        self.queue.remove()
        self.assertEqual(self.queue.size(), 0)

        self.queue.add('X')
        self.assertEqual(self.queue.size(), 1)


if __name__ == '__main__':
    unittest.main()
