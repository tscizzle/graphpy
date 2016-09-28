"""
Tests for helpers.py
"""


import graphpy.helpers

import unittest


class TestUndirectedEdge(unittest.TestCase):

    def test_is_hashable(self):
        """ Check if an object is hashable """
        is_hashable = graphpy.helpers.is_hashable

        hashables = [0, '', 'nonempty', tuple(), (0, 1)]
        not_hashables = [{}, [], set(), {0, 1}, ('', {})]

        for h in hashables:
            self.assertTrue(is_hashable(h))
        for nh in not_hashables:
            self.assertFalse(is_hashable(nh))


if __name__ == '__main__':
    unittest.main()
