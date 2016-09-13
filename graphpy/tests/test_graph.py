"""
Tests for graph.py
"""


from edge import UndirectedEdge, DirectedEdge
from vertex import UndirectedVertex, DirectedVertex
from graph import (UndirectedGraph, DirectedGraph, BadGraphInputException,
                   VertexNameAlreadyExistsException,
                   VertexAlreadyExistsException, EdgeAlreadyExistsException,
                   VertexAlreadyHasEdgesException)

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
        self.assertTrue(0 < g_half.num_edges < max_edges)
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
        """ Get the number of an undirected graph's vertices and edges """
        g = UndirectedGraph.from_dict({'v0': ['v1'],
                                       'v1': []})

        self.assertEqual(g.num_vertices, 2)
        self.assertEqual(g.num_edges, 1)
        with self.assertRaises(AttributeError):
            g.num_vertices = 0
        with self.assertRaises(AttributeError):
            g.num_edges = 0

    def test_undirected_graph_average_degree(self):
        """ Get the average degree of all vertices in an undirected graph """
        g = UndirectedGraph.from_dict({'v0': ['v1'],
                                       'v1': [],
                                       'v2': []})

        self.assertEqual(g.average_degree, 2.0 / 3.0)
        with self.assertRaises(AttributeError):
            g.average_degree = 0

    def test_undirected_graph_is_connected(self):
        """ Get whether a path exists for every pair of vertices in an
            undirected graph """
        g_connected = UndirectedGraph.from_dict({'v0': ['v1', 'v2'],
                                                 'v1': [],
                                                 'v2': []})
        g_disconnected = UndirectedGraph.from_dict({'v0': ['v1'],
                                                    'v1': [],
                                                    'v2': []})

        self.assertTrue(g_connected.is_connected)
        self.assertFalse(g_disconnected.is_connected)
        with self.assertRaises(AttributeError):
            g_connected.is_connected = False
        with self.assertRaises(AttributeError):
            g_disconnected.is_connected = True

    def test_undirected_graph_add_vertex(self):
        """ Add vertices to an undirected graph """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        g = UndirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)

        self.assertTrue(g.has_vertex(v0))
        self.assertTrue(g.has_vertex(v1))
        self.assertFalse(g.has_vertex(v2))

    def test_undirected_graph_add_edge(self):
        """ Add edges to an undirected graph """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        e01 = UndirectedEdge(v0, v1)
        e02 = UndirectedEdge(v0, v2)
        e10 = UndirectedEdge(v1, v0)
        g = UndirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_edge(v0, v1)

        self.assertTrue(g.has_edge(e01))
        self.assertFalse(g.has_edge(e02))
        self.assertTrue(g.has_edge(e10))

    def test_undirected_graph_remove_vertex(self):
        """ Remove vertices from an undirected graph """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        e01 = UndirectedEdge(v0, v1)
        e12 = UndirectedEdge(v1, v2)
        e10 = UndirectedEdge(v1, v0)
        g = UndirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_vertex(v2)
        g.add_edge(v0, v1)
        g.add_edge(v1, v2)

        g.remove_vertex(v0)

        self.assertFalse(g.has_vertex(v0))
        self.assertTrue(g.has_vertex(v1))
        self.assertTrue(g.has_vertex(v2))
        with self.assertRaises(KeyError):
            _ = g[v0.name]
        self.assertFalse(g.has_edge(e01))
        self.assertFalse(g.has_edge(e10))
        self.assertTrue(g.has_edge(e12))

        g.remove_vertex(v1)

        self.assertFalse(g.has_vertex(v0))
        self.assertFalse(g.has_vertex(v1))
        self.assertTrue(g.has_vertex(v2))
        with self.assertRaises(KeyError):
            _ = g[v1.name]
        self.assertFalse(g.has_edge(e01))
        self.assertFalse(g.has_edge(e10))
        self.assertFalse(g.has_edge(e12))

    def test_undirected_graph_remove_edge(self):
        """ Remove edges from an undirected graph """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        e01 = UndirectedEdge(v0, v1)
        e02 = UndirectedEdge(v0, v2)
        e10 = UndirectedEdge(v1, v0)
        g = UndirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_vertex(v2)
        g.add_edge(v0, v1)
        g.add_edge(v0, v2)

        g.remove_edge(v0, v1)

        self.assertFalse(g.has_edge(e01))
        self.assertFalse(g.has_edge(e10))
        self.assertTrue(g.has_edge(e02))

        g.remove_edge(v0, v2)

        self.assertFalse(g.has_edge(e01))
        self.assertFalse(g.has_edge(e10))
        self.assertFalse(g.has_edge(e02))

    def test_undirected_graph_search(self):
        """ Search for paths from an undirected vertex to all vertices reachable
            from it """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        v3 = UndirectedVertex(name='v3')
        v4 = UndirectedVertex(name='v4')
        g = UndirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_vertex(v2)
        g.add_vertex(v3)
        g.add_vertex(v4)
        g.add_edge(v0, v1)
        g.add_edge(v0, v2)
        g.add_edge(v1, v3)

        self.assertEqual(g.search(v0, goal=v0), [v0])
        self.assertEqual(g.search(v0, goal=v1), [v0, v1])
        self.assertEqual(g.search(v0, goal=v2), [v0, v2])
        self.assertEqual(g.search(v0, goal=v3), [v0, v1, v3])
        self.assertIsNone(g.search(v0, goal=v4))
        self.assertEqual(g.search(v0), {v0: [v0],
                                        v1: [v0, v1],
                                        v2: [v0, v2],
                                        v3: [v0, v1, v3]})
        self.assertEqual(g.search(v0, goal=v0, method='depth_first'), [v0])
        self.assertEqual(g.search(v0, goal=v1, method='depth_first'), [v0, v1])
        self.assertEqual(g.search(v0, goal=v2, method='depth_first'), [v0, v2])
        self.assertEqual(g.search(v0, goal=v3, method='depth_first'),
                         [v0, v1, v3])
        self.assertIsNone(g.search(v0, goal=v4, method='depth_first'))
        self.assertEqual(g.search(v0, method='depth_first'),
                         {v0: [v0],
                          v1: [v0, v1],
                          v2: [v0, v2],
                          v3: [v0, v1, v3]})

    def test_bad_undirected_graph_input(self):
        """ An undirected graph should not be able to be created from a
            dictionary with a value which is in a neighbor list but is not a
            vertex key """
        graph_dict = {'v0': ['v1', 'v2'],
                      'v1': []}

        with self.assertRaises(BadGraphInputException):
            _ = UndirectedGraph.from_dict(graph_dict)

    def test_undirected_graph_vertex_name_already_exists(self):
        """ An undirected graph should not be able to add a vertex with the same
            name as an existing vertex in the graph """
        g = UndirectedGraph.from_dict({'v0': []})

        with self.assertRaises(VertexNameAlreadyExistsException):
            g.add_vertex(UndirectedVertex(name='v0'))

    def test_undirected_graph_vertex_already_exists(self):
        """ An undirected graph should not be able to add a vertex that already
            exists in the graph """
        v0 = UndirectedVertex(name='v0')
        g = UndirectedGraph()
        g.add_vertex(v0)

        with self.assertRaises(VertexAlreadyExistsException):
            g.add_vertex(v0)

    def test_undirected_graph_edge_already_exists_exception(self):
        """ An undirected graph should not be able to add an edge that already
            exists in the graph """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        g = UndirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_edge(v0, v1)

        with self.assertRaises(EdgeAlreadyExistsException):
            g.add_edge(v0, v1)

    def test_undirected_graph_vertex_already_has_edges(self):
        """ An undirected graph should not be able to add a vertex that already
            contains edges """
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        e01 = UndirectedEdge(v0, v1)
        v0.add_edge(e01)
        g = UndirectedGraph()

        with self.assertRaises(VertexAlreadyHasEdgesException):
            g.add_vertex(v0)


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
        self.assertTrue(0 < g_half.num_edges < max_edges)
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
        """ Get the number of an undirected graph's vertices and edges """
        g = DirectedGraph.from_dict({'v0': ['v1'],
                                     'v1': []})

        self.assertEqual(g.num_vertices, 2)
        self.assertEqual(g.num_edges, 1)
        with self.assertRaises(AttributeError):
            g.num_vertices = 0
        with self.assertRaises(AttributeError):
            g.num_edges = 0

    def test_directed_graph_average_outs_and_average_ins(self):
        """ Get the average out degree and in degree of all vertices in a
            directed graph """
        g = DirectedGraph.from_dict({'v0': ['v1'],
                                     'v1': [],
                                     'v2': []})

        self.assertEqual(g.average_outs, 1.0 / 3.0)
        self.assertEqual(g.average_ins, 1.0 / 3.0)
        with self.assertRaises(AttributeError):
            g.average_outs = 0
        with self.assertRaises(AttributeError):
            g.average_ins = 0

    def test_directed_graph_is_weakly_connected(self):
        """ Get whether a path exists for every pair of vertices in a directed
            graph when treating its edges as undirected """
        g_connected = DirectedGraph.from_dict({'v0': ['v1', 'v2'],
                                               'v1': [],
                                               'v2': []})
        g_disconnected = DirectedGraph.from_dict({'v0': ['v1'],
                                                  'v1': [],
                                                  'v2': []})

        self.assertTrue(g_connected.is_weakly_connected)
        self.assertFalse(g_disconnected.is_weakly_connected)
        with self.assertRaises(AttributeError):
            g_connected.is_weakly_connected = False
        with self.assertRaises(AttributeError):
            g_disconnected.is_weakly_connected = True

    def test_directed_graph_is_strongly_connected(self):
        """ Get whether a path exists in both directions for every pair of
            vertices in a directed graph """
        g_connected = DirectedGraph.from_dict({'v0': ['v1'],
                                               'v1': ['v2'],
                                               'v2': ['v0']})
        g_disconnected = DirectedGraph.from_dict({'v0': ['v1', 'v2'],
                                                  'v1': [],
                                                  'v2': []})

        self.assertTrue(g_connected.is_strongly_connected)
        self.assertFalse(g_disconnected.is_strongly_connected)
        with self.assertRaises(AttributeError):
            g_connected.is_strongly_connected = False
        with self.assertRaises(AttributeError):
            g_disconnected.is_strongly_connected = True

    def test_directed_graph_add_vertex(self):
        """ Add vertices to a directed graph """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        g = DirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)

        self.assertTrue(g.has_vertex(v0))
        self.assertTrue(g.has_vertex(v1))
        self.assertFalse(g.has_vertex(v2))

    def test_directed_graph_add_edge(self):
        """ Add edges to a directed graph """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        e01 = DirectedEdge(v0, v1)
        e02 = DirectedEdge(v0, v2)
        e10 = DirectedEdge(v1, v0)
        g = DirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_edge(v0, v1)

        self.assertTrue(g.has_edge(e01))
        self.assertFalse(g.has_edge(e02))
        self.assertFalse(g.has_edge(e10))

    def test_directed_graph_remove_vertex(self):
        """ Remove vertices from a directed graph """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        e01 = DirectedEdge(v0, v1)
        e12 = DirectedEdge(v1, v2)
        e10 = DirectedEdge(v1, v0)
        g = DirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_vertex(v2)
        g.add_edge(v0, v1)
        g.add_edge(v1, v2)

        g.remove_vertex(v0)

        self.assertFalse(g.has_vertex(v0))
        self.assertTrue(g.has_vertex(v1))
        self.assertTrue(g.has_vertex(v2))
        with self.assertRaises(KeyError):
            _ = g[v0.name]
        self.assertFalse(g.has_edge(e01))
        self.assertFalse(g.has_edge(e10))
        self.assertTrue(g.has_edge(e12))

        g.remove_vertex(v1)

        self.assertFalse(g.has_vertex(v0))
        self.assertFalse(g.has_vertex(v1))
        self.assertTrue(g.has_vertex(v2))
        with self.assertRaises(KeyError):
            _ = g[v1.name]
        self.assertFalse(g.has_edge(e01))
        self.assertFalse(g.has_edge(e10))
        self.assertFalse(g.has_edge(e12))

    def test_directed_graph_remove_edge(self):
        """ Remove edges from a directed graph """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        e01 = DirectedEdge(v0, v1)
        e02 = DirectedEdge(v0, v2)
        e10 = DirectedEdge(v1, v0)
        g = DirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_vertex(v2)
        g.add_edge(v0, v1)
        g.add_edge(v0, v2)

        g.remove_edge(v0, v1)

        self.assertFalse(g.has_edge(e01))
        self.assertFalse(g.has_edge(e10))
        self.assertTrue(g.has_edge(e02))

        g.remove_edge(v0, v2)

        self.assertFalse(g.has_edge(e01))
        self.assertFalse(g.has_edge(e10))
        self.assertFalse(g.has_edge(e02))

    def test_directed_graph_search(self):
        """ Search for paths from a directed vertex to all vertices reachable
            from it """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        v3 = DirectedVertex(name='v3')
        v4 = DirectedVertex(name='v4')
        g = DirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_vertex(v2)
        g.add_vertex(v3)
        g.add_vertex(v4)
        g.add_edge(v0, v0)
        g.add_edge(v0, v1)
        g.add_edge(v2, v0)
        g.add_edge(v1, v3)

        self.assertEqual(g.search(v0, goal=v0), [v0])
        self.assertEqual(g.search(v0, goal=v1), [v0, v1])
        self.assertIsNone(g.search(v0, goal=v2))
        self.assertEqual(g.search(v0, goal=v3), [v0, v1, v3])
        self.assertIsNone(g.search(v0, goal=v4))
        self.assertEqual(g.search(v0), {v0: [v0],
                                        v1: [v0, v1],
                                        v3: [v0, v1, v3]})
        self.assertEqual(g.search(v0, goal=v0, method='depth_first'), [v0])
        self.assertEqual(g.search(v0, goal=v1, method='depth_first'), [v0, v1])
        self.assertIsNone(g.search(v0, goal=v2, method='depth_first'))
        self.assertEqual(g.search(v0, goal=v3, method='depth_first'),
                         [v0, v1, v3])
        self.assertIsNone(g.search(v0, goal=v4, method='depth_first'))
        self.assertEqual(g.search(v0, method='depth_first'),
                         {v0: [v0],
                          v1: [v0, v1],
                          v3: [v0, v1, v3]})

    def test_directed_graph_vertex_name_already_exists(self):
        """ A directed graph should not be able to add a vertex with the same
            name as an existing vertex in the graph """
        g = DirectedGraph.from_dict({'v0': []})

        with self.assertRaises(VertexNameAlreadyExistsException):
            g.add_vertex(DirectedVertex(name='v0'))

    def test_directed_graph_vertex_already_exists(self):
        """ A directed graph should not be able to add a vertex that already
            exists in the graph """
        v0 = DirectedVertex(name='v0')
        g = DirectedGraph()
        g.add_vertex(v0)

        with self.assertRaises(VertexAlreadyExistsException):
            g.add_vertex(v0)

    def test_directed_graph_edge_already_exists_exception(self):
        """ A directed graph should not be able to add an edge that already
            exists in the graph """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        g = DirectedGraph()
        g.add_vertex(v0)
        g.add_vertex(v1)
        g.add_edge(v0, v1)

        with self.assertRaises(EdgeAlreadyExistsException):
            g.add_edge(v0, v1)

    def test_directed_graph_vertex_already_has_edges(self):
        """ A directed graph should not be able to add a vertex that already
            contains edges """
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        e01 = DirectedEdge(v0, v1)
        v0.add_edge(e01)
        g = DirectedGraph()

        with self.assertRaises(VertexAlreadyHasEdgesException):
            g.add_vertex(v0)


def n_choose_2(n):
    return n * (n - 1) / 2.0


if __name__ == '__main__':
    unittest.main()
