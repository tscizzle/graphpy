"""
Tests for graph.py
"""


from graphpy.graph import (UndirectedGraph, DirectedGraph,
                           BadGraphInputException,
                           VertexAlreadyExistsException,
                           EdgeAlreadyExistsException)

import unittest


################################################################################
#                                                                              #
#                                  Undirected                                  #
#                                                                              #
################################################################################


class TestUndirectedGraph(unittest.TestCase):

    def test_undirected_graph_length(self):
        """ Get the length of an undirected graph """
        g = UndirectedGraph()

        self.assertEqual(len(g), 0)

        g.add_vertex(v_val='v0')

        self.assertEqual(len(g), 1)

        g.add_vertex(v_val='v1')
        g.add_edge(('v0', 'v1'))

        self.assertEqual(len(g), 2)

        g.remove_vertex('v0')

        self.assertEqual(len(g), 1)

    def test_undirected_graph_iteration(self):
        """ Iterate through an undirected graph """
        g = UndirectedGraph()

        counter = 0
        for v in g:
            counter += 1
        self.assertEqual(counter, 0)

        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_edge(('v0', 'v1'))

        for v in g:
            counter += 1
            self.assertTrue(g.has_vertex(v.val))
        self.assertEqual(counter, 2)

    def test_create_undirected_graph_from_lists(self):
        """ Create an undirected graph from lists of vertices and edges """
        vertices = [('v0', {'city': 'Paris'}),
                    (1, {'continent': 'Europe', 'city': 'London'}),
                    ((2, 2),),
                    ('v3',),
                    ('v4',)]
        edges = [(('v0', 1), {'weight': 3}),
                 (('v0', (2, 2)), {'weight': 4}),
                 ((1, 'v3'),)]
        g = UndirectedGraph.from_lists(vertices, edges)

        v0 = g.get_vertex('v0')
        v1 = g.get_vertex(1)
        v2 = g.get_vertex((2, 2))
        v3 = g.get_vertex('v3')
        v4 = g.get_vertex('v4')
        e01 = g.get_edge(('v0', 1))
        e02 = g.get_edge(('v0', (2, 2)))
        e13 = g.get_edge((1, 'v3'))
        self.assertEqual(g.num_vertices, 5)
        self.assertEqual(g.num_edges, 3)
        self.assertEqual(set(v0.neighbors), set([v1, v2]))
        self.assertEqual(set(v1.neighbors), set([v0, v3]))
        self.assertEqual(set(v2.neighbors), set([v0]))
        self.assertEqual(set(v3.neighbors), set([v1]))
        self.assertEqual(set(v4.neighbors), set())
        self.assertEqual(v0.get('city'), 'Paris')
        self.assertEqual(v1.get('continent'), 'Europe')
        self.assertEqual(v1.get('city'), 'London')
        self.assertIsNone(v2.get('city'))
        self.assertEqual(e01.get('weight'), 3)
        self.assertEqual(e02.get('weight'), 4)
        self.assertIsNone(e13.get('weight'))

        duplicate_vertices = [('v0_dupe',), ('v0_dupe',)]
        with self.assertRaises(VertexAlreadyExistsException):
            _ = UndirectedGraph.from_lists(duplicate_vertices, [])

        vertices_dupe_edge = [('v0_dupe_edge',), ('v1_dupe_edge',)]
        duplicate_edges = [(('v0_dupe_edge', 'v1_dupe_edge'),),
                           (('v1_dupe_edge', 'v0_dupe_edge'),)]
        with self.assertRaises(EdgeAlreadyExistsException):
            _ = UndirectedGraph.from_lists(vertices_dupe_edge, duplicate_edges)

    def test_create_undirected_graph_from_dict(self):
        """ Create an undirected graph from an adjacency dictionary """
        graph_dict = {'v0': [(1,), (1,), ((2, 2), {'weight': 5})],
                      1: [('v0',), ('v3',)],
                      (2, 2): [],
                      'v3': [],
                      'v4': []}
        vertex_attrs = {'v0': {'city': 'Paris'},
                        1: {'continent': 'Europe', 'city': 'London'},
                        'v5': {'city': 'Jamestown'}}
        g = UndirectedGraph.from_dict(graph_dict, vertex_attrs=vertex_attrs)

        v0 = g.get_vertex('v0')
        v1 = g.get_vertex(1)
        v2 = g.get_vertex((2, 2))
        v3 = g.get_vertex('v3')
        v4 = g.get_vertex('v4')
        v5 = g.get_vertex('v5')
        e01 = g.get_edge(('v0', 1))
        e02 = g.get_edge(('v0', (2, 2)))
        e13 = g.get_edge((1, 'v3'))
        self.assertEqual(g.num_vertices, 6)
        self.assertEqual(g.num_edges, 3)
        self.assertEqual(set(v0.neighbors), set([v1, v2]))
        self.assertEqual(set(v1.neighbors), set([v0, v3]))
        self.assertEqual(set(v2.neighbors), set([v0]))
        self.assertEqual(set(v3.neighbors), set([v1]))
        self.assertEqual(set(v4.neighbors), set())
        self.assertEqual(set(v5.neighbors), set())
        self.assertEqual(v0.get('city'), 'Paris')
        self.assertEqual(v1.get('continent'), 'Europe')
        self.assertEqual(v1.get('city'), 'London')
        self.assertEqual(v5.get('city'), 'Jamestown')
        self.assertIsNone(v2.get('city'))
        self.assertIsNone(e01.get('weight'))
        self.assertEqual(e02.get('weight'), 5)
        self.assertIsNone(e13.get('weight'))
        with self.assertRaises(BadGraphInputException):
            _ = UndirectedGraph.from_dict({'v0': [({'weight': 5},)],
                                           'v1': [({'weight': 3},)]})

    def test_create_undirected_graph_from_directed_graph(self):
        """ Create an undirected graph from a directed graph """
        graph_dict = {'v0': [('v0',), ('v1',), ('v2',)],
                      'v1': [('v0',), ('v3',)],
                      'v2': [],
                      'v3': [('v1',)],
                      'v4': []}
        dg = DirectedGraph.from_dict(graph_dict)
        g = UndirectedGraph.from_directed_graph(dg)

        self.assertEqual(g.num_vertices, 5)
        self.assertEqual(g.num_edges, 4)

    def test_create_random_undirected_graph(self):
        """ Create an undirected graph with edges between random nodes """
        num_vertices = 10
        v_vals = ['v' + str(i) for i in xrange(num_vertices)]
        g_half = UndirectedGraph.random_graph(v_vals, 0.5)
        g_zero = UndirectedGraph.random_graph(v_vals, 0.0)
        g_one = UndirectedGraph.random_graph(v_vals, 1.0)

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
        v_vals = ['v' + str(i) for i in xrange(num_vertices)]
        g = UndirectedGraph.complete_graph(v_vals)

        max_edges = n_choose_2(num_vertices)
        self.assertEqual(g.num_vertices, num_vertices)
        self.assertEqual(g.num_edges, max_edges)

    def test_undirected_graph_vertices_and_edges(self):
        """ Get undirected graphs' vertices and edges properties """
        g = UndirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_edge(('v0', 'v1'))

        v0 = g.get_vertex('v0')
        v1 = g.get_vertex('v1')
        e01 = g.get_edge(('v0', 'v1'))
        self.assertEqual(set(g.vertices), set([v0, v1]))
        self.assertEqual(set(g.edges), set([e01]))
        with self.assertRaises(AttributeError):
            g.vertices = set()
        with self.assertRaises(AttributeError):
            g.edges = set()

    def test_undirected_graph_num_vertices_and_num_edges(self):
        """ Get the number of an undirected graph's vertices and edges """
        g = UndirectedGraph.from_dict({'v0': [('v1',)],
                                       'v1': []})

        self.assertEqual(g.num_vertices, 2)
        self.assertEqual(g.num_edges, 1)
        with self.assertRaises(AttributeError):
            g.num_vertices = 0
        with self.assertRaises(AttributeError):
            g.num_edges = 0

    def test_undirected_graph_average_degree(self):
        """ Get the average degree of all vertices in an undirected graph """
        g = UndirectedGraph.from_dict({'v0': [('v1',)],
                                       'v1': [],
                                       'v2': []})
        empty_g = UndirectedGraph()

        self.assertEqual(g.average_degree, 2.0 / 3.0)
        with self.assertRaises(AttributeError):
            g.average_degree = 0
        self.assertEqual(empty_g.average_degree, 0)

    def test_undirected_graph_is_connected(self):
        """ Get whether a path exists for every pair of vertices in an
            undirected graph """
        g_connected = UndirectedGraph.from_dict({'v0': [('v1',), ('v2',)],
                                                 'v1': [],
                                                 'v2': []})
        g_disconnected = UndirectedGraph.from_dict({'v0': [('v1',)],
                                                    'v1': [],
                                                    'v2': []})

        self.assertTrue(g_connected.is_connected)
        self.assertFalse(g_disconnected.is_connected)
        with self.assertRaises(AttributeError):
            g_connected.is_connected = False
        with self.assertRaises(AttributeError):
            g_disconnected.is_connected = True

    def test_undirected_graph_clone(self):
        """ Clone an undirected graph """
        vertices = [('v0', {'city': 'Paris'}),
                    ('v1', {'continent': 'Europe', 'city': 'London'}),
                    ('v2',),
                    ('v3',),
                    ('v4',)]
        edges = [(('v0', 'v1'), {'weight': 3}),
                 (('v0', 'v2'), {'weight': 4}),
                 (('v1', 'v3'),)]
        g = UndirectedGraph.from_lists(vertices, edges)

        g_prime = g.clone()

        v0 = g.get_vertex('v0')
        v0_prime = g_prime.get_vertex('v0')
        e01 = g.get_edge(('v0', 'v1'))
        e01_prime = g_prime.get_edge(('v0', 'v1'))
        self.assertEqual(g_prime.num_vertices, g.num_vertices)
        self.assertEqual(g_prime.num_edges, g.num_edges)
        self.assertNotEqual(v0, v0_prime)
        self.assertNotEqual(e01, e01_prime)
        self.assertEqual(v0.attrs, v0_prime.attrs)

        g.add_vertex('v5', {'city': 'Jamestown'})

        self.assertTrue(g.has_vertex('v5'))
        self.assertFalse(g_prime.has_vertex('v5'))

        g.remove_vertex('v0')

        self.assertFalse(g.has_vertex('v0'))
        self.assertTrue(g_prime.has_vertex('v0'))
        self.assertFalse(g.has_edge(('v0', 'v1')))
        self.assertTrue(g_prime.has_edge(('v0', 'v1')))

        e01.set('weight', 5)

        self.assertEqual(e01.get('weight'), 5)
        self.assertEqual(e01_prime.get('weight'), 3)

    def test_undirected_graph_add_vertex(self):
        """ Add vertices to an undirected graph """
        g = UndirectedGraph()
        v0_val = g.add_vertex(v_val='v0', attrs={'city': 'Modena'})
        v1_val = g.add_vertex(v_val='v1')

        self.assertEqual(v0_val, 'v0')
        self.assertEqual(v1_val, 'v1')
        self.assertTrue(g.has_vertex('v0'))
        self.assertTrue(g.has_vertex('v1'))
        self.assertFalse(g.has_vertex('v2'))
        self.assertEqual(g.get_vertex(v0_val).get('city'), 'Modena')
        self.assertIsNone(g.get_vertex(v1_val).get('city'))

    def test_undirected_graph_add_edge(self):
        """ Add edges to an undirected graph """
        g = UndirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_edge(('v0', 'v0'), attrs={'weight': 5})
        g.add_edge(('v0', 'v1'), attrs={'weight': 7})

        e00 = g.get_edge(('v0', 'v0'))
        e01 = g.get_edge(('v0', 'v1'))
        self.assertTrue(g.has_edge(('v0', 'v0')))
        self.assertTrue(g.has_edge(('v0', 'v1')))
        self.assertFalse(g.has_edge(('v0', 'v2')))
        self.assertTrue(g.has_edge(('v1', 'v0')))
        self.assertEqual(e00.get('weight'), 5)
        self.assertEqual(e01.get('weight'), 7)

    def test_undirected_graph_remove_vertex(self):
        """ Remove vertices from an undirected graph """
        g = UndirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_vertex(v_val='v2')
        g.add_edge(('v0', 'v1'))
        g.add_edge(('v1', 'v2'))

        g.remove_vertex('v0')

        self.assertFalse(g.has_vertex('v0'))
        self.assertTrue(g.has_vertex('v1'))
        self.assertTrue(g.has_vertex('v2'))
        self.assertFalse(g.has_edge(('v0', 'v1')))
        self.assertFalse(g.has_edge(('v1', 'v0')))
        self.assertTrue(g.has_edge(('v1', 'v2')))

        g.remove_vertex('v1')

        self.assertFalse(g.has_vertex('v0'))
        self.assertFalse(g.has_vertex('v1'))
        self.assertTrue(g.has_vertex('v2'))
        self.assertFalse(g.has_edge(('v0', 'v1')))
        self.assertFalse(g.has_edge(('v1', 'v0')))
        self.assertFalse(g.has_edge(('v1', 'v2')))

    def test_undirected_graph_remove_edge(self):
        """ Remove edges from an undirected graph """
        g = UndirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_vertex(v_val='v2')
        g.add_edge(('v0', 'v1'))
        g.add_edge(('v0', 'v2'))

        g.remove_edge(('v0', 'v1'))

        self.assertFalse(g.has_edge(('v0', 'v1')))
        self.assertFalse(g.has_edge(('v1', 'v0')))
        self.assertTrue(g.has_edge(('v0', 'v2')))

        g.remove_edge(('v0', 'v2'))

        self.assertFalse(g.has_edge(('v0', 'v1')))
        self.assertFalse(g.has_edge(('v1', 'v0')))
        self.assertFalse(g.has_edge(('v0', 'v2')))

    def test_undirected_graph_search(self):
        """ Search for paths from an undirected vertex to all vertices reachable
            from it """
        g = UndirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_vertex(v_val='v2')
        g.add_vertex(v_val='v3')
        g.add_vertex(v_val='v4')
        g.add_edge(('v0', 'v0'))
        g.add_edge(('v0', 'v1'))
        g.add_edge(('v0', 'v2'))
        g.add_edge(('v1', 'v3'))

        self.assertEqual(g.search('v0', goal_val='v0'), ['v0'])
        self.assertEqual(g.search('v0', goal_val='v1'), ['v0', 'v1'])
        self.assertEqual(g.search('v0', goal_val='v2'), ['v0', 'v2'])
        self.assertEqual(g.search('v0', goal_val='v3'),
                         ['v0', 'v1', 'v3'])
        self.assertIsNone(g.search('v0', goal_val='v4'))
        self.assertEqual(g.search('v0'), {'v0': ['v0'],
                                          'v1': ['v0', 'v1'],
                                          'v2': ['v0', 'v2'],
                                          'v3': ['v0', 'v1', 'v3']})
        self.assertEqual(g.search('v0', goal_val='v0', method='depth_first'),
                         ['v0'])
        self.assertEqual(g.search('v0', goal_val='v1', method='depth_first'),
                         ['v0', 'v1'])
        self.assertEqual(g.search('v0', goal_val='v2', method='depth_first'),
                         ['v0', 'v2'])
        self.assertEqual(g.search('v0', goal_val='v3', method='depth_first'),
                         ['v0', 'v1', 'v3'])
        self.assertIsNone(g.search('v0', goal_val='v4', method='depth_first'))
        self.assertEqual(g.search('v0', method='depth_first'),
                         {'v0': ['v0'],
                          'v1': ['v0', 'v1'],
                          'v2': ['v0', 'v2'],
                          'v3': ['v0', 'v1', 'v3']})

    def test_bad_undirected_graph_input(self):
        """ An undirected graph from_dict input must be of a certain form """
        graph_dict = {'v0': ['v1', {'weight': 3}],
                      'v1': [],
                      'v2': []}

        with self.assertRaises(BadGraphInputException):
            _ = UndirectedGraph.from_dict(graph_dict)

    def test_undirected_graph_vertex_already_exists(self):
        """ An undirected graph should not be able to add a vertex that already
            exists in the graph """
        g = UndirectedGraph()
        g.add_vertex(v_val='v0')

        with self.assertRaises(VertexAlreadyExistsException):
            g.add_vertex(v_val='v0')

    def test_undirected_graph_edge_already_exists_exception(self):
        """ An undirected graph should not be able to add an edge that already
            exists in the graph """
        g = UndirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_edge(('v0', 'v1'))

        with self.assertRaises(EdgeAlreadyExistsException):
            g.add_edge(('v1', 'v0'))


################################################################################
#                                                                              #
#                                   Directed                                   #
#                                                                              #
################################################################################


class TestDirectedGraph(unittest.TestCase):

    def test_directed_graph_length(self):
        """ Get the length of a directed graph """
        g = DirectedGraph()

        self.assertEqual(len(g), 0)

        g.add_vertex(v_val='v0')

        self.assertEqual(len(g), 1)

        g.add_vertex(v_val='v1')
        g.add_edge(('v0', 'v1'))

        self.assertEqual(len(g), 2)

        g.remove_vertex('v0')

        self.assertEqual(len(g), 1)

    def test_directed_graph_iteration(self):
        """ Iterate through a directed graph """
        g = DirectedGraph()

        counter = 0
        for v in g:
            counter += 1
        self.assertEqual(counter, 0)

        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_edge(('v0', 'v1'))

        for v in g:
            counter += 1
            self.assertTrue(g.has_vertex(v.val))
        self.assertEqual(counter, 2)

    def test_create_directed_graph_from_lists(self):
        """ Create a directed graph from lists of vertices and edges """
        vertices = [('v0', {'city': 'Paris'}),
                    (1, {'continent': 'Europe', 'city': 'London'}),
                    ((2, 2),),
                    ('v3',),
                    ('v4',)]
        edges = [(('v0', 1), {'weight': 3}),
                 (('v0', (2, 2)), {'weight': 4}),
                 ((1, 'v3'),),
                 ((1, 'v0'), {'weight': 5})]
        g = DirectedGraph.from_lists(vertices, edges)

        v0 = g.get_vertex('v0')
        v1 = g.get_vertex(1)
        v2 = g.get_vertex((2, 2))
        v3 = g.get_vertex('v3')
        v4 = g.get_vertex('v4')
        e01 = g.get_edge(('v0', 1))
        e02 = g.get_edge(('v0', (2, 2)))
        e13 = g.get_edge((1, 'v3'))
        e10 = g.get_edge((1, 'v0'))
        self.assertEqual(g.num_vertices, 5)
        self.assertEqual(g.num_edges, 4)
        self.assertEqual(set(v0.outs), set([v1, v2]))
        self.assertEqual(set(v1.outs), set([v0, v3]))
        self.assertEqual(set(v2.outs), set())
        self.assertEqual(set(v3.outs), set())
        self.assertEqual(set(v4.outs), set())
        self.assertEqual(set(v0.ins), set([v1]))
        self.assertEqual(set(v1.ins), set([v0]))
        self.assertEqual(set(v2.ins), set([v0]))
        self.assertEqual(set(v3.ins), set([v1]))
        self.assertEqual(set(v4.ins), set())
        self.assertEqual(v0.get('city'), 'Paris')
        self.assertEqual(v1.get('continent'), 'Europe')
        self.assertEqual(v1.get('city'), 'London')
        self.assertIsNone(v2.get('city'))
        self.assertEqual(e01.get('weight'), 3)
        self.assertEqual(e02.get('weight'), 4)
        self.assertIsNone(e13.get('weight'))
        self.assertEqual(e10.get('weight'), 5)

        duplicate_vertices = [('v0_dupe',), ('v0_dupe',)]
        with self.assertRaises(VertexAlreadyExistsException):
            _ = DirectedGraph.from_lists(duplicate_vertices, [])

        vertices_dupe_edge = [('v0_dupe_edge',), ('v1_dupe_edge',)]
        duplicate_edges = [(('v0_dupe_edge', 'v1_dupe_edge'),),
                           (('v0_dupe_edge', 'v1_dupe_edge'),)]
        with self.assertRaises(EdgeAlreadyExistsException):
            _ = DirectedGraph.from_lists(vertices_dupe_edge, duplicate_edges)

    def test_create_directed_graph_from_dict(self):
        """ Create a directed graph from an adjacency dictionary """
        graph_dict = {'v0': [(1,), (1,), ((2, 2), {'weight': 5})],
                      1: [('v0',), ('v3',)],
                      (2, 2): [],
                      'v3': [],
                      'v4': []}
        vertex_attrs = {'v0': {'city': 'Paris'},
                        1: {'continent': 'Europe', 'city': 'London'},
                        'v5': {'city': 'Jamestown'}}
        g = DirectedGraph.from_dict(graph_dict, vertex_attrs=vertex_attrs)

        v0 = g.get_vertex('v0')
        v1 = g.get_vertex(1)
        v2 = g.get_vertex((2, 2))
        v3 = g.get_vertex('v3')
        v4 = g.get_vertex('v4')
        v5 = g.get_vertex('v5')
        e01 = g.get_edge(('v0', 1))
        e02 = g.get_edge(('v0', (2, 2)))
        self.assertEqual(g.num_vertices, 6)
        self.assertEqual(g.num_edges, 4)
        self.assertEqual(set(v0.outs), set([v1, v2]))
        self.assertEqual(set(v1.outs), set([v0, v3]))
        self.assertEqual(set(v2.outs), set())
        self.assertEqual(set(v3.outs), set())
        self.assertEqual(set(v4.outs), set())
        self.assertEqual(set(v0.ins), set([v1]))
        self.assertEqual(set(v1.ins), set([v0]))
        self.assertEqual(set(v2.ins), set([v0]))
        self.assertEqual(set(v3.ins), set([v1]))
        self.assertEqual(set(v4.ins), set())
        self.assertEqual(v0.get('city'), 'Paris')
        self.assertEqual(v1.get('continent'), 'Europe')
        self.assertEqual(v1.get('city'), 'London')
        self.assertEqual(v5.get('city'), 'Jamestown')
        self.assertIsNone(v2.get('city'))
        self.assertIsNone(e01.get('weight'))
        self.assertEqual(e02.get('weight'), 5)
        with self.assertRaises(BadGraphInputException):
            _ = DirectedGraph.from_dict({'v0': [({'weight': 5},)],
                                         'v1': [({'weight': 3},)]})

    def test_create_directed_graph_from_transpose(self):
        """ Create a directed graph by reversing the edges of an input graph """
        graph_dict = {'v0': [('v1',), ('v2',)],
                      'v1': [('v0',), ('v3',)],
                      'v2': [],
                      'v3': [],
                      'v4': []}
        tg = DirectedGraph.from_dict(graph_dict)
        g = DirectedGraph.from_transpose(tg)

        v0 = g.get_vertex('v0')
        v1 = g.get_vertex('v1')
        v2 = g.get_vertex('v2')
        v3 = g.get_vertex('v3')
        v4 = g.get_vertex('v4')
        self.assertEqual(g.num_vertices, 5)
        self.assertEqual(g.num_edges, 4)
        self.assertEqual(set(v0.outs), set([v1]))
        self.assertEqual(set(v1.outs), set([v0]))
        self.assertEqual(set(v2.outs), set([v0]))
        self.assertEqual(set(v3.outs), set([v1]))
        self.assertEqual(set(v4.outs), set())
        self.assertEqual(set(v0.ins), set([v1, v2]))
        self.assertEqual(set(v1.ins), set([v0, v3]))
        self.assertEqual(set(v2.ins), set())
        self.assertEqual(set(v3.ins), set())
        self.assertEqual(set(v4.ins), set())

    def test_create_random_directed_graph(self):
        """ Create a directed graph with edges between random nodes """
        num_vertices = 10
        v_vals = ['v' + str(i) for i in xrange(num_vertices)]
        g_half = DirectedGraph.random_graph(v_vals, 0.5)
        g_zero = DirectedGraph.random_graph(v_vals, 0.0)
        g_one = DirectedGraph.random_graph(v_vals, 1.0)

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
        v_vals = ['v' + str(i) for i in xrange(num_vertices)]
        g = DirectedGraph.complete_graph(v_vals)

        max_edges = num_vertices ** 2
        self.assertEqual(g.num_vertices, num_vertices)
        self.assertEqual(g.num_edges, max_edges)

    def test_directed_graph_vertices_and_edges(self):
        """ Get directed graphs' vertices and edges properties """
        g = DirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_edge(('v0', 'v1'))

        v0 = g.get_vertex('v0')
        v1 = g.get_vertex('v1')
        e01 = g.get_edge(('v0', 'v1'))
        self.assertEqual(set(g.vertices), set([v0, v1]))
        self.assertEqual(set(g.edges), set([e01]))
        with self.assertRaises(AttributeError):
            g.vertices = set()
        with self.assertRaises(AttributeError):
            g.edges = set()

    def test_directed_graph_num_vertices_and_num_edges(self):
        """ Get the number of a directed graph's vertices and edges """
        g = DirectedGraph.from_dict({'v0': [('v1',)],
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
        g = DirectedGraph.from_dict({'v0': [('v1',)],
                                     'v1': [],
                                     'v2': []})
        empty_g = DirectedGraph()

        self.assertEqual(g.average_outs, 1.0 / 3.0)
        self.assertEqual(g.average_ins, 1.0 / 3.0)
        with self.assertRaises(AttributeError):
            g.average_outs = 0
        with self.assertRaises(AttributeError):
            g.average_ins = 0
        self.assertEqual(empty_g.average_outs, 0)
        self.assertEqual(empty_g.average_ins, 0)

    def test_directed_graph_is_weakly_connected(self):
        """ Get whether a path exists for every pair of vertices in a directed
            graph when treating its edges as undirected """
        g_connected = DirectedGraph.from_dict({'v0': [('v1',), ('v2',)],
                                               'v1': [],
                                               'v2': []})
        g_disconnected = DirectedGraph.from_dict({'v0': [('v1',)],
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
        g_connected = DirectedGraph.from_dict({'v0': [('v1',)],
                                               'v1': [('v2',)],
                                               'v2': [('v0',)]})
        g_disconnected = DirectedGraph.from_dict({'v0': [('v1',), ('v2',)],
                                                  'v1': [],
                                                  'v2': []})

        self.assertTrue(g_connected.is_strongly_connected)
        self.assertFalse(g_disconnected.is_strongly_connected)
        with self.assertRaises(AttributeError):
            g_connected.is_strongly_connected = False
        with self.assertRaises(AttributeError):
            g_disconnected.is_strongly_connected = True

    def test_directed_graph_clone(self):
        """ Clone a directed graph """
        vertices = [('v0', {'city': 'Paris'}),
                    ('v1', {'continent': 'Europe', 'city': 'London'}),
                    ('v2',),
                    ('v3',),
                    ('v4',)]
        edges = [(('v0', 'v1'), {'weight': 3}),
                 (('v0', 'v2'), {'weight': 4}),
                 (('v1', 'v3'),)]
        g = DirectedGraph.from_lists(vertices, edges)

        g_prime = g.clone()

        v0 = g.get_vertex('v0')
        v0_prime = g_prime.get_vertex('v0')
        e01 = g.get_edge(('v0', 'v1'))
        e01_prime = g_prime.get_edge(('v0', 'v1'))
        self.assertEqual(g_prime.num_vertices, g.num_vertices)
        self.assertEqual(g_prime.num_edges, g.num_edges)
        self.assertNotEqual(v0, v0_prime)
        self.assertNotEqual(e01, e01_prime)
        self.assertEqual(v0.attrs, v0_prime.attrs)

        g.add_vertex('v5', {'city': 'Jamestown'})

        self.assertTrue(g.has_vertex('v5'))
        self.assertFalse(g_prime.has_vertex('v5'))

        g.remove_vertex('v0')

        self.assertFalse(g.has_vertex('v0'))
        self.assertTrue(g_prime.has_vertex('v0'))
        self.assertFalse(g.has_edge(('v0', 'v1')))
        self.assertTrue(g_prime.has_edge(('v0', 'v1')))

        e01.set('weight', 5)

        self.assertEqual(e01.get('weight'), 5)
        self.assertEqual(e01_prime.get('weight'), 3)

    def test_directed_graph_add_vertex(self):
        """ Add vertices to a directed graph """
        g = DirectedGraph()
        v0_val = g.add_vertex(v_val='v0', attrs={'city': 'Modena'})
        v1_val = g.add_vertex(v_val='v1')

        self.assertEqual(v0_val, 'v0')
        self.assertEqual(v1_val, 'v1')
        self.assertTrue(g.has_vertex('v0'))
        self.assertTrue(g.has_vertex('v1'))
        self.assertFalse(g.has_vertex('v2'))
        self.assertEqual(g.get_vertex('v0').get('city'), 'Modena')
        self.assertIsNone(g.get_vertex('v1').get('city'))

    def test_directed_graph_add_edge(self):
        """ Add edges to a directed graph """
        g = DirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_edge(('v0', 'v0'), attrs={'weight': 5})
        g.add_edge(('v0', 'v1'), attrs={'weight': 7})

        e00 = g.get_edge(('v0', 'v0'))
        e01 = g.get_edge(('v0', 'v1'))
        self.assertTrue(g.has_edge(('v0', 'v0')))
        self.assertTrue(g.has_edge(('v0', 'v1')))
        self.assertFalse(g.has_edge(('v0', 'v2')))
        self.assertFalse(g.has_edge(('v1', 'v0')))
        self.assertEqual(e00.get('weight'), 5)
        self.assertEqual(e01.get('weight'), 7)

    def test_directed_graph_remove_vertex(self):
        """ Remove vertices from a directed graph """
        g = DirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_vertex(v_val='v2')
        g.add_edge(('v0', 'v1'))
        g.add_edge(('v1', 'v2'))

        g.remove_vertex('v0')

        self.assertFalse(g.has_vertex('v0'))
        self.assertTrue(g.has_vertex('v1'))
        self.assertTrue(g.has_vertex('v2'))
        self.assertFalse(g.has_edge(('v0', 'v1')))
        self.assertFalse(g.has_edge(('v1', 'v0')))
        self.assertTrue(g.has_edge(('v1', 'v2')))

        g.remove_vertex('v1')

        self.assertFalse(g.has_vertex('v0'))
        self.assertFalse(g.has_vertex('v1'))
        self.assertTrue(g.has_vertex('v2'))
        self.assertFalse(g.has_edge(('v0', 'v1')))
        self.assertFalse(g.has_edge(('v1', 'v1')))
        self.assertFalse(g.has_edge(('v1', 'v2')))

    def test_directed_graph_remove_edge(self):
        """ Remove edges from a directed graph """
        g = DirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_vertex(v_val='v2')
        g.add_edge(('v0', 'v1'))
        g.add_edge(('v0', 'v2'))

        g.remove_edge(('v0', 'v1'))

        self.assertFalse(g.has_edge(('v0', 'v1')))
        self.assertFalse(g.has_edge(('v1', 'v0')))
        self.assertTrue(g.has_edge(('v0', 'v2')))

        g.remove_edge(('v0', 'v2'))

        self.assertFalse(g.has_edge(('v0', 'v1')))
        self.assertFalse(g.has_edge(('v1', 'v0')))
        self.assertFalse(g.has_edge(('v0', 'v2')))

    def test_directed_graph_search(self):
        """ Search for paths from a directed vertex to all vertices reachable
            from it """
        g = DirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_vertex(v_val='v2')
        g.add_vertex(v_val='v3')
        g.add_vertex(v_val='v4')
        g.add_edge(('v0', 'v0'))
        g.add_edge(('v0', 'v1'))
        g.add_edge(('v2', 'v0'))
        g.add_edge(('v1', 'v3'))

        self.assertEqual(g.search('v0', goal_val='v0'), ['v0'])
        self.assertEqual(g.search('v0', goal_val='v1'), ['v0', 'v1'])
        self.assertIsNone(g.search('v0', goal_val='v2'))
        self.assertEqual(g.search('v0', goal_val='v3'), ['v0', 'v1', 'v3'])
        self.assertIsNone(g.search('v0', goal_val='v4'))
        self.assertEqual(g.search('v0'), {'v0': ['v0'],
                                          'v1': ['v0', 'v1'],
                                          'v3': ['v0', 'v1', 'v3']})
        self.assertEqual(g.search('v0', goal_val='v0', method='depth_first'),
                         ['v0'])
        self.assertEqual(g.search('v0', goal_val='v1', method='depth_first'),
                         ['v0', 'v1'])
        self.assertIsNone(g.search('v0', goal_val='v2', method='depth_first'))
        self.assertEqual(g.search('v0', goal_val='v3', method='depth_first'),
                         ['v0', 'v1', 'v3'])
        self.assertIsNone(g.search('v0', goal_val='v4', method='depth_first'))
        self.assertEqual(g.search('v0', method='depth_first'),
                         {'v0': ['v0'],
                          'v1': ['v0', 'v1'],
                          'v3': ['v0', 'v1', 'v3']})

    def test_bad_directed_graph_input(self):
        """ A directed graph from_dict input must be of a certain form """
        graph_dict = {'v0': ['v1', {'weight': 3}],
                      'v1': [],
                      'v2': []}

        with self.assertRaises(BadGraphInputException):
            _ = UndirectedGraph.from_dict(graph_dict)

    def test_directed_graph_vertex_already_exists(self):
        """ A directed graph should not be able to add a vertex that already
            exists in the graph """
        g = DirectedGraph()
        g.add_vertex(v_val='v0')

        with self.assertRaises(VertexAlreadyExistsException):
            g.add_vertex('v0')

    def test_directed_graph_edge_already_exists_exception(self):
        """ A directed graph should not be able to add an edge that already
            exists in the graph """
        g = DirectedGraph()
        g.add_vertex(v_val='v0')
        g.add_vertex(v_val='v1')
        g.add_edge(('v0', 'v1'))

        with self.assertRaises(EdgeAlreadyExistsException):
            g.add_edge(('v0', 'v1'))


def n_choose_2(n):
    return n * (n - 1) / 2.0


if __name__ == '__main__':
    unittest.main()
