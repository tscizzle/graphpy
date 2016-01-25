"""
Implementation of an edge, as used in graphs
"""


################################################################################
#                                                                              #
#                                  Undirected                                  #
#                                                                              #
################################################################################


class UndirectedEdge(object):

    def __init__(self, v0, v1):
        if v0 == v1:
            raise NoSelfEdgeException(v0, v1)
        self._vertices = frozenset([v0, v1])

    def __repr__(self):
        vertices = tuple(self._vertices)
        return "Edge(%s, %s)" % (vertices[0], vertices[1])

    def __str__(self):
        vertices = tuple(self._vertices)
        return "E(%s, %s)" % (str(vertices[0]), str(vertices[1]))

    def __eq__(self, other):
        return self._vertices == other.vertices

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._vertices)

    @property
    def vertices(self):
        return self._vertices


################################################################################
#                                                                              #
#                                   Directed                                   #
#                                                                              #
################################################################################


class DirectedEdge(object):

    def __init__(self, v_from, v_to):
        self._v_from = v_from
        self._v_to = v_to

    def __repr__(self):
        return "Edge(%s, %s)" % (self._v_from, self._v_to)

    def __str__(self):
        return "E(%s, %s)" % (str(self._v_from), str(self._v_to))

    def __eq__(self, other):
        return (self._v_from, self._v_to) == (other.v_from, other.v_to)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self._v_from, self._v_to))

    @property
    def v_from(self):
        return self._v_from

    @property
    def v_to(self):
        return self._v_to


################################################################################
#                                                                              #
#                                  Exceptions                                  #
#                                                                              #
################################################################################


class NoSelfEdgeException(Exception):
    def __init__(self, v0, v1):
        m = ("Cannot make an edge from a vertex (" + str(v0) + ") to itself (" +
             str(v1) + ").")
        super(NoSelfEdgeException, self).__init__(m)
