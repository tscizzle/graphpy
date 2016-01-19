"""
Tests for graph.py
"""


from edge import UndirectedEdge, DirectedEdge
from vertex import UndirectedVertex, DirectedVertex
from graph import UndirectedGraph, DirectedGraph

import unittest


class TestUndirectedGraph(unittest.TestCase):

    def test_undirected_graph_indexing(self):
        """ Index an undirected graph by vertex name """
        v0 = UndirectedVertex(name='v0')
        g = UndirectedGraph()
        g.add_vertex(v0)

        self.assertEqual(g['v0'], v0)
        with self.assertRaises(TypeError):
            _ = g[v0]
        with self.assertRaises(KeyError):
            _ = g['v1']

    def test_create_undirected_graph_from_dict(self):
        """ Create an undirected graph from an adjacency dictionary """
        graph_dict = {'v0': ['v1', 'v2'],
                      'v1': ['v0', 'v3'],
                      'v2': [],
                      'v3': [],
                      'v4': []}
        g = UndirectedGraph.from_dict(graph_dict)

        self.assertEqual(g.num_vertices, 5)
        self.assertEqual(g.num_edges, 3)
        self.assertEqual(g['v0'].neighbors, set([g['v1'], g['v2']]))
        self.assertEqual(g['v1'].neighbors, set([g['v0'], g['v3']]))
        self.assertEqual(g['v2'].neighbors, set([g['v0']]))
        self.assertEqual(g['v3'].neighbors, set([g['v1']]))
        self.assertEqual(g['v4'].neighbors, set())

    def test_create_undirected_graph_from_directed_graph(self):
        """ Create an undirected graph from a directed graph """
        graph_dict = {'v0': ['v1', 'v2'],
                      'v1': ['v0', 'v3'],
                      'v2': [],
                      'v3': ['v1'],
                      'v4': []}
        dg = DirectedGraph.from_dict(graph_dict)
        g = UndirectedGraph.from_directed_graph(dg)

        self.assertEqual(g.num_vertices, 5)
        self.assertEqual(g.num_edges, 3)

    def test_create_random_undirected_graph(self):
        """ Create an undirected graph with edges between random nodes """
        num_vertices = 10
        v_names = ['v' + str(i) for i in xrange(num_vertices)]
        g_half = UndirectedGraph.random_graph(v_names, 0.5)
        g_zero = UndirectedGraph.random_graph(v_names, 0.0)
        g_one = UndirectedGraph.random_graph(v_names, 1.0)

        max_edges = n_choose_2(num_vertices)
        self.assertEqual(g_half.num_vertices, num_vertices)
        self.assertEqual(g_zero.num_vertices, num_vertices)
        self.assertEqual(g_one.num_vertices, num_vertices)
        self.assertTrue((max_edges / 2.0) - 7 <= g_half.num_edges <=
                        (max_edges / 2.0) + 10)
        self.assertEqual(g_zero.num_edges, 0)
        self.assertEqual(g_one.num_edges, max_edges)

    def test_create_complete_undirected_graph(self):
        """ Create an undirected graph with edges between all nodes """
        num_vertices = 10
        v_names = ['v' + str(i) for i in xrange(num_vertices)]
        g = UndirectedGraph.complete_graph(v_names)

        max_edges = n_choose_2(num_vertices)
        self.assertEqual(g.num_vertices, num_vertices)
        self.assertEqual(g.num_edges, max_edges)

    def test_undirected_graph_vertices_and_edges(self):
        """ Get undirected graphs' vertices and edges properties """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        e01 = UndirectedEdge(v0, v1)
        g = UndirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_edge(v0, v1)

        self.assertEqual(g.vertices, set([v0, v1]))
        self.assertEqual(g.edges, set([e01]))
        with self.assertRaises(AttributeError):
            g.vertices = set()
        with self.assertRaises(AttributeError):
            g.edges = set()

    def test_undirected_graph_num_vertices_and_num_edges(self):
        """ Get undirected graphs' num_vertices and num_edges properties """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        g = UndirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_edge(v0, v1)

        self.assertEqual(g.num_vertices, 2)
        self.assertEqual(g.num_edges, 1)
        with self.assertRaises(AttributeError):
            g.num_vertices = 0
        with self.assertRaises(AttributeError):
            g.num_edges = 0

    ## TODO: test the rest of the methods


class TestDirectedGraph(unittest.TestCase):

    def test_directed_graph_indexing(self):
        """ Index a directed graph by vertex name """
        v0 = DirectedVertex(name='v0')
        g = DirectedGraph()
        g.add_vertex(v0)

        self.assertEqual(g['v0'], v0)
        with self.assertRaises(TypeError):
            _ = g[v0]
        with self.assertRaises(KeyError):
            _ = g['v1']

    def test_create_directed_graph_from_dict(self):
        """ Create a directed graph from an adjacency dictionary """
        graph_dict = {'v0': ['v1', 'v2'],
                      'v1': ['v0', 'v3'],
                      'v2': [],
                      'v3': [],
                      'v4': []}
        g = DirectedGraph.from_dict(graph_dict)

        self.assertEqual(g.num_vertices, 5)
        self.assertEqual(g.num_edges, 4)
        self.assertEqual(g['v0'].outs, set([g['v1'], g['v2']]))
        self.assertEqual(g['v1'].outs, set([g['v0'], g['v3']]))
        self.assertEqual(g['v2'].outs, set())
        self.assertEqual(g['v3'].outs, set())
        self.assertEqual(g['v4'].outs, set())
        self.assertEqual(g['v0'].ins, set([g['v1']]))
        self.assertEqual(g['v1'].ins, set([g['v0']]))
        self.assertEqual(g['v2'].ins, set([g['v0']]))
        self.assertEqual(g['v3'].ins, set([g['v1']]))
        self.assertEqual(g['v4'].ins, set())

    def test_create_directed_graph_from_transpose(self):
        """ Create a directed graph by reversing the edges of an input graph """
        graph_dict = {'v0': ['v1', 'v2'],
                      'v1': ['v0', 'v3'],
                      'v2': [],
                      'v3': [],
                      'v4': []}
        tg = DirectedGraph.from_dict(graph_dict)
        g = DirectedGraph.from_transpose(tg)

        self.assertEqual(g.num_vertices, 5)
        self.assertEqual(g.num_edges, 4)
        self.assertEqual(g['v0'].outs, set([g['v1']]))
        self.assertEqual(g['v1'].outs, set([g['v0']]))
        self.assertEqual(g['v2'].outs, set([g['v0']]))
        self.assertEqual(g['v3'].outs, set([g['v1']]))
        self.assertEqual(g['v4'].outs, set())
        self.assertEqual(g['v0'].ins, set([g['v1'], g['v2']]))
        self.assertEqual(g['v1'].ins, set([g['v0'], g['v3']]))
        self.assertEqual(g['v2'].ins, set())
        self.assertEqual(g['v3'].ins, set())
        self.assertEqual(g['v4'].ins, set())

    def test_create_random_directed_graph(self):
        """ Create a directed graph with edges between random nodes """
        num_vertices = 10
        v_names = ['v' + str(i) for i in xrange(num_vertices)]
        g_half = DirectedGraph.random_graph(v_names, 0.5)
        g_zero = DirectedGraph.random_graph(v_names, 0.0)
        g_one = DirectedGraph.random_graph(v_names, 1.0)

        max_edges = num_vertices ** 2
        self.assertEqual(g_half.num_vertices, num_vertices)
        self.assertEqual(g_zero.num_vertices, num_vertices)
        self.assertEqual(g_one.num_vertices, num_vertices)
        self.assertTrue((max_edges / 2.0) - 10 <= g_half.num_edges <=
                        (max_edges / 2.0) + 10)
        self.assertEqual(g_zero.num_edges, 0)
        self.assertEqual(g_one.num_edges, max_edges)

    def test_create_complete_directed_graph(self):
        """ Create a directed graph with edges between all nodes """
        num_vertices = 10
        v_names = ['v' + str(i) for i in xrange(num_vertices)]
        g = DirectedGraph.complete_graph(v_names)

        max_edges = num_vertices ** 2
        self.assertEqual(g.num_vertices, num_vertices)
        self.assertEqual(g.num_edges, max_edges)

    def test_directed_graph_vertices_and_edges(self):
        """ Get directed graphs' vertices and edges properties """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        e01 = DirectedEdge(v0, v1)
        g = DirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_edge(v0, v1)

        self.assertEqual(g.vertices, set([v0, v1]))
        self.assertEqual(g.edges, set([e01]))
        with self.assertRaises(AttributeError):
            g.vertices = set()
        with self.assertRaises(AttributeError):
            g.edges = set()

    def test_directed_graph_num_vertices_and_num_edges(self):
        """ Get directed graphs' num_vertices and num_edges properties """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        g = DirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_edge(v0, v1)

        self.assertEqual(g.num_vertices, 2)
        self.assertEqual(g.num_edges, 1)
        with self.assertRaises(AttributeError):
            g.num_vertices = 0
        with self.assertRaises(AttributeError):
            g.num_edges = 0

    ## TODO: test the rest of the methods


def n_choose_2(n):
    return n * (n - 1) / 2.0


if __name__ == '__main__':
    unittest.main()
