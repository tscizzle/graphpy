"""
Tests for helpers.py
"""


from graphpy.helpers import *

import unittest


################################################################################
#                                                                              #
#                                Miscellaneous                                 #
#                                                                              #
################################################################################


class TestMiscellaneous(unittest.TestCase):

    def test_is_hashable(self):
        """ Check if an object is hashable """
        hashables = [0, '', 'nonempty', tuple(), (0, 1)]
        not_hashables = [{}, [], set(), {0, 1}, ('', {})]

        for h in hashables:
            self.assertTrue(is_hashable(h))
        for nh in not_hashables:
            self.assertFalse(is_hashable(nh))

    def test_keydefaultdict(self):
        """ Make a defaultdict-like object whose default_factory takes the
            requested key as an argument """
        default_square = keydefaultdict(lambda x: x**2)
        default_square[5] = 7

        self.assertEqual(default_square[0], 0)
        self.assertEqual(default_square[1], 1)
        self.assertEqual(default_square[2], 4)
        self.assertEqual(default_square[5], 7)


################################################################################
#                                                                              #
#                                Priority Queue                                #
#                                                                              #
################################################################################


class TestPriorityQueue(unittest.TestCase):

    def test_priority_queue_contains(self):
        """ Check if a priority queue contains a certain element """
        pq = PriorityQueue(data=[(5, 'E'), (1, 'A'), (4, 'D')])
        empty_pq = PriorityQueue()

        self.assertTrue('A' in pq)
        self.assertFalse('F' in pq)

        pq.pop_min()

        self.assertFalse('A'in pq)

        self.assertFalse('A' in empty_pq)

    def test_priority_queue_find_min(self):
        """ Peek at the minimum element in a priority queue without modifying
            the priority queue """
        pq = PriorityQueue(data=[(5, 'E'), (1, 'A'), (4, 'D')])
        empty_pq = PriorityQueue()

        self.assertEqual(pq.find_min(), (1, 'A'))
        self.assertEqual(pq.find_min(), (1, 'A'))

        pq.pop_min()

        self.assertEqual(pq.find_min(), (4, 'D'))

        with self.assertRaises(IndexError):
            empty_pq.find_min()

    def test_priority_queue_pop_min(self):
        """ Pop the minimum element from a priority queue """
        pq = PriorityQueue(data=[(5, 'E'), (1, 'A'), (4, 'D')])

        self.assertEqual(pq.pop_min(), (1, 'A'))
        self.assertEqual(pq.pop_min(), (4, 'D'))
        self.assertEqual(pq.pop_min(), (5, 'E'))
        with self.assertRaises(IndexError):
            pq.pop_min()

    def test_priority_queue_insert(self):
        """ Insert an element into a priority queue """
        pq = PriorityQueue(data=[(5, 'E'), (2, 'B'), (4, 'D')])
        pq.insert('C', 3)

        self.assertEqual(pq.find_min(), (2, 'B'))

        pq.insert('A', 1)

        self.assertEqual(pq.find_min(), (1, 'A'))
        with self.assertRaises(ValueError):
            pq.insert('A', 6)

    def test_priority_queue_decrease_key(self):
        """ Decrease the priority for an item """
        pq = PriorityQueue(data=[(5, 'E'), (2, 'B'), (4, 'D')])
        pq.decrease_key('D', 1)

        self.assertEqual(pq.pop_min(), (1, 'D'))
        with self.assertRaises(KeyError):
            pq.decrease_key('A', 3)
        with self.assertRaises(ValueError):
            pq.decrease_key('E', 7)


if __name__ == '__main__':
    unittest.main()
