"""
Implementation of an edge, as used in graphs
"""


class UndirectedEdge(object):

    def __init__(self, v0, v1):
        if v0 == v1:
            raise NoSelfEdgeException("Cannot make edge from " + str(v0) +
                                      " to itself.")
        self.vertices = set([v0, v1])

    def __repr__(self):
        vertices = tuple(self.vertices)
        return "Edge(%s, %s)" % (vertices[0], vertices[1])

    def __str__(self):
        vertices = tuple(self.vertices)
        return "E(%s, %s)" % (str(vertices[0]), str(vertices[1]))

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __ne__(self, other):
        return not self.__eq__(other)


class DirectedEdge(object):

    def __init__(self, v_from, v_to):
        self.v_from = v_from
        self.v_to = v_to

    def __repr__(self):
        return "Edge(%s, %s)" % (self.v_from, self.v_to)

    def __str__(self):
        return "E(%s, %s)" % (str(self.v_from), str(self.v_to))

    def __eq__(self, other):
        return (self.v_from, self.v_to) == (other.v_from, other.v_to)

    def __ne__(self, other):
        return not self.__eq__(other)


class NoSelfEdgeException(Exception):
    pass
