"""
Implementation of a graph
"""


from edge import UndirectedEdge, DirectedEdge
from vertex import UndirectedVertex, DirectedVertex
from helpers import *

import copy
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
        self._vals_to_vertices_map = {}
        self._vals_to_edges_map = {}

    def __str__(self):
        vertices_str = ", ".join(str(v) for v in self._vertices)
        edges_str = ", ".join(str(e) for e in self._edges)
        return "Vertices: %s\nEdges: %s" % (vertices_str, edges_str)

    def __len__(self):
        return self.num_vertices

    def __iter__(self):
        return iter(self._vertices)

    @classmethod
    def from_lists(cls, vertices, edges):
        """ Generate a graph by passing in a list of vertex vals and a list of
            edges between those vertices """
        g = cls()

        for v in vertices:
            if isinstance(v, tuple) and (len(v) == 1 or len(v) == 2):
                g.add_vertex(*v)
            else:
                m = (str(v) + " must be a tuple and have length 1 or 2")
                raise ValueError(m)

        for e in edges:
            if isinstance(e, tuple) and (len(e) == 1 or len(e) == 2):
                g.add_edge(*e)
            else:
                m = (str(e) + " must be a tuple and have length 1 or 2")
                raise ValueError(m)

        return g

    @classmethod
    def from_dict(cls, graph_dict, vertex_attrs=None):
        """ Generate a graph by passing in a dictionary of vertex vals each
            mapped to a set of vals of vertices to which there is an edge """
        vertex_attrs = vertex_attrs or {}

        g = cls()

        for v_val in graph_dict:
            g.add_vertex(v_val)

        for v_val, neighbor_edge_list in graph_dict.items():
            for neighbor_edge in neighbor_edge_list:
                if (isinstance(neighbor_edge, tuple) and
                    (len(neighbor_edge) == 1 or len(neighbor_edge) == 2)):
                    neighbor_val = neighbor_edge[0]
                    edge_attrs = (neighbor_edge[1] if len(neighbor_edge) == 2
                                                   else None)
                else:
                    m = (str(neighbor_edge) + " must be a tuple and have "
                         "length 1 or 2")
                    raise ValueError(m)

                if not is_hashable(neighbor_val):
                    raise ValueError(str(neighbor_val) + " is not hashable")

                if not g.has_vertex(neighbor_val):
                    g.add_vertex(neighbor_val)

                v_vals = (v_val, neighbor_val)
                if not g.has_edge(v_vals):
                    g.add_edge(v_vals, attrs=edge_attrs)

        for v_val, v_attrs in vertex_attrs.items():
            if not g.has_vertex(v_val):
                g.add_vertex(v_val)
            v = g.get_vertex(v_val)
            for attr, value in v_attrs.items():
                v.set(attr, value)

        return g

    @classmethod
    def from_directed_graph(cls, directed_graph):
        """ Generate an undirected graph by turning a directed graph's edges
            into undirected edges and removing duplicate edges """
        g = cls()

        for v in directed_graph.vertices:
            g.add_vertex(v.val)

        for e in directed_graph.edges:
            v_vals = (e.v_from.val, e.v_to.val)
            if not g.has_edge(v_vals):
                g.add_edge(v_vals)

        return g

    @classmethod
    def random_graph(cls, vertex_vals, p):
        """ Generate a graph using a set of vertex vals where each pair of
            vertices has some probability of having an edge between them """
        g = cls()

        for v_val in vertex_vals:
            g.add_vertex(v_val)

        for v0 in g.vertices:
            for v1 in g.vertices:
                if v0 > v1 and random.random() < p:
                    g.add_edge((v0.val, v1.val))

        return g

    @classmethod
    def complete_graph(cls, vertex_vals):
        """ Generate a graph with all possible edges using a set of vertex
            vals """
        return cls.random_graph(vertex_vals, 1.0)

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
        return (len(self.search(tuple(self._vertices)[0].val)) ==
                self.num_vertices)

    def clone(self):
        """ Clones this graph """
        g = self.__class__()

        for v in self._vertices:
            g.add_vertex(v.val, attrs=copy.deepcopy(v.attrs))

        for e in self._edges:
            vertices = list(e.vertices)
            g.add_edge((vertices[0].val, vertices[-1].val),
                       attrs=copy.deepcopy(e.attrs))

        return g

    def has_vertex(self, v_val):
        """ Checks if a certain vertex already exists in this graph """
        return v_val in self._vals_to_vertices_map

    def has_edge(self, v_vals):
        """ Checks if a certain edge already exists in this graph """
        return v_vals in self._vals_to_edges_map

    def get_vertex(self, v_val):
        """ Gets a vertex in this graph """
        return self._vals_to_vertices_map.get(v_val)

    def get_edge(self, v_vals):
        """ Gets an edge between vertices in this graph """
        return self._vals_to_edges_map.get(v_vals)

    def add_vertex(self, v_val=None, attrs=None):
        """ Adds a vertex to this graph """
        if not is_hashable(v_val):
            raise TypeError(str(v_val) + " must be hashable")
        v = UndirectedVertex(val=v_val, attrs=attrs)
        if self.has_vertex(v_val):
            raise ValueError(str(v) + " already exists")

        self._vertices.add(v)
        self._vals_to_vertices_map[v_val] = v

        return v.val

    def add_edge(self, v_vals, attrs=None):
        """ Adds an edge between vertices in this graph """
        v0_val, v1_val = v_vals
        v0 = self.get_vertex(v0_val)
        v1 = self.get_vertex(v1_val)
        e = UndirectedEdge((v0, v1), attrs=attrs)
        if self.has_edge((v0_val, v1_val)):
            raise ValueError(str(e) + " already exists")

        v0.add_edge(e)
        if not e.is_self_edge:
            v1.add_edge(e)
        self._edges.add(e)
        self._vals_to_edges_map[(v0_val, v1_val)] = e
        self._vals_to_edges_map[(v1_val, v0_val)] = e

    def remove_vertex(self, v_val):
        """ Removes a vertex from this graph """
        v = self.get_vertex(v_val)
        for e in set(v.edges):
            vertices = list(e.vertices)
            self.remove_edge((vertices[0].val, vertices[-1].val))
        self._vertices.discard(v)
        del self._vals_to_vertices_map[v_val]

    def remove_edge(self, v_vals):
        """ Removes an edge between vertices in this graph """
        v0_val, v1_val = v_vals
        v0 = self.get_vertex(v0_val)
        v1 = self.get_vertex(v1_val)
        e = UndirectedEdge((v0, v1))

        v0.remove_edge(e)
        if not e.is_self_edge:
            v1.remove_edge(e)
        self._edges.discard(e)
        del self._vals_to_edges_map[(v0.val, v1.val)]
        if not e.is_self_edge:
            del self._vals_to_edges_map[(v1.val, v0.val)]

    def search(self, start_val, goal_val=None, method='breadth_first'):
        """ Search for either some goal vertex or all vertices reachable from
            a source vertex """
        ## TODO: change these asserts to raises of ValueError
        assert self.has_vertex(start_val)
        assert goal_val is None or self.has_vertex(goal_val)
        assert method in set(['breadth_first', 'depth_first'])
        start = self.get_vertex(start_val)
        goal = self.get_vertex(goal_val)
        pop_idx = 0 if method == 'breadth_first' else -1

        vertex_queue = [(start, [start])]
        seen_so_far = set([start])
        paths = {}

        namify_path = lambda path: [v.val for v in path]

        # handle each vertex until there are no vertices left to check
        while vertex_queue:
            current_vertex, current_path = vertex_queue.pop(pop_idx)

            # if searching for a specific vertex, check if this is it
            if current_vertex == goal:
                return namify_path(current_path)

            # if this is the first visit to this vertex, store its path
            if current_vertex not in paths:
                paths[current_vertex.val] = namify_path(current_path)

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

    def dijkstra(self, start_val, goal_val=None, return_distances=False,
                 priority_queue=PriorityQueue):
        """ Find the shortest path to either some goal vertex or to all vertices
            reachable from a source vertex """
        for e in self._edges:
            edge_weight = e.get('weight')
            if edge_weight is None:
                raise ValueError(str(e) + " must have a weight")
            if edge_weight < 0:
                raise ValueError(str(e) + " must have a non-negative weight")
        start = self.get_vertex(start_val)
        goal = self.get_vertex(goal_val)

        distances = {v: float('inf') for v in self}
        predecessors = {v: -1 for v in self}
        cloud_so_far = set([start])

        distances[start] = 0
        predecessors[start] = None

        # relax edges until there are no vertices left not in the cloud
        vertex_queue = priority_queue(data=[(distances[v], v) for v in self])
        while vertex_queue:
            # move the closest vertex that's not in the cloud into the cloud
            _, current_vertex = vertex_queue.pop_min()
            cloud_so_far.add(current_vertex)

            # if searching for a specific vertex, check if this is it
            if current_vertex == goal:
                break

            # conditionally relax each of that vertex's edges
            current_distance = distances[current_vertex]
            eligible_neighbors = [n for n in current_vertex.neighbors
                                  if n not in cloud_so_far]
            for neighbor in eligible_neighbors:
                current_neighbor_distance = distances[neighbor]
                e = self.get_edge((current_vertex.val, neighbor.val))
                new_neighbor_distance = current_distance + e.get('weight')
                if new_neighbor_distance < current_neighbor_distance:
                    distances[neighbor] = new_neighbor_distance
                    predecessors[neighbor] = current_vertex
                    vertex_queue.decrease_key(neighbor, new_neighbor_distance)

        # with the algorithm complete, prepare the output

        namify_keys = lambda dic: {v.val: d for v, d in dic.items()}
        namify_values = lambda dic: {k: v.val if hasattr(v, 'val') else v
                                     for k, v in dic.items()}
        namified_distances = namify_keys(distances)
        namified_predecessors = namify_values(namify_keys(predecessors))

        def backtrack(target_val):
            """ Use our predecessor map to get the shortest path from our start
                to some target """
            if namified_predecessors[target_val] == -1:
                return None
            path = [target_val]
            while namified_predecessors[path[-1]] is not None:
                path.append(namified_predecessors[path[-1]])
            path.reverse()
            return path

        if goal_val is not None:
            return (namified_distances[goal_val] if return_distances
                                                 else backtrack(goal_val))
        else:
            return (namified_distances if return_distances
                                       else keydefaultdict(backtrack))


################################################################################
#                                                                              #
#                                   Directed                                   #
#                                                                              #
################################################################################


class DirectedGraph(object):

    def __init__(self):
        self._vertices = set()
        self._edges = set()
        self._vals_to_vertices_map = {}
        self._vals_to_edges_map = {}

    def __str__(self):
        vertices_str = ", ".join(str(v) for v in self._vertices)
        edges_str = ", ".join(str(e) for e in self._edges)
        return "Vertices: %s\nEdges: %s" % (vertices_str, edges_str)

    def __len__(self):
        return self.num_vertices

    def __iter__(self):
        return iter(self._vertices)

    @classmethod
    def from_lists(cls, vertices, edges):
        """ Generate a graph by passing in a list of vertex vals and a list of
            edges between those vertices """
        g = cls()

        for v in vertices:
            if isinstance(v, tuple) and (len(v) == 1 or len(v) == 2):
                g.add_vertex(*v)
            else:
                m = (str(v) + " must be a tuple and have length 1 or 2")
                raise ValueError(m)

        for e in edges:
            if isinstance(e, tuple) and (len(e) == 1 or len(e) == 2):
                g.add_edge(*e)
            else:
                m = (str(e) + " must be a tuple and have length 1 or 2")
                raise ValueError(m)

        return g

    @classmethod
    def from_dict(cls, graph_dict, vertex_attrs=None):
        """ Generate a graph by passing in a dictionary of vertex vals each
            mapped to a set of vals of vertices to which there is an edge """
        vertex_attrs = vertex_attrs or {}

        g = cls()

        for v_val in graph_dict:
            g.add_vertex(v_val)

        for v_val, out_edge_list in graph_dict.items():
            for out_edge in out_edge_list:
                if (isinstance(out_edge, tuple) and
                    (len(out_edge) == 1 or len(out_edge) == 2)):
                    out_val = out_edge[0]
                    edge_attrs = out_edge[1] if len(out_edge) == 2 else None
                else:
                    m = (str(out_edge) + " must be tuple and have length 1 or "
                         "2")
                    raise ValueError(m)

                if not is_hashable(out_val):
                    raise ValueError(str(out_val) + " is not hashable")

                if not g.has_vertex(out_val):
                    g.add_vertex(out_val)

                v_vals = (v_val, out_val)
                if not g.has_edge(v_vals):
                    g.add_edge(v_vals, attrs=edge_attrs)

        for v_val, v_attrs in vertex_attrs.items():
            if not g.has_vertex(v_val):
                g.add_vertex(v_val)
            v = g.get_vertex(v_val)
            for attr, value in v_attrs.items():
                v.set(attr, value)

        return g

    @classmethod
    def from_transpose(cls, transpose_graph):
        """ Generate a graph by transposing another graph (reversing all of its
            edges) """
        g = cls()
        for v in transpose_graph.vertices:
            g.add_vertex(v.val)
        for e in transpose_graph.edges:
            g.add_edge((e.v_to.val, e.v_from.val))
        return g

    @classmethod
    def random_graph(cls, vertex_vals, p=0.5):
        """ Generate a graph using a set of vertex vals where each ordered pair
            of vertices has some probability of having an edge from the first to
            the second """
        g = cls()
        for v_val in vertex_vals:
            g.add_vertex(v_val)
        for v0 in g.vertices:
            for v1 in g.vertices:
                if random.random() < p:
                    g.add_edge((v0.val, v1.val))
        return g

    @classmethod
    def complete_graph(cls, vertex_vals):
        """ Generate a graph with all possible edges using a set of vertex
            vals """
        return cls.random_graph(vertex_vals, p=1.0)

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
        return (len(self.search(v_self.val)) == len(t.search(v_t.val)) ==
                self.num_vertices)

    def clone(self):
        """ Clones this graph """
        g = self.__class__()

        for v in self._vertices:
            g.add_vertex(v.val, attrs=copy.deepcopy(v.attrs))

        for e in self._edges:
            g.add_edge((e.v_from.val, e.v_to.val), attrs=copy.deepcopy(e.attrs))

        return g

    def has_vertex(self, v_val):
        """ Checks if a certain vertex already exists in this graph """
        return v_val in self._vals_to_vertices_map

    def has_edge(self, v_vals):
        """ Checks if a certain edge already exists in this graph """
        return v_vals in self._vals_to_edges_map

    def get_vertex(self, v_val):
        """ Gets a vertex in this graph """
        return self._vals_to_vertices_map.get(v_val)

    def get_edge(self, v_vals):
        """ Gets an edge between vertices in this graph """
        return self._vals_to_edges_map.get(v_vals)

    def add_vertex(self, v_val=None, attrs=None):
        """ Adds a vertex to this graph """
        if not is_hashable(v_val):
            raise TypeError(str(v_val) + " must be hashable")
        v = DirectedVertex(val=v_val, attrs=attrs)
        if self.has_vertex(v_val):
            raise ValueError(str(v) + " already exists")

        self._vertices.add(v)
        self._vals_to_vertices_map[v_val] = v

        return v.val

    def add_edge(self, v_vals, attrs=None):
        """ Adds an edge from one vertex in this graph to another """
        v_from_val, v_to_val = v_vals
        v_from = self.get_vertex(v_from_val)
        v_to = self.get_vertex(v_to_val)
        e = DirectedEdge((v_from, v_to), attrs=attrs)
        if self.has_edge((v_from_val, v_to_val)):
            raise ValueError(str(e) + " already exists")

        v_from.add_edge(e)
        if v_from != v_to:
            v_to.add_edge(e)
        self._edges.add(e)
        self._vals_to_edges_map[(v_from.val, v_to.val)] = e

    def remove_vertex(self, v_val):
        """ Removes a vertex from this graph """
        v = self.get_vertex(v_val)
        for e in set(v.edges):
            self.remove_edge((e.v_from.val, e.v_to.val))
        self._vertices.discard(v)
        del self._vals_to_vertices_map[v_val]

    def remove_edge(self, v_vals):
        """ Removes an edge from one vertex in this graph to another """
        v_from_val, v_to_val = v_vals
        v_from = self.get_vertex(v_from_val)
        v_to = self.get_vertex(v_to_val)
        e = DirectedEdge((v_from, v_to))

        v_from.remove_edge(e)
        v_to.remove_edge(e)
        self._edges.discard(e)
        del self._vals_to_edges_map[(v_from.val, v_to.val)]

    def search(self, start_val, goal_val=None, method='breadth_first'):
        """ Search for either some goal vertex or all vertices reachable from
            some vertex """
        ## TODO: change these asserts to raises of ValueError
        assert self.has_vertex(start_val)
        assert goal_val is None or self.has_vertex(goal_val)
        assert method in set(['breadth_first', 'depth_first'])
        start = self.get_vertex(start_val)
        goal = self.get_vertex(goal_val)
        pop_idx = 0 if method == 'breadth_first' else -1

        vertex_queue = [(start, [start])]
        seen_so_far = set([start])
        paths = {}

        namify_path = lambda path: [v.val for v in path]

        # handle each vertex until there are no vertices left to check
        while vertex_queue:
            current_vertex, current_path = vertex_queue.pop(pop_idx)

            # if searching for a specific vertex, check if this is it
            if current_vertex == goal:
                return namify_path(current_path)

            # if this is the first visit to this vertex, store its path
            if current_vertex not in paths:
                paths[current_vertex.val] = namify_path(current_path)

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

    def dijkstra(self, start_val, goal_val=None, return_distances=False,
                 priority_queue=PriorityQueue):
        """ Find the shortest path to either some goal vertex or to all vertices
            reachable from a source vertex """
        for e in self._edges:
            edge_weight = e.get('weight')
            if edge_weight is None:
                raise ValueError(str(e) + " must have a weight")
            if edge_weight < 0:
                raise ValueError(str(e) + " must have a non-negative weight")
        raise NotImplementedError
