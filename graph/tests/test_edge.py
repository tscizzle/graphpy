"""
Tests for edge.py
"""


from edge import UndirectedEdge, DirectedEdge, NoSelfEdgeException
from vertex import UndirectedVertex, DirectedVertex

import unittest


class TestUndirectedEdge(unittest.TestCase):

    def test_create_undirected_edge(self):
        """ Create a undirected edge """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        e = UndirectedEdge(v0, v1)

        self.assertEqual(e.vertices, set([v0, v1]))

    def test_no_self_undirected_edge(self):
        """ Undirected edges should not be able to connect a vertex to
            itself """
        v = UndirectedVertex(name='v')

        with self.assertRaises(NoSelfEdgeException):
            UndirectedEdge(v, v)

    def test_undirected_edge_equality(self):
        """ Compare undirected edges for equality """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        e01 = UndirectedEdge(v0, v1)
        e02 = UndirectedEdge(v0, v2)
        e12 = UndirectedEdge(v1, v2)
        e10 = UndirectedEdge(v1, v0)
        another_e01 = UndirectedEdge(v0, v1)

        self.assertEqual(e01, e01)
        self.assertEqual(e02, e02)
        self.assertEqual(e12, e12)
        self.assertNotEqual(e01, e02)
        self.assertNotEqual(e01, e12)
        self.assertNotEqual(e02, e12)
        self.assertEqual(e01, e10)
        self.assertEqual(e01, another_e01)


class TestDirectedEdge(unittest.TestCase):

    def test_create_directed_edge(self):
        """ Create a undirected edge """
        v0 = DirectedVertex()
        v1 = DirectedVertex()
        e00 = DirectedEdge(v0, v0)
        e01 = DirectedEdge(v0, v1)

        self.assertEqual(e00.v_from, v0)
        self.assertEqual(e00.v_to, v0)
        self.assertEqual(e01.v_from, v0)
        self.assertEqual(e01.v_to, v1)

    def test_undirected_edge_equality(self):
        """ Compare undirected edges for equality """
        v0 = DirectedVertex()
        v1 = DirectedVertex()
        v2 = DirectedVertex()
        e00 = DirectedEdge(v0, v0)
        e01 = DirectedEdge(v0, v1)
        e10 = DirectedEdge(v1, v0)
        e11 = DirectedEdge(v1, v1)
        e02 = DirectedEdge(v0, v2)
        another_e01 = DirectedEdge(v0, v1)

        self.assertEqual(e00, e00)
        self.assertEqual(e01, e01)
        self.assertEqual(e10, e10)
        self.assertEqual(e11, e11)
        self.assertNotEqual(e01, e02)
        self.assertNotEqual(e01, e10)
        self.assertEqual(e01, another_e01)


if __name__ == '__main__':
    unittest.main()
