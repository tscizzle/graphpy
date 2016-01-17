"""
Tests for graph.py
"""


from graph import UndirectedGraph, DirectedGraph

import unittest


class TestUndirectedGraph(unittest.TestCase):

    def test_create_undirected_graph_from_dict(self):
        graph_dict = {'v0': ['v1', 'v2'],
                      'v1': ['v0', 'v3'],
                      'v2': [],
                      'v3': []}
        g = UndirectedGraph.from_dict(graph_dict)
        print g

        self.assertEqual(g.num_vertices(), 4)
        self.assertEqual(g.num_edges(), 3)
        print g

    def test_create_undirected_graph_from_directed_graph(self):
        pass

    def test_create_random_undirected_graph(self):
        pass

    def test_create_complete_undirected_graph(self):
        pass

    def test_undirected_graph_get_and_set_vertices_and_edges(self):
        g = UndirectedGraph()

        with self.assertRaises(AttributeError):
            g.vertices = set()
        with self.assertRaises(AttributeError):
            g.edges = set()
        try:
            _ = g.vertices
            _ = g.edges
        except:
            self.fail("We should be able to get the properties 'vertices' and "
                      "'edges' even though we can't set them.")


class TestDirectedGraph(unittest.TestCase):

    def test_create_directed_graph_from_dict(self):
        pass

    def test_create_undirected_graph_from_transpose(self):
        pass

    def test_create_random_directed_graph(self):
        pass

    def test_create_complete_directed_graph(self):
        pass


if __name__ == '__main__':
    unittest.main()
