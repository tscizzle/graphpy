"""
Implementation of an edge, as used in graphs
"""


################################################################################
#                                                                              #
#                                  Undirected                                  #
#                                                                              #
################################################################################


class UndirectedEdge(object):

    def __init__(self, vertices, attrs=None):
        self._vertices = frozenset(vertices)
        self._attrs = attrs or {}
        self._is_self_edge = vertices[0] == vertices[1]

    def __repr__(self):
        vertices = (tuple(self._vertices) if not self._is_self_edge else
                    tuple(self._vertices) * 2)
        return "Edge(%s, %s)" % (vertices[0], vertices[1])

    def __str__(self):
        vertices = (tuple(self._vertices) if not self._is_self_edge else
                    tuple(self._vertices) * 2)
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

    @property
    def attrs(self):
        return self._attrs

    @property
    def is_self_edge(self):
        return self._is_self_edge

    def get(self, attr):
        """ Get an attribute """
        return self._attrs.get(attr)

    def set(self, attr, value):
        """ Set an attribute """
        self._attrs[attr] = value

    def has_attr(self, attr):
        """ Check if an attribute exists """
        return attr in self._attrs

    def del_attr(self, attr):
        """ Delete an attribute """
        del self._attrs[attr]


################################################################################
#                                                                              #
#                                   Directed                                   #
#                                                                              #
################################################################################


class DirectedEdge(object):

    def __init__(self, vertices, attrs=None):
        self._v_from = vertices[0]
        self._v_to = vertices[1]
        self._attrs = attrs or {}

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

    @property
    def attrs(self):
        return self._attrs

    def get(self, attr):
        """ Get an attribute """
        return self._attrs.get(attr)

    def set(self, attr, value):
        """ Set an attribute """
        self._attrs[attr] = value

    def has_attr(self, attr):
        """ Check if an attribute exists """
        return attr in self._attrs

    def del_attr(self, attr):
        """ Delete an attribute """
        del self._attrs[attr]
