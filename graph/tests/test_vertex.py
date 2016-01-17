"""
Tests for vertex.py
"""


from edge import UndirectedEdge, DirectedEdge
from vertex import UndirectedVertex, DirectedVertex, EdgeAlreadyExistsException

import unittest


class TestUndirectedVertex(unittest.TestCase):

    def test_create_undirected_vertex(self):
        v0 = UndirectedVertex(name='v0')

        self.assertEqual(v0.name, 'v0')
        self.assertEqual(v0.edges, [])

    def test_undirected_vertex_add_and_has_edge(self):
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        v0.add_edge(v1)
        e01 = UndirectedEdge(v0, v1)
        e10 = UndirectedEdge(v1, v0)
        e02 = UndirectedEdge(v0, v2)

        self.assertTrue(v0.has_edge(e01))
        self.assertTrue(v0.has_edge(e10))
        self.assertTrue(v1.has_edge(e01))
        self.assertTrue(v1.has_edge(e10))
        self.assertFalse(v2.has_edge(e01))
        self.assertFalse(v0.has_edge(e02))

    def test_undirected_edge_already_exists(self):
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v0.add_edge(v1)

        with self.assertRaises(EdgeAlreadyExistsException):
            v0.add_edge(v1)
        with self.assertRaises(EdgeAlreadyExistsException):
            v1.add_edge(v0)

    def test_undirected_vertex_neighbors_and_degree(self):
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        v3 = UndirectedVertex(name='v3')
        v4 = UndirectedVertex(name='v4')
        v0.add_edge(v1)
        v0.add_edge(v2)
        v1.add_edge(v3)

        self.assertEqual(v0.neighbors(), set([v1, v2]))
        self.assertEqual(v1.neighbors(), set([v0, v3]))
        self.assertEqual(v2.neighbors(), set([v0]))
        self.assertEqual(v3.neighbors(), set([v1]))
        self.assertEqual(v4.neighbors(), set())
        self.assertEqual(v0.degree(), 2)
        self.assertEqual(v1.degree(), 2)
        self.assertEqual(v2.degree(), 1)
        self.assertEqual(v3.degree(), 1)
        self.assertEqual(v4.degree(), 0)

    def test_undirected_vertex_search(self):
        v0 = UndirectedVertex(name='v0')
        v1 = UndirectedVertex(name='v1')
        v2 = UndirectedVertex(name='v2')
        v3 = UndirectedVertex(name='v3')
        v4 = UndirectedVertex(name='v4')
        v0.add_edge(v1)
        v0.add_edge(v2)
        v1.add_edge(v3)

        self.assertEqual(v0.search(goal=v0), [v0])
        self.assertEqual(v0.search(goal=v1), [v0, v1])
        self.assertEqual(v0.search(goal=v2), [v0, v2])
        self.assertEqual(v0.search(goal=v3), [v0, v1, v3])
        self.assertIsNone(v0.search(goal=v4))
        self.assertEqual(v0.search(), {v0: [v0],
                                       v1: [v0, v1],
                                       v2: [v0, v2],
                                       v3: [v0, v1, v3]})
        self.assertEqual(v0.search(goal=v0, method='depth_first'), [v0])
        self.assertEqual(v0.search(goal=v1, method='depth_first'), [v0, v1])
        self.assertEqual(v0.search(goal=v2, method='depth_first'), [v0, v2])
        self.assertEqual(v0.search(goal=v3, method='depth_first'), [v0, v1, v3])
        self.assertIsNone(v0.search(goal=v4, method='depth_first'))
        self.assertEqual(v0.search(method='depth_first'), {v0: [v0],
                                                           v1: [v0, v1],
                                                           v2: [v0, v2],
                                                           v3: [v0, v1, v3]})


class TestDirectedVertex(unittest.TestCase):

    def test_create_directed_vertex(self):
        v0 = DirectedVertex(name='v0')

        self.assertEqual(v0.name, 'v0')
        self.assertEqual(v0.edges, [])

    def test_directed_vertex_add_and_has_edge(self):
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        v0.add_edge(v1)
        e01 = DirectedEdge(v0, v1)
        e10 = DirectedEdge(v1, v0)
        e02 = DirectedEdge(v0, v2)

        self.assertTrue(v0.has_edge(e01))
        self.assertFalse(v0.has_edge(e10))
        self.assertTrue(v1.has_edge(e01))
        self.assertFalse(v1.has_edge(e10))
        self.assertFalse(v2.has_edge(e01))
        self.assertFalse(v0.has_edge(e02))

    def test_directed_vertex_already_exists(self):
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v0.add_edge(v1)

        with self.assertRaises(EdgeAlreadyExistsException):
            v0.add_edge(v1)
        try:
            v1.add_edge(v0)
        except EdgeAlreadyExistsException:
            self.fail("There should be no EdgeAlreadyExistsException because "
                      "(v1 -> v0) is a different edge than (v0 -> v1) for a "
                      "DirectedVertex.")

    def test_directed_vertex_ins_and_outs_and_degrees(self):
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        v3 = DirectedVertex(name='v3')
        v4 = DirectedVertex(name='v4')
        v0.add_edge(v0)
        v0.add_edge(v1)
        v0.add_edge(v2)
        v1.add_edge(v3)
        v3.add_edge(v1)

        self.assertEqual(v0.outs(), set([v0, v1, v2]))
        self.assertEqual(v0.ins(), set([v0]))
        self.assertEqual(v1.outs(), set([v3]))
        self.assertEqual(v1.ins(), set([v0, v3]))
        self.assertEqual(v2.outs(), set())
        self.assertEqual(v2.ins(), set([v0]))
        self.assertEqual(v3.outs(), set([v1]))
        self.assertEqual(v3.ins(), set([v1]))
        self.assertEqual(v4.outs(), set())
        self.assertEqual(v4.ins(), set())
        self.assertEqual(v0.out_degree(), 3)
        self.assertEqual(v0.in_degree(), 1)
        self.assertEqual(v1.out_degree(), 1)
        self.assertEqual(v1.in_degree(), 2)
        self.assertEqual(v2.out_degree(), 0)
        self.assertEqual(v2.in_degree(), 1)
        self.assertEqual(v3.out_degree(), 1)
        self.assertEqual(v3.in_degree(), 1)
        self.assertEqual(v4.out_degree(), 0)
        self.assertEqual(v4.in_degree(), 0)

    def test_directed_vertex_search(self):
        v0 = DirectedVertex(name='v0')
        v1 = DirectedVertex(name='v1')
        v2 = DirectedVertex(name='v2')
        v3 = DirectedVertex(name='v3')
        v4 = DirectedVertex(name='v4')
        v0.add_edge(v0)
        v0.add_edge(v1)
        v2.add_edge(v0)
        v1.add_edge(v3)
        v3.add_edge(v1)

        self.assertEqual(v0.search(goal=v0), [v0])
        self.assertEqual(v0.search(goal=v1), [v0, v1])
        self.assertIsNone(v0.search(goal=v2))
        self.assertEqual(v0.search(goal=v3), [v0, v1, v3])
        self.assertIsNone(v0.search(goal=v4))
        self.assertEqual(v0.search(), {v0: [v0],
                                       v1: [v0, v1],
                                       v3: [v0, v1, v3]})
        self.assertEqual(v0.search(goal=v0, method='depth_first'), [v0])
        self.assertEqual(v0.search(goal=v1, method='depth_first'), [v0, v1])
        self.assertIsNone(v0.search(goal=v2, method='depth_first'))
        self.assertEqual(v0.search(goal=v3, method='depth_first'), [v0, v1, v3])
        self.assertIsNone(v0.search(goal=v4, method='depth_first'))
        self.assertEqual(v0.search(method='depth_first'), {v0: [v0],
                                                           v1: [v0, v1],
                                                           v3: [v0, v1, v3]})


if __name__ == '__main__':
    unittest.main()
