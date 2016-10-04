"""
Tests for edge.py
"""


from graphpy.edge import UndirectedEdge, DirectedEdge
from graphpy.vertex import UndirectedVertex, DirectedVertex

import unittest


################################################################################
#                                                                              #
#                                  Undirected                                  #
#                                                                              #
################################################################################


class TestUndirectedEdge(unittest.TestCase):

    def test_create_undirected_edge(self):
        """ Create an undirected edge """
        v0 = UndirectedVertex(val='v0')
        v1 = UndirectedVertex(val='v1')
        e00 = UndirectedEdge((v0, v0), attrs={'weight': 5, 0: 1})
        e01 = UndirectedEdge((v0, v1))

        self.assertEqual(e00.vertices, frozenset([v0]))
        self.assertEqual(e00.attrs, {'weight': 5, 0: 1})
        self.assertEqual(e01.vertices, frozenset([v0, v1]))
        self.assertEqual(e01.attrs, {})

    def test_undirected_edge_equality(self):
        """ Compare undirected edges for equality """
        v0 = UndirectedVertex(val='v0')
        v1 = UndirectedVertex(val='v1')
        v2 = UndirectedVertex(val='v2')
        e01 = UndirectedEdge((v0, v1))
        e02 = UndirectedEdge((v0, v2))
        e12 = UndirectedEdge((v1, v2))
        e10 = UndirectedEdge((v1, v0))
        another_e01 = UndirectedEdge((v0, v1))

        self.assertEqual(e01, e01)
        self.assertEqual(e02, e02)
        self.assertEqual(e12, e12)
        self.assertNotEqual(e01, e02)
        self.assertNotEqual(e01, e12)
        self.assertNotEqual(e02, e12)
        self.assertEqual(e01, e10)
        self.assertEqual(e01, another_e01)

    def test_undirected_edge_hashing(self):
        """ Hash an undirected edge """
        v0 = UndirectedVertex(val='v0')
        v1 = UndirectedVertex(val='v1')
        v2 = UndirectedVertex(val='v2')
        e01 = UndirectedEdge((v0, v1))
        e02 = UndirectedEdge((v0, v2))
        e10 = UndirectedEdge((v1, v0))
        edge_set = set([e01])

        self.assertTrue(e01 in edge_set)
        self.assertTrue(e10 in edge_set)
        self.assertFalse(e02 in edge_set)

    def test_undirected_edge_vertices(self):
        """ Get an undirected edge's vertices property """
        v0 = UndirectedVertex(val='v0')
        v1 = UndirectedVertex(val='v1')
        e01 = UndirectedEdge((v0, v1))

        self.assertEqual(e01.vertices, frozenset([v0, v1]))
        with self.assertRaises(AttributeError):
            e01.vertices = frozenset()

    def test_undirected_edge_attrs(self):
        """ Get an undirected edge's attrs property """
        v0 = UndirectedVertex(val='v0')
        v1 = UndirectedVertex(val='v1')
        e01 = UndirectedEdge((v0, v1), {'weight': 5})

        self.assertEqual(e01.attrs, {'weight': 5})
        with self.assertRaises(AttributeError):
            e01.attrs = {'key': 'value'}

    def test_undirected_edge_is_self_edge(self):
        """ Get an undirected edge's is_self_edge property """
        v0 = UndirectedVertex(val='v0')
        v1 = UndirectedVertex(val='v1')
        e00 = UndirectedEdge((v0, v0))
        e01 = UndirectedEdge((v0, v1))

        self.assertTrue(e00.is_self_edge)
        self.assertFalse(e01.is_self_edge)
        with self.assertRaises(AttributeError):
            e00.is_self_edge = False

    def test_undirected_edge_get(self):
        """ Get an attribute of an undirected edge """
        v0 = UndirectedVertex(val='v0')
        v1 = UndirectedVertex(val='v1')
        e01 = UndirectedEdge((v0, v1), attrs={'weight': 5})

        self.assertEqual(e01.get('weight'), 5)
        self.assertIsNone(e01.get('notthere'))

    def test_undirected_edge_set(self):
        """ Set an attribute of an undirected edge """
        v0 = UndirectedVertex(val='v0')
        v1 = UndirectedVertex(val='v1')
        e01 = UndirectedEdge((v0, v1))

        e01.set('weight', 5)

        self.assertEqual(e01.attrs, {'weight': 5})

        e01.set(0, 1)

        self.assertEqual(e01.attrs, {'weight': 5, 0: 1})

    def test_undirected_edge_has_attr(self):
        """ Check if an undirected edge has a particular attribute """
        v0 = UndirectedVertex(val='v0')
        v1 = UndirectedVertex(val='v1')
        e01 = UndirectedEdge((v0, v1), attrs={'weight': 5, 0: 1})

        self.assertTrue(e01.has_attr('weight'))
        self.assertFalse(e01.has_attr('length'))

        e01.del_attr('weight')

        self.assertFalse(e01.has_attr('weight'))

    def test_undirected_edge_del_attr(self):
        """ Delete an attribute of an undirected edge """
        v0 = UndirectedVertex(val='v0')
        v1 = UndirectedVertex(val='v1')
        e01 = UndirectedEdge((v0, v1), attrs={'weight': 5, 0: 1})

        e01.del_attr('weight')

        self.assertEqual(e01.attrs, {0: 1})

        e01.del_attr(0)

        self.assertEqual(e01.attrs, {})


################################################################################
#                                                                              #
#                                   Directed                                   #
#                                                                              #
################################################################################


class TestDirectedEdge(unittest.TestCase):

    def test_create_directed_edge(self):
        """ Create a directed edge """
        v0 = DirectedVertex()
        v1 = DirectedVertex()
        e00 = DirectedEdge((v0, v0), attrs={'weight': 5, 0: 1})
        e01 = DirectedEdge((v0, v1))

        self.assertEqual(e00.v_from, v0)
        self.assertEqual(e00.v_to, v0)
        self.assertEqual(e00.attrs, {'weight': 5, 0: 1})
        self.assertEqual(e01.v_from, v0)
        self.assertEqual(e01.v_to, v1)
        self.assertEqual(e01.attrs, {})

    def test_undirected_edge_equality(self):
        """ Compare directed edges for equality """
        v0 = DirectedVertex()
        v1 = DirectedVertex()
        v2 = DirectedVertex()
        e00 = DirectedEdge((v0, v0))
        e01 = DirectedEdge((v0, v1))
        e10 = DirectedEdge((v1, v0))
        e11 = DirectedEdge((v1, v1))
        e02 = DirectedEdge((v0, v2))
        another_e01 = DirectedEdge((v0, v1))

        self.assertEqual(e00, e00)
        self.assertEqual(e01, e01)
        self.assertEqual(e10, e10)
        self.assertEqual(e11, e11)
        self.assertNotEqual(e01, e02)
        self.assertNotEqual(e01, e10)
        self.assertEqual(e01, another_e01)

    def test_directed_edge_hashing(self):
        """ Hash a directed edge """
        v0 = DirectedVertex(val='v0')
        v1 = DirectedVertex(val='v1')
        v2 = DirectedVertex(val='v2')
        e01 = DirectedEdge((v0, v1))
        e02 = DirectedEdge((v0, v2))
        e10 = DirectedEdge((v1, v0))
        another_e01 = DirectedEdge((v0, v1))
        edge_set = set([e01])

        self.assertTrue(e01 in edge_set)
        self.assertFalse(e10 in edge_set)
        self.assertFalse(e02 in edge_set)
        self.assertTrue(another_e01 in edge_set)

    def test_directed_edge_v_from_and_v_to(self):
        """ Get a directed edge's v_from and v_to properties """
        v0 = DirectedVertex(val='v0')
        v1 = DirectedVertex(val='v1')
        v2 = DirectedVertex(val='v2')
        v3 = DirectedVertex(val='v3')
        e01 = DirectedEdge((v0, v1))

        self.assertEqual(e01.v_from, v0)
        self.assertEqual(e01.v_to, v1)
        with self.assertRaises(AttributeError):
            e01.v_from = v2
        with self.assertRaises(AttributeError):
            e01.v_to = v3

    def test_directed_edge_attrs(self):
        """ Get an directed edge's attrs property """
        v0 = DirectedVertex(val='v0')
        v1 = DirectedVertex(val='v1')
        e01 = DirectedEdge((v0, v1), {'weight': 5})

        self.assertEqual(e01.attrs, {'weight': 5})
        with self.assertRaises(AttributeError):
            e01.attrs = {'key': 'value'}

    def test_directed_edge_get(self):
        """ Get an attribute of a directed edge """
        v0 = DirectedVertex(val='v0')
        v1 = DirectedVertex(val='v1')
        e01 = DirectedEdge((v0, v1), attrs={'weight': 5})

        self.assertEqual(e01.get('weight'), 5)
        self.assertIsNone(e01.get('notthere'))

    def test_directed_edge_set(self):
        """ Set an attribute of a directed edge """
        v0 = DirectedVertex(val='v0')
        v1 = DirectedVertex(val='v1')
        e01 = DirectedEdge((v0, v1))

        e01.set('weight', 5)

        self.assertEqual(e01.attrs, {'weight': 5})

        e01.set(0, 1)

        self.assertEqual(e01.attrs, {'weight': 5, 0: 1})

    def test_directed_edge_has_attr(self):
        """ Check if a directed edge has a particular attribute """
        v0 = DirectedVertex(val='v0')
        v1 = DirectedVertex(val='v1')
        e01 = DirectedEdge((v0, v1), attrs={'weight': 5, 0: 1})

        self.assertTrue(e01.has_attr('weight'))
        self.assertFalse(e01.has_attr('length'))

        e01.del_attr('weight')

        self.assertFalse(e01.has_attr('weight'))

    def test_directed_edge_del_attr(self):
        """ Delete an attribute of a directed edge """
        v0 = DirectedVertex(val='v0')
        v1 = DirectedVertex(val='v1')
        e01 = DirectedEdge((v0, v1), attrs={'weight': 5, 0: 1})

        e01.del_attr('weight')

        self.assertEqual(e01.attrs, {0: 1})

        e01.del_attr(0)

        self.assertEqual(e01.attrs, {})


if __name__ == '__main__':
    unittest.main()
