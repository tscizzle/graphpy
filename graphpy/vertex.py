"""
Implementation of a vertex, as used in graphs
"""


################################################################################
#                                                                              #
#                                  Undirected                                  #
#                                                                              #
################################################################################


class UndirectedVertex(object):

    def __init__(self, name=''):
        self._name = name or id(self)
        self._edges = set()

    def __repr__(self):
        display = (self.name, id(self))
        return "Vertex(name=%s, id=%s)" % display

    def __str__(self):
        return "V(%s)" % self.name

    def __contains__(self, e):
        return e in self._edges

    @property
    def name(self):
        return self._name

    @property
    def edges(self):
        return self._edges

    @property
    def neighbors(self):
        """ List of vertices adjacent to this vertex """
        return set(v for e in self._edges for v in e.vertices if v != self)

    @property
    def degree(self):
        """ Number of neighbors this vertex has """
        return len(self.neighbors)

    def add_edge(self, e):
        """ Adds an edge to this vertex """
        if self not in e.vertices:
            raise VertexNotPartOfEdgeException(self, e)
        if e in self:
            raise VertexAlreadyHasEdgeException(self, e)

        self._edges.add(e)

    def remove_edge(self, e):
        """ Removes an edge from this vertex """
        self._edges.discard(e)


################################################################################
#                                                                              #
#                                   Directed                                   #
#                                                                              #
################################################################################


class DirectedVertex(object):

    def __init__(self, name=''):
        self._name = name
        self._edges = set()

    def __repr__(self):
        display = (self.name, id(self))
        return "Vertex(name=%s, id=%s)" % display

    def __str__(self):
        return "V(%s)" % self.name

    def __contains__(self, e):
        return e in self._edges

    @property
    def name(self):
        return self._name

    @property
    def edges(self):
        return self._edges

    @property
    def outs(self):
        """ List of vertices into which this vertex has an edge """
        return set(e.v_to for e in self._edges if e.v_from == self)

    @property
    def ins(self):
        """ List of vertices which have an edge into this vertex """
        return set(e.v_from for e in self._edges if e.v_to == self)

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
        """ Number of vertices which have an edge with this vertex (out or
            in) """
        return self.out_degree + self.in_degree

    def add_edge(self, e):
        """ Adds an edge to this vertex """
        if self != e.v_from and self != e.v_to:
            raise VertexNotPartOfEdgeException(self, e)
        if e in self:
            raise VertexAlreadyHasEdgeException(self, e)

        self._edges.add(e)

    def remove_edge(self, e):
        """ Removes an edge from this vertex """
        self._edges.discard(e)


################################################################################
#                                                                              #
#                                  Exceptions                                  #
#                                                                              #
################################################################################


class VertexNotPartOfEdgeException(Exception):
    def __init__(self, v, e):
        m = str(v) + " is not part of " + str(e) + "."
        super(VertexNotPartOfEdgeException, self).__init__(m)

class VertexAlreadyHasEdgeException(Exception):
    def __init__(self, v, e):
        m = str(v) + " already has " + str(e) + "."
        super(VertexAlreadyHasEdgeException, self).__init__(m)
