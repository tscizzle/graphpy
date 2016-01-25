graphpy
=======

graph.edge
----------

*class* graph.edge.\ **UndirectedEdge**(*v0*, *v1*)
    An edge with no concept of direction
    **Parameters**
        - **v0** (UndirectedVertex): one endpoint of this edge
        - **v1**: (UndirectedVertex): the other endpoint of this edge
    *property* **vertices**
        frozenset of the two UndirectedVertex objects this edge connects

*class* graph.edge.\ **DirectedEdge**(*v_from*, *v_to*)
    An edge with a concept of direction
    **Parameters**
        - **v_from** (DirectedVertex): tail of this edge
        - **v_to**: (DirectedVertex): head of this edge
    *property* **v_from**
        DirectedVertex object from which this edge points (the tail)
    *property* **v_from**
        DirectedVertex object to which this edge points (the head)

*exception* graph.edge.\ **NoSelfEdgeException**(*v0*, *v1*)
    UndirectedEdge objects are not allowed to connect an UndirectedVertex object to itself
    **Parameters**
        - **v0** (UndirectedVertex): one endpoint of the offending edge
        - **v1** (UndirectedVertex): the other endpoint of the offending edge

graph.vertex
------------

*class* graph.vertex.\ **UndirectedVertex**(*name=None*)
    A vertex used with undirected edges
    **Parameters**
        - **name**: String, identifying name of this vertex
    *property* **name**
        String name of this vertex
    *property* **edges**
        List of UndirectedEdge objects this vertex has
    *property* **neighbors**
        List of UndirectedVertex objects which share an edge with this vertex
    *property* **degree**
        Number of neighbors this vertex has
    *method* **add_edge**(*e*)
        Add an UndirectedEdge object to this vertex
        **Parameters**
            - **e**: UndirectedEdge, edge to add

*class* graph.vertex.\ **DirectedVertex**(*name=None*)
    A vertex used with directed edges
    **Parameters**
        - **name**: String, identifying name of this vertex
    *property* **name**
        String name of this vertex
    *property* **edges**
        List of DirectedEdge objects this vertex has
