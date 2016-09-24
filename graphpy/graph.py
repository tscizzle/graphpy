"""
Implementation of a graph
"""


from edge import UndirectedEdge, DirectedEdge
from vertex import UndirectedVertex, DirectedVertex

import random


################################################################################
#                                                                              #
#                                  Undirected                                  #
#                                                                              #
################################################################################


class UndirectedGraph(object):

    def __init__(self):
        self._vertices = set()
        self._edges = set()
        self._names_to_vertices_map = {}
        self._names_to_edges_map = {}

    def __str__(self):
        vertices_str = ", ".join(str(v) for v in self._vertices)
        edges_str = ", ".join(str(e) for e in self._edges)
        return "Vertices: %s\nEdges: %s" % (vertices_str, edges_str)

    def __len__(self):
        return self.num_vertices

    def __getitem__(self, key):
        if isinstance(key, basestring):
            if key not in self._names_to_vertices_map:
                raise KeyError("No vertex with name " + key + ".")
            else:
                return self._names_to_vertices_map[key]
        elif (isinstance(key, tuple) and len(key) == 2 and
                         all(isinstance(v_name, basestring) for v_name in key)):
            if key not in self._names_to_edges_map:
                raise KeyError("No edge between vertices with names " +
                               key[0] + " and " + key[1] + ".")
            else:
                return self._names_to_edges_map[key]
        else:
            raise TypeError("Can't get key " + str(key) + ". Must be either a "
                            "string or tuple of length 2 of strings.")

    def __delitem__(self, key):
        if isinstance(key, basestring):
            self.remove_vertex(self[key])
        elif isinstance(key, tuple) and len(key) == 2:
            self.remove_edge(*(self[v_name] for v_name in key))
        else:
            raise TypeError("Can't del with key " + str(key) + ". Must be "
                            "either a string or tuple of length 2 of strings.")

    def __iter__(self):
        return iter(self._vertices)

    def __contains__(self, item):
        return self.has_vertex(item) or self.has_edge(item)

    @classmethod
    def from_lists(cls, vertices, edges):
        g = cls()
        for v in vertices:
            g.add_vertex(v)
        for e in edges:
            g.add_edge(*e.vertices, attrs=e.attrs)
        return g

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
                    m = (str(n_name) + " is in a neighbor list but is not a "
                         "vertex key.")
                    raise BadGraphInputException(m)
        return g

    @classmethod
    def from_directed_graph(cls, directed_graph):
        """ Generate an undirected graph by turning a directed graph's edges
            into undirected edges and removing duplicate edges """
        g = cls()
        for v in directed_graph.vertices:
            g.add_vertex(UndirectedVertex(name=v.name))
        for e in directed_graph.edges:
            try:
                g.add_edge(g[e.v_from.name], g[e.v_to.name])
            except EdgeAlreadyExistsException:
                pass
        return g

    @classmethod
    def random_graph(cls, vertex_names, p):
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
        return cls.random_graph(vertex_names, 1.0)

    @property
    def vertices(self):
        return iter(self._vertices)

    @property
    def edges(self):
        return iter(self._edges)

    @property
    def num_vertices(self):
        """ Number of vertices in this graph """
        return len(self._vertices)

    @property
    def num_edges(self):
        """ Number of edges in this graph """
        return len(self._edges)

    @property
    def average_degree(self):
        """ Average number of neighbors vertices in this graph have """
        if not self.num_vertices:
            return 0
        return 2.0 * self.num_edges / self.num_vertices

    @property
    def is_connected(self):
        """ Checks if this graph has paths from each vertex to each other
            vertex """
        return len(self.search(tuple(self._vertices)[0])) == self.num_vertices

    def has_vertex(self, v):
        """ Checks if a certain vertex already exists in this graph """
        return v in self._vertices

    def has_edge(self, e):
        """ Checks if a certain edge already exists in this graph """
        return e in self._edges

    def add_vertex(self, v):
        """ Adds a vertex to this graph """
        if self.has_vertex(v):
            raise VertexAlreadyExistsException(v)
        if v.name in self._names_to_vertices_map:
            raise VertexNameAlreadyExistsException(v.name)
        if v.degree:
            raise VertexAlreadyHasEdgesException(v)

        self._vertices.add(v)
        self._names_to_vertices_map[v.name] = v

    def add_edge(self, v0, v1, attrs=None):
        """ Adds an edge between two vertices in this graph """
        e = UndirectedEdge(v0, v1, attrs=attrs)
        if self.has_edge(e):
            raise EdgeAlreadyExistsException(e)

        v0.add_edge(e)
        if not e.is_self_edge:
            v1.add_edge(e)
        self._edges.add(e)
        self._names_to_edges_map[(v0.name, v1.name)] = e
        self._names_to_edges_map[(v1.name, v0.name)] = e

    def remove_vertex(self, v):
        """ Removes a vertex from this graph """
        for e in set(v.edges):
            self.remove_edge(*e.vertices)
        self._vertices.discard(v)
        del self._names_to_vertices_map[v.name]

    def remove_edge(self, v0, v1):
        """ Removes an edge between two vertices in this graph """
        e = UndirectedEdge(v0, v1)

        v0.remove_edge(e)
        if not e.is_self_edge:
            v1.remove_edge(e)
        self._edges.discard(e)
        del self._names_to_edges_map[(v0.name, v1.name)]
        if not e.is_self_edge:
            del self._names_to_edges_map[(v1.name, v0.name)]

    def search(self, start, goal=None, method='breadth_first'):
        """ Search for either some goal vertex or all vertices reachable from
            some vertex """
        assert self.has_vertex(start)
        assert method in set(['breadth_first', 'depth_first'])
        pop_idx = 0 if method == 'breadth_first' else -1

        vertex_queue = [(start, [start])]
        seen_so_far = set([start])
        paths = {}

        # handle each vertex until there are no vertices left to check
        while vertex_queue:
            current_vertex, current_path = vertex_queue.pop(pop_idx)

            # if searching for a specific vertex, check if this is it
            if current_vertex == goal:
                return current_path

            # if this is the first visit to this vertex, store its path
            if current_vertex not in paths:
                paths[current_vertex] = current_path

            # put this vertex's neighbors onto the back of the queue
            for neighbor in current_vertex.neighbors:
                if neighbor not in seen_so_far:
                    new_path = current_path + [neighbor]
                    vertex_queue.append((neighbor, new_path))
                    seen_so_far.add(neighbor)

        # if searching for a specific vertex, it was not reachable
        if goal is not None:
            return None

        return paths


################################################################################
#                                                                              #
#                                   Directed                                   #
#                                                                              #
################################################################################


class DirectedGraph(object):

    def __init__(self):
        self._vertices = set()
        self._edges = set()
        self._names_to_vertices_map = {}
        self._names_to_edges_map = {}

    def __str__(self):
        vertices_str = ", ".join(str(v) for v in self._vertices)
        edges_str = ", ".join(str(e) for e in self._edges)
        return "Vertices: %s\nEdges: %s" % (vertices_str, edges_str)

    def __len__(self):
        return self.num_vertices

    def __getitem__(self, key):
        if isinstance(key, basestring):
            if key not in self._names_to_vertices_map:
                raise KeyError("No vertex with name " + key + ".")
            else:
                return self._names_to_vertices_map[key]
        elif (isinstance(key, tuple) and len(key) == 2 and
                         all(isinstance(v_name, basestring) for v_name in key)):
            if key not in self._names_to_edges_map:
                raise KeyError("No edge between vertices with names " +
                               key[0] + " and " + key[1] + ".")
            else:
                return self._names_to_edges_map[key]
        else:
            raise TypeError("Can't get key " + str(key) + ". Must be either a "
                            "string or tuple of length 2 of strings.")

    def __delitem__(self, key):
        if isinstance(key, basestring):
            self.remove_vertex(self[key])
        elif isinstance(key, tuple) and len(key) == 2:
            self.remove_edge(*(self[v_name] for v_name in key))
        else:
            raise TypeError("Can't del with key " + str(key) + ". Must be "
                            "either a string or tuple of length 2 of strings.")

    def __iter__(self):
        return iter(self._vertices)

    def __contains__(self, item):
        return self.has_vertex(item) or self.has_edge(item)

    @classmethod
    def from_lists(cls, vertices, edges):
        g = cls()
        for v in vertices:
            g.add_vertex(v)
        for e in edges:
            g.add_edge(e.v_from, e.v_to, attrs=e.attrs)
        return g

    @classmethod
    def from_dict(cls, graph_dict):
        """ Generate a graph by passing in a dictionary of vertex names each
            mapped to a set of names of vertices to which there is an edge """
        g = cls()
        for v_name in graph_dict:
            g.add_vertex(DirectedVertex(name=v_name))
        for v_name, o_name_list in graph_dict.items():
            for o_name in o_name_list:
                try:
                    g.add_edge(g[v_name], g[o_name])
                except EdgeAlreadyExistsException:
                    pass
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
        for e in transpose_graph.edges:
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

    @property
    def vertices(self):
        return iter(self._vertices)

    @property
    def edges(self):
        return iter(self._edges)

    @property
    def num_vertices(self):
        """ Number of vertices in this graph """
        return len(self._vertices)

    @property
    def num_edges(self):
        """ Number of edges in this graph """
        return len(self._edges)

    @property
    def average_outs(self):
        """ Average number of outs vertices in this graph have """
        if not self.num_vertices:
            return 0
        return 1.0 * self.num_edges / self.num_vertices

    @property
    def average_ins(self):
        """ Average number of ins vertices in this graph have """
        if not self.num_vertices:
            return 0
        return 1.0 * self.num_edges / self.num_vertices

    @property
    def is_weakly_connected(self):
        """ Checks if this graph has a path from each vertex to each other
            vertex when treating its edges as undirected """
        return UndirectedGraph.from_directed_graph(self).is_connected

    @property
    def is_strongly_connected(self):
        """ Checks if this graph has a path from each vertex to each other
            vertex """
        v_self = tuple(self._vertices)[0]
        t = self.from_transpose(self)
        v_t = tuple(t.vertices)[0]
        return (len(self.search(v_self)) == len(t.search(v_t)) ==
                self.num_vertices)

    def has_vertex(self, v):
        """ Checks if a certain vertex already exists in this graph """
        return v in self._vertices

    def has_edge(self, e):
        """ Checks if a certain edge already exists in this graph """
        return e in self._edges

    def add_vertex(self, v):
        """ Adds a vertex to this graph """
        if self.has_vertex(v):
            raise VertexAlreadyExistsException(v)
        if v.name in self._names_to_vertices_map:
            raise VertexNameAlreadyExistsException(v.name)
        if v.in_degree or v.out_degree:
            raise VertexAlreadyHasEdgesException(v)

        self._vertices.add(v)
        self._names_to_vertices_map[v.name] = v

    def add_edge(self, v_from, v_to, attrs=None):
        """ Adds an edge from one vertex in this graph to another """
        e = DirectedEdge(v_from, v_to, attrs=attrs)
        if self.has_edge(e):
            raise EdgeAlreadyExistsException(e)

        v_from.add_edge(e)
        if v_from != v_to:
            v_to.add_edge(e)
        self._edges.add(e)
        self._names_to_edges_map[(v_from.name, v_to.name)] = e

    def remove_vertex(self, v):
        """ Removes a vertex from this graph """
        for e in set(v.edges):
            self.remove_edge(e.v_from, e.v_to)
        self._vertices.discard(v)
        del self._names_to_vertices_map[v.name]

    def remove_edge(self, v_from, v_to):
        """ Removes an edge from one vertex in this graph to another """
        e = DirectedEdge(v_from, v_to)

        v_from.remove_edge(e)
        v_to.remove_edge(e)
        self._edges.discard(e)
        del self._names_to_edges_map[(v_from.name, v_to.name)]

    def search(self, start, goal=None, method='breadth_first'):
        """ Search for either some goal vertex or all vertices reachable from
            some vertex """
        assert self.has_vertex(start)
        assert method in set(['breadth_first', 'depth_first'])
        pop_idx = 0 if method == 'breadth_first' else -1

        vertex_queue = [(start, [start])]
        seen_so_far = set([start])
        paths = {}

        # handle each vertex until there are no vertices left to check
        while vertex_queue:
            current_vertex, current_path = vertex_queue.pop(pop_idx)

            # if searching for a specific vertex, check if this is it
            if current_vertex == goal:
                return current_path

            # if this is the first visit to this vertex, store its path
            if current_vertex not in paths:
                paths[current_vertex] = current_path

            # put the vertices this vertex points to onto the back of the queue
            for out in current_vertex.outs:
                if out not in seen_so_far:
                    new_path = current_path + [out]
                    vertex_queue.append((out, new_path))
                    seen_so_far.add(out)

        # if searching for a specific vertex, it was not reachable
        if goal is not None:
            return None

        return paths


################################################################################
#                                                                              #
#                                  Exceptions                                  #
#                                                                              #
################################################################################


class BadGraphInputException(Exception):
    pass

class VertexAlreadyExistsException(Exception):
    def __init__(self, v):
        m = str(v) + " already exists."
        super(VertexAlreadyExistsException, self).__init__(m)

class VertexNameAlreadyExistsException(Exception):
    def __init__(self, name):
        m = "A vertex with name " + name + " already exists in the graph."
        super(VertexNameAlreadyExistsException, self).__init__(m)

class EdgeAlreadyExistsException(Exception):
    def __init__(self, e):
        m = str(e) + " already exists."
        super(EdgeAlreadyExistsException, self).__init__(m)

class VertexAlreadyHasEdgesException(Exception):
    def __init__(self, v):
        m = "Can't add vertex " + str(v) + " with degree > 0 to a graph."
        super(VertexAlreadyHasEdgesException, self).__init__(m)
