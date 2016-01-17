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

    def has_edge(self, edge):
        """ Checks if a certain edge already exists on this vertex """
        return edge in self.edges

    def add_edge(self, other):
        """ Adds an edge from this vertex to another vertex """
        edge = UndirectedEdge(self, other)

        if self.has_edge(edge) or other.has_edge(edge):
            raise EdgeAlreadyExistsException(str(edge) + " already exists.")

        self.edges.append(edge)
        other.edges.append(edge)
        return edge

    def neighbors(self):
        """ List of vertices adjacent to this vertex """
        return set(vertex for edge in self.edges for vertex in edge.vertices
                   if vertex != self)

    def degree(self):
        """ Number of neighbors this vertex has """
        return len(self.neighbors())

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
            for neighbor in current_vertex.neighbors():
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

    def has_edge(self, edge):
        """ Checks if a certain edge already exists on this vertex """
        return edge in self.edges

    def add_edge(self, other):
        """ Adds an edge from this vertex to another vertex """
        edge = DirectedEdge(self, other)

        if self.has_edge(edge) or other.has_edge(edge):
            raise EdgeAlreadyExistsException(str(edge) + " already exists.")

        self.edges.append(edge)
        other.edges.append(edge)
        return edge

    def outs(self):
        """ List of vertices into which this vertex has an edge """
        return set(edge.v_to for edge in self.edges if edge.v_from == self)

    def ins(self):
        """ List of vertices which have an edge into this vertex """
        return set(edge.v_from for edge in self.edges if edge.v_to == self)

    def out_degree(self):
        """ Number of vertices into which this vertex has an edge """
        return len(self.outs())

    def in_degree(self):
        """ Number of vertices which have an edge into this vertex """
        return len(self.ins())

    def degree(self):
        """ Number of vertices which have an """
        return self.in_degree() + self.out_degree()

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
            for out in current_vertex.outs():
                if out not in seen_so_far:
                    new_path = current_path + [out]
                    vertex_queue.append((out, new_path))
                    seen_so_far.add(out)

        # if searching for a specific vertex, it was not reachable
        if goal is not None:
            return None

        return paths


class EdgeAlreadyExistsException(Exception):
    def __init__(self, e):
        m = str(e) + " already exists."
        super(EdgeAlreadyExistsException, self).__init__(m)
