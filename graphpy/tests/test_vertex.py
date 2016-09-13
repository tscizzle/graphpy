"""
Tests for vertex.py
"""


from edge import UndirectedEdge, DirectedEdge
from vertex import (UndirectedVertex, DirectedVertex,
                    VertexAlreadyHasEdgeException, VertexNotPartOfEdgeException)

import unittest


class TestUndirectedVertex(unittest.TestCase):

    def test_create_undirected_vertex(self):
        """ Create an undirected vertex """
        v0 = UndirectedVertex(name='v0')

        self.assertEqual(v0.name, 'v0')
        self.assertEqual(v0.edges, set())

    def test_undirected_vertex_name(self):
        """ Get an undirected vertex's name property """
        v0 = UndirectedVertex(name='v0')

        self.assertEqual(v0.name, 'v0')
        with self.assertRaises(AttributeError):
            v0.name = ''

    def test_undirected_vertex_neighbors_and_degree(self):
        """ Get undirected vertices' neighbors and degree properties """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        e01 = UndirectedEdge(v0, v1)
        e02 = UndirectedEdge(v0, v2)
        v0.add_edge(e01)
        v0.add_edge(e02)

        self.assertEqual(v0.neighbors, set([v1, v2]))
        with self.assertRaises(AttributeError):
            v0.neighbors = set()
        self.assertEqual(v0.degree, 2)
        with self.assertRaises(AttributeError):
            v0.degree = 0

    def test_undirected_vertex_add_edge(self):
        """ Add an edge to an undirected vertex """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        e01 = UndirectedEdge(v0, v1)
        e10 = UndirectedEdge(v1, v0)
        e02 = UndirectedEdge(v0, v2)
        v0.add_edge(e01)

        self.assertTrue(e01 in v0)
        self.assertTrue(e10 in v0)
        self.assertFalse(e02 in v0)

    def test_undirected_vertex_remove_edge(self):
        """ Remove an edge from an undirected vertex """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        e01 = UndirectedEdge(v0, v1)
        e10 = UndirectedEdge(v1, v0)
        e02 = UndirectedEdge(v0, v2)
        v0.add_edge(e01)
        v0.add_edge(e02)

        v0.remove_edge(e01)

        self.assertFalse(e01 in v0)
        self.assertFalse(e10 in v0)
        self.assertTrue(e02 in v0)

        v0.remove_edge(e02)

        self.assertFalse(e01 in v0)
        self.assertFalse(e10 in v0)
        self.assertFalse(e02 in v0)

    def test_undirected_vertex_already_has_edge(self):
        """ An undirected vertex should not be able to add an edge that it
            already has """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        e01 = UndirectedEdge(v0, v1)
        v0.add_edge(e01)

        with self.assertRaises(VertexAlreadyHasEdgeException):
            v0.add_edge(e01)
        try:
            v1.add_edge(e01)
        except VertexAlreadyHasEdgeException:
            self.fail("Adding the edge (v0, v1) to v0 should not stop the edge "
                      "(v0, v1) from being added to v1.")

    def test_undirected_vertex_not_part_of_edge(self):
        """ An undirected vertex should not be able add an edge which doesn't
            have it as a vertex """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        e12 = UndirectedEdge(v1, v2)

        with self.assertRaises(VertexNotPartOfEdgeException):
            v0.add_edge(e12)


class TestDirectedVertex(unittest.TestCase):

    def test_create_directed_vertex(self):
        """ Create a directed vertex """
        v0 = DirectedVertex(name='v0')

        self.assertEqual(v0.name, 'v0')
        self.assertEqual(v0.edges, set())

    def test_directed_vertex_name(self):
        """ Get a directed vertex's name property """
        v0 = DirectedVertex(name='v0')

        self.assertEqual(v0.name, 'v0')
        with self.assertRaises(AttributeError):
            v0.name = ''

    def test_directed_vertex_outs_and_ins_and_degrees(self):
        """ Get directed vertices' outs, ins, out_degree, and in_degree
            properties """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        e00 = DirectedEdge(v0, v0)
        e01 = DirectedEdge(v0, v1)
        e02 = DirectedEdge(v0, v2)
        e10 = DirectedEdge(v1, v0)
        v0.add_edge(e00)
        v0.add_edge(e01)
        v0.add_edge(e02)
        v0.add_edge(e10)

        self.assertEqual(v0.outs, set([v0, v1, v2]))
        self.assertEqual(v0.ins, set([v0, v1]))
        self.assertEqual(v0.out_degree, 3)
        self.assertEqual(v0.in_degree, 2)

    def test_directed_vertex_add_edge(self):
        """ Add an edge to a directed vertex """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        e01 = DirectedEdge(v0, v1)
        e10 = DirectedEdge(v1, v0)
        e02 = DirectedEdge(v0, v2)
        v0.add_edge(e01)

        self.assertTrue(e01 in v0)
        self.assertFalse(e10 in v0)
        self.assertFalse(e02 in v0)

    def test_directed_vertex_remove_edge(self):
        """ Remove an edge from a directed vertex """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        e01 = DirectedEdge(v0, v1)
        e10 = DirectedEdge(v1, v0)
        e02 = DirectedEdge(v0, v2)
        v0.add_edge(e01)
        v0.add_edge(e10)
        v0.add_edge(e02)

        v0.remove_edge(e01)

        self.assertFalse(e01 in v0)
        self.assertTrue(e10 in v0)
        self.assertTrue(e02 in v0)

        v0.remove_edge(e02)

        self.assertFalse(e01 in v0)
        self.assertTrue(e10 in v0)
        self.assertFalse(e02 in v0)

    def test_directed_vertex_already_has_edge(self):
        """ A directed vertex should not be able to add an edge that it already
            has """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        e01 = DirectedEdge(v0, v1)
        e10 = DirectedEdge(v1, v0)
        v0.add_edge(e01)

        with self.assertRaises(VertexAlreadyHasEdgeException):
            v0.add_edge(e01)
        try:
            v0.add_edge(e10)
        except VertexAlreadyHasEdgeException:
            self.fail("There should be no exception because (v1 -> v0) is a "
                      "different edge than (v0 -> v1) for a directed vertex.")

    def test_directed_vertex_not_part_of_edge(self):
        """ A directed vertex should not be able add an edge which doesn't have
            it as a vertex """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        e12 = DirectedEdge(v1, v2)

        with self.assertRaises(VertexNotPartOfEdgeException):
            v0.add_edge(e12)


if __name__ == '__main__':
    unittest.main()
