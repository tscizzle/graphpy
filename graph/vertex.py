"""
Implementation of a vertex, as used in graphs
"""


from edge import UndirectedEdge, DirectedEdge


class UndirectedVertex(object):

    def __init__(self, name=''):
        self.name = name or id(self)
        self.edges = []

    def __repr__(self):
        display = (self.name, id(self))
        return "Vertex(name=%s, id=%s)" % display

    def __str__(self):
        return "V(%s)" % self.name

    @property
    def neighbors(self):
        """ List of vertices adjacent to this vertex """
        return set(vertex for e in self.edges for vertex in e.vertices
                   if vertex != self)

    @property
    def degree(self):
        """ Number of neighbors this vertex has """
        return len(self.neighbors)

    def has_edge(self, e):
        """ Checks if a certain edge already exists on this vertex """
        return e in self.edges

    def add_edge(self, other_v):
        """ Adds an edge from this vertex to another vertex """
        e = UndirectedEdge(self, other_v)

        if self.has_edge(e) or other_v.has_edge(e):
            raise VertexAlreadyHasEdgeException(e)

        self.edges.append(e)
        other_v.edges.append(e)
        return e

    def search(self, goal=None, method='breadth_first'):
        """ Search for either some goal vertex or all vertices reachable from
            this vertex """
        assert method in set(['breadth_first', 'depth_first'])
        pop_idx = 0 if method == 'breadth_first' else -1

        vertex_queue = [(self, [self])]
        seen_so_far = set([self])
        paths = {}

        # handle each vertex until there are no vertices left to check
        while vertex_queue:
            current_vertex, current_path = vertex_queue.pop(pop_idx)

            # if searching for a specific vertex, check if this is it
            if goal is not None and current_vertex == goal:
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


class DirectedVertex(object):

    def __init__(self, name=''):
        self.name = name
        self.edges = []

    def __repr__(self):
        display = (self.name, id(self))
        return "Vertex(name=%s, id=%s)" % display

    def __str__(self):
        return "V(%s)" % self.name

    @property
    def outs(self):
        """ List of vertices into which this vertex has an edge """
        return set(e.v_to for e in self.edges if e.v_from == self)

    @property
    def ins(self):
        """ List of vertices which have an edge into this vertex """
        return set(e.v_from for e in self.edges if e.v_to == self)

    @property
    def out_degree(self):
        """ Number of vertices into which this vertex has an edge """
        return len(self.outs)

    @property
    def in_degree(self):
        """ Number of vertices which have an edge into this vertex """
        return len(self.ins)

    @property
    def degree(self):
        """ Number of vertices which have an edge with this vertex (in or
            out) """
        return self.in_degree + self.out_degree

    def has_edge(self, e):
        """ Checks if a certain edge already exists on this vertex """
        return e in self.edges

    def add_edge(self, other_v):
        """ Adds an edge from this vertex to another vertex """
        e = DirectedEdge(self, other_v)

        if self.has_edge(e) or other_v.has_edge(e):
            raise VertexAlreadyHasEdgeException(e)

        self.edges.append(e)
        other_v.edges.append(e)
        return e

    def search(self, goal=None, method='breadth_first'):
        """ Search for either some goal vertex or all vertices reachable from
            this vertex """
        assert method in set(['breadth_first', 'depth_first'])
        pop_idx = 0 if method == 'breadth_first' else -1

        vertex_queue = [(self, [self])]
        seen_so_far = set([self])
        paths = {}

        # handle each vertex until there are no vertices left to check
        while vertex_queue:
            current_vertex, current_path = vertex_queue.pop(pop_idx)

            # if searching for a specific vertex, check if this is it
            if goal is not None and current_vertex == goal:
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


class VertexAlreadyHasEdgeException(Exception):
    def __init__(self, e):
        m = str(e) + " already exists."
        super(VertexAlreadyHasEdgeException, self).__init__(m)
