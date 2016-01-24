graph.edge
==========

*class* graph.edge.**UndirectedEdge**(*v0*, *v1*)
    *property* **vertices**
        frozenset of the two UndirectedVertex objects this edge connects

*class* graph.edge.**DirectedEdge**(*v_from*, *v_to*)
    *property* **v_from**
        DirectedVertex object from which this edge points
    *property* **v_from**
        DirectedVertex object to which this edge points

*exception* graph.edge.**NoSelfEdgeException**(*e*)
    UndirectedEdge objects are not allowed to connect an UndirectedVertex object to itself

graph.vertex
============

*class* graph.vertex.**UndirectedVertex**(*name=None*)
    *property* **name**
        String name of this vertex

*class* graph.vertex.**DirectedVertex**(*name=None*)
    *property* **name**
        String name of this vertex
