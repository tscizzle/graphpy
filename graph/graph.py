"""
Implementation of a graph
"""


from edge import UndirectedEdge, DirectedEdge, NoSelfEdgeException
from vertex import UndirectedVertex, DirectedVertex

import random


class UndirectedGraph(object):

    def __init__(self):
        self._vertices = set()
        self._edges = set()
        self._names_to_vertices_map = {}

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    def __str__(self):
        vertices_str = ", ".join(str(v) for v in self._vertices)
        edges_str = ", ".join(str(e) for e in self._edges)
        return "Vertices: %s\nEdges: %s" % (vertices_str, edges_str)

    def __getitem__(self, key):
        if not isinstance(key, basestring):
            raise TypeError("Can't index with non-string key " + str(key) + ".")
        if key not in self._names_to_vertices_map:
            raise KeyError("No vertex with name " + key + ".")

        return self._names_to_vertices_map[key]

    @classmethod
    def from_dict(cls, graph_dict):
        """ Generate a graph by passing in a dictionary of vertex names each
            mapped to a set of names of vertices to which there is an edge """
        g = cls()
        for v_name in graph_dict:
            g.add_vertex(UndirectedVertex(name=v_name))
        for v_name, n_name_list in graph_dict.items():
            for n_name in n_name_list:
                try:
                    g.add_edge(g[v_name], g[n_name])
                except EdgeAlreadyExistsException:
                    pass
                except KeyError:
                    m = (str(n_name) + " in a neighbor list but not in the "
                         "vertex list.")
                    raise BadGraphInputException(m)
        return g

    @classmethod
    def from_directed_graph(cls, directed_graph):
        """ Generate an undirected graph by turning a directed graph's edges
            into undirected edges and removing duplicate edges and
            self-edges """
        g = cls()
        for v in directed_graph.vertices:
            g.add_vertex(UndirectedVertex(name=v.name))
        for e in directed_graph.edges:
            try:
                g.add_edge(g[e.v_from.name], g[e.v_to.name])
            except (EdgeAlreadyExistsException, NoSelfEdgeException):
                pass
        return g

    @classmethod
    def random_graph(cls, vertex_names, p=0.5):
        """ Generate a graph using a set of vertex names where each pair of
            vertices has some probability of having an edge between them """
        g = cls()
        for v_name in vertex_names:
            g.add_vertex(UndirectedVertex(name=v_name))
        for v0 in g.vertices:
            for v1 in g.vertices:
                if v0 > v1 and random.random() < p:
                    g.add_edge(v0, v1)
        return g

    @classmethod
    def complete_graph(cls, vertex_names):
        """ Generate a graph with all possible edges using a set of vertex
            names """
        return cls.random_graph(vertex_names, p=1.0)

    def num_vertices(self):
        """ Number of vertices in this graph """
        return len(self._vertices)

    def num_edges(self):
        """ Number of edges in this graph """
        return len(self._edges)

    def has_vertex(self, v):
        """ Checks if a certain vertex already exists in this graph """
        return v in self._vertices

    def has_edge(self, e):
        """ Checks if a certain edge already exists in this graph """
        return e in self._edges

    def add_vertex(self, v):
        """ Adds a vertex to this graph """
        if v.name in self._names_to_vertices_map:
            raise VertexNameAlreadyExistsException(v.name)
        if self.has_vertex(v):
            raise VertexAlreadyExistsException(v)
        if v.degree():
            raise VertexAlreadyHasEdgesException(v)

        self._vertices.add(v)
        self._names_to_vertices_map[v.name] = v
        return v

    def add_edge(self, v0, v1):
        """ Adds an edge between two vertices in this graph """
        e = UndirectedEdge(v0, v1)
        if self.has_edge(e):
            raise EdgeAlreadyExistsException(e)

        self._edges.add(v0.add_edge(v1))
        return e

    def average_degree(self):
        """ Average number of neighbors vertices in this graph have """
        if not self.num_vertices:
            return 0
        return 2.0 * self.num_edges() / self.num_vertices()

    def is_connected(self):
        """ Checks if this graph has paths from each vertex to each other
            vertex """
        return len(self.search(tuple(self._vertices)[0])) == self.num_vertices

    def search(self, start, goal=None, method='breadth_first'):
        """ Search for either some goal vertex or all vertices reachable from
            some vertex """
        return start.search(goal=goal, method=method)


class DirectedGraph(object):

    def __init__(self, name=''):
        self.name = name or id(self)
        self._vertices = set()
        self._edges = set()
        self._names_to_vertices_map = {}

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    def __str__(self):
        vertices_str = ", ".join(str(v) for v in self._vertices)
        edges_str = ", ".join(str(e) for e in self._edges)
        return "Vertices: %s\nEdges: %s" % (vertices_str, edges_str)

    def __getitem__(self, key):
        if not isinstance(key, basestring):
            raise TypeError("Can't index with non-string key " + str(key) + ".")
        if key not in self._names_to_vertices_map:
            raise KeyError("No vertex with name " + key + ".")

        return self._names_to_vertices_map[key]

    @classmethod
    def from_dict(cls, graph_dict):
        """ Generate a graph by passing in a dictionary of vertex names each
            mapped to a set of names of vertices to which there is an edge """
        g = cls()
        for v_name in graph_dict:
            g.add_vertex(UndirectedVertex(name=v_name))
        for v_name, o_name_list in graph_dict.items():
            for o_name in o_name_list:
                try:
                    g.add_edge(g[v_name], g[o_name])
                except KeyError:
                    m = (str(o_name) + " in a neighbor list but not in the "
                         "vertex list.")
                    raise BadGraphInputException(m)
        return g

    @classmethod
    def from_transpose(cls, transpose_graph):
        """ Generate a graph by transposing another graph (reversing all of its
            edges) """
        g = cls()
        for v in transpose_graph.vertices:
            g.add_vertex(DirectedVertex(name=v.name))
        for e in transpose_graph:
            g.add_edge(g[e.v_to.name], g[e.v_from.name])
        return g

    @classmethod
    def random_graph(cls, vertex_names, p=0.5):
        """ Generate a graph using a set of vertex names where each ordered pair
            of vertices has some probability of having an edge from the first to
            the second """
        g = cls()
        for v_name in vertex_names:
            g.add_vertex(DirectedVertex(name=v_name))
        for v0 in g.vertices:
            for v1 in g.vertices:
                if random.random() < p:
                    g.add_edge(v0, v1)
        return g

    @classmethod
    def complete_graph(cls, vertex_names):
        """ Generate a graph with all possible edges using a set of vertex
            names """
        return cls.random_graph(vertex_names, p=1.0)

    def num_vertices(self):
        """ Number of vertices in this graph """
        return len(self._vertices)

    def num_edges(self):
        """ Number of edges in this graph """
        return len(self._edges)

    def has_vertex(self, v):
        """ Checks if a certain vertex already exists in this graph """
        return v in self._vertices

    def has_edge(self, e):
        """ Checks if a certain edge already exists in this graph """
        return e in self._edges

    def add_vertex(self, v):
        """ Adds a vertex to this graph """
        if v.name in self._names_to_vertices_map:
            raise VertexNameAlreadyExistsException(v.name)
        if self.has_vertex(v):
            raise VertexAlreadyExistsException(v)
        if v.in_degree() or v.out_degree():
            raise VertexAlreadyHasEdgesException(v)

        self._vertices.add(v)
        self._names_to_vertices_map[v.name] = v
        return v

    def add_edge(self, v0, v1):
        """ Adds an edge from one vertex in this graph to another """
        e = DirectedEdge(v0, v1)
        if self.has_edge(e):
            raise EdgeAlreadyExistsException(e)

        self._edges.add(v0.add_edge(v1))
        return e

    def average_ins(self):
        """ Average number of ins vertices in this graph have """
        if not self.num_vertices:
            return 0
        return 1.0 * self.num_edges() / self.num_vertices()

    def average_outs(self):
        """ Average number of outs vertices in this graph have """
        if not self.num_vertices:
            return 0
        return 1.0 * self.num_edges() / self.num_vertices()

    def is_weakly_connected(self):
        """ Checks if this graph has a path from each vertex to each other
            vertex when treating its edges as undirected """
        return UndirectedGraph.from_directed_graph(self).is_connected()

    def is_strongly_connected(self):
        """ Checks if this graph has a path from each vertex to each other
            vertex """
        v = tuple(self._vertices)[0]
        t = self.from_transpose(self)
        return len(self.search(v)) == len(t.search(v)) == self.num_vertices

    def search(self, start, goal=None, method='breadth_first'):
        """ Search for either some goal vertex or all vertices reachable from
            some vertex """
        return start.search(goal=goal, method=method)


class BadGraphInputException(Exception):
    pass

class VertexNameAlreadyExistsException(Exception):
    def __init__(self, name):
        m = "A vertex with name " + name + " already exists in the graph."
        super(VertexNameAlreadyExistsException, self).__init__(m)

class VertexAlreadyExistsException(Exception):
    def __init__(self, v):
        m = str(v) + " already exists."
        super(VertexAlreadyExistsException, self).__init__(m)

class EdgeAlreadyExistsException(Exception):
    def __init__(self, e):
        m = str(e) + " already exists."
        super(EdgeAlreadyExistsException, self).__init__(m)

class VertexAlreadyHasEdgesException(Exception):
    def __init__(self, v):
        m = "Can't add vertex " + str(v) + " with degree > 0 to a graph."
        super(VertexAlreadyHasEdgesException, self).__init__(m)
