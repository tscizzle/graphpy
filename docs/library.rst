graphpy
=======

graph.edge
----------

*class* graph.edge.UndirectedEdge(*v0*, *v1*)
    - **Parameters**
        - **v0** <UndirectedVertex>
        - **v1** <UndirectedVertex>
    - *property* **vertices**
        - frozenset of the two UndirectedVertex objects this edge connects
    - *property* **is_self_edge**
        - bool for whether or not this edge connects a vertex to itself

*class* graph.edge.DirectedEdge(*v_from*, *v_to*)
    - **Parameters**
        - **v_from** <DirectedVertex>
        - **v_to** <DirectedVertex>
    - *property* **v_from**
        - DirectedVertex object from which this edge points (the tail)
    - *property* **v_to**
        - DirectedVertex object to which this edge points (the head)

graph.vertex
------------

*class* graph.vertex.UndirectedVertex(*name* =None)
    - **Parameters**
        - **name** <String>
    - *property* **name**
        - String name of this vertex
    - *property* **edges**
        - Iterator over UndirectedEdge objects this vertex has
    - *property* **has_self_edge**
        - bool for whether or not this vertex has an edge connecting it to itself
    - *property* **neighbors**
        - Iterator over UndirectedVertex objects which share an edge with this vertex
    - *property* **degree**
        - Number of neighbors this vertex has (+1 if it has a self edge)
    - *method* **__contains__** (*e*)
        - Can do ``e in v`` to check if the UndirectedVertex ``v`` has the UndirectedEdge ``e``
    - *method* **add_edge** (*e*)
        - **Parameters**
            - **e** <UndirectedEdge>
    - *method* **remove_edge** (*e*)
        - **Parameters**
            - **e** <UndirectedEdge>

*class* graph.vertex.DirectedVertex(*name* =None)
    - **Parameters**
        - **name** <String>
    - *property* **name**
        - String name of this vertex
    - *property* **edges**
        - Iterator over DirectedEdge objects this vertex has
    - *property* **outs**
        - Iterator over DirectedVertex objects into which this vertex has an edge
    - *property* **ins**
        - Iterator over DirectedVertex objects which have an edge into this vertex
    - *property* **out_degree**
        - Number of outs this vertex has
    - *property* **in_degree**
        - Number of ins this vertex has
    - *property* **degree**
        - Number of total ins and outs this vertex has
    - *method* **__contains__** (*e*)
        - Can do ``e in v`` to check if the DirectedVertex ``v`` has the DirectedEdge ``e``
    - *method* **add_edge** (*e*)
        - **Parameters**
            - **e** <DirectedEdge>
    - *method* **remove_edge** (*e*)
        - **Parameters**
            - **e** <DirectedEdge>

*exception* graph.vertex.VertexNotPartOfEdgeException(*v*, *e*)
    - Cannot add an edge to a vertex which is not one of that edge's endpoints

*exception* graph.vertex.VertexAlreadyHasEdgeException(*v*, *e*)
    - Cannot add an edge to a vertex that already has that edge

graph.graph
-----------

*class* graph.vertex.UndirectedGraph()
    - *classmethod* **from_dict** (*graph_dict*)
        - **Parameters**
            - **graph_dict** <dict>
                - String -> String[]
                - each vertex's name maps to a list of the names of the vertices to which that vertex has an edge
        - **Returns**
            - UndirectedGraph object defined by *graph_dict*
    - *classmethod* **from_directed_graph** (*directed_graph*)
        - **Parameters**
            - **directed_graph** <DirectedGraph>
                - the directed graph version of the desired undirected graph
        - **Returns**
            - UndirectedGraph object version of *directed_graph*
                - duplicate edges are treated as a single edge
    - *classmethod* **random_graph** (*vertex_names*, *p* =0.5)
        - **Parameters**
            - **vertex_names** <String[]>
                - List of names of the vertices to include
            - **p** <float>
                - float between 0 and 1
                - represents the probability each pair of vertices has of having an edge between them
        - **Returns**
            - UndirectedGraph object with edges between random pairs of vertices
    - *classmethod* **complete_graph** (*vertex_names*)
        - **Parameters**
            - **vertex_names** <String[]>
                - List of names of the vertices to include
        - **Returns**
            - UndirectedGraph object with edges between all pairs of vertices
    - *property* **vertices**
        - Iterator over UndirectedVertex objects this graph has
    - *property* **edges**
        - Iterator over UndirectedEdge objects this graph has
    - *property* **num_vertices**
        - Number of vertices this graph has
    - *property* **num_edges**
        - Number of edges this graph has
    - *property* **average_degree**
        - Average degree each vertex in this graph has
    - *property* **is_connected**
        - Whether or not there exists a path between every pair of vertices this graph has
    - *method* **__len__**
        - Can do ``len(g)`` to get the number of vertices in UndirectedGraph ``g``
    - *method* **__getitem__** (*v_name*)
        - Can do ``g[v_name]`` to check if UndirectedGraph ``g`` has an UndirectedVertex with name ``v_name``
        - Can do ``g[(v0_name, v1_name)]`` to check if UndirectedGraph ``g`` has an UndirectedEdge connecting UndirectedVertex objects with names ``v0_name`` and ``v1_name``
    - *method* **__delitem__** (*v_name*)
        - Can do ``del g[v_name]`` to remove an UndirectedVertex with name ``v_name`` from UndirectedGraph ``g``
        - Can do ``del g[(v0_name, v1_name)]`` to remove an UndirectedEdge connecting UndirectedVertex objects with names ``v0_name`` and ``v1_name`` from UndirectedGraph ``g``
    - *method* **__iter__**
        - Can do ``for v in g`` to iterate through the vertices of UndirectedGraph ``g``
    - *method* **__contains__** (*item*)
        - Can do ``v in g`` to check whether or not UndirectedVertex ``v`` is a vertex in UndirectedGraph ``g``
        - Can do ``e in g`` to check whether or not UndirectedEdge ``e`` is an edge in UndirectedGraph ``g``
    - *method* **has_vertex** (*v*)
        - **Parameters**
            - **v** <UndirectedVertex>
        - **Returns**
            - bool for whether or not *v* is a vertex in this graph
    - *method* **has_edge** (*e*)
        - **Parameters**
            - **e** <UndirectedEdge>
        - **Returns**
            - bool for whether or not *e* is an edge in this graph
    - *method* **add_vertex** (*v*)
        - **Parameters**
            - **v** <UndirectedVertex>
    - *method* **add_edge** (*v0*, *v1*)
        - **Parameters**
            - **v0** <UndirectedVertex>
            - **v1** <UndirectedVertex>
    - *method* **remove_vertex** (*v*)
        - **Parameters**
            - **v** <UndirectedVertex>
    - *method* **remove_edge** (*v0*, *v1*)
        - **Parameters**
            - **v0** <UndirectedVertex>
            - **v1** <UndirectedVertex>
    - *method* **search** (*start*, *goal* =None, *method* ='breadth_first')
        - **Parameters**
            - **start** <UndirectedVertex>
                - vertex to act as the root of the search algorithm
            - **goal** <UndirectedVertex>
                - optional
                - if specified, the search algorithm terminates when this vertex is found
                - if not specified, the search algorithm goes through the entire graph
            - **method** <String>
                - optional (defaults to 'breadth_first')
                - one of ['breadth_first', 'depth_first']
                - specifies which search algorithm is used
        - **Returns**
            - UndirectedVertex[] if *goal* is specified, representing the path from *start* to *goal*
            - dict mapping UndirectedVertex -> UndirectedVertex[] if *goal* is not specified, each value representing the path from *start* to that value's key

*class* graph.vertex.DirectedGraph()
    - *classmethod* **from_dict** (*graph_dict*)
        - **Parameters**
            - **graph_dict** <dict>
                - String -> String[]
                - each vertex's name maps to a list of the names of the vertices to which that vertex has an edge
        - **Returns**
            - DirectedGraph object defined by *graph_dict*
    - *classmethod* **from_transpose** (*transpose_graph*)
        - **Parameters**
            - **transpose_graph** <DirectedGraph>
                - a directed graph with the opposite orientation of the desired graph
        - **Returns**
            - DirectedGraph object with all edges of *transpose_graph* reversed
    - *classmethod* **random_graph** (*vertex_names*, *p* =0.5)
        - **Parameters**
            - **vertex_names** <String[]>
                - List of names of the vertices to include
            - **p** <float>
                - float between 0 and 1
                - represents the probability each pair of vertices has of having an edge between them in a certain direction (so for any pair (v0, v1) there is *p* probability this graph has the edge (v0 -> v1), and this is separate and independent of whether this graph has (v1 -> v0))
        - **Returns**
            - DirectedGraph object with edges between random pairs of vertices
    - *classmethod* **complete_graph** (*vertex_names*)
        - **Parameters**
            - **vertex_names** <String[]>
                - List of names of the vertices to include
        - **Returns**
            - DirectedGraph object with edges between all pairs of vertices in both directions
    - *property* **vertices**
        - Iterator over DirectedVertex objects this graph has
    - *property* **edges**
        - Iterator over DirectedEdge objects this graph has
    - *property* **num_vertices**
        - Number of vertices this graph has
    - *property* **num_edges**
        - Number of edges this graph has
    - *property* **average_outs**
        - Average number of outs each vertex in this graph has
    - *property* **average_ins**
        - Average number of ins each vertex in this graph has
    - *property* **is_weakly_connected**
        - Whether or not there exists a path between every pair of vertices in the undirected version of this graph
    - *property* **is_strongly_connected**
        - Whether or not there exists a path from each vertex in this graph to each other vertex
    - *method* **__len__**
        - Can do ``len(g)`` to get the number of vertices in DirectedGraph ``g``
    - *method* **__getitem__** (*v_name*)
        - Can do ``g[v_name]`` to check if DirectedGraph ``g`` has a DirectedVertex with name ``v_name``
        - Can do ``g[(v0_name, v1_name)]`` to check if DirectedGraph ``g`` has a DirectedEdge connecting DirectedVertex objects with names ``v0_name`` and ``v1_name``
    - *method* **__delitem__** (*v_name*)
        - Can do ``del g[v_name]`` to remove a DirectedVertex with name ``v_name`` from DirectedGraph ``g``
        - Can do ``del g[(v0_name, v1_name)]`` to remove a DirectedEdge connecting DirectedVertex objects with names ``v0_name`` and ``v1_name`` from DirectedGraph ``g``
    - *method* **__iter__**
        - Can do ``for v in g`` to iterate through the vertices of DirectedGraph ``g``
    - *method* **__contains__** (*item*)
        - Can do ``v in g`` to check whether or not DirectedVertex ``v`` is a vertex in DirectedGraph ``g``
        - Can do ``e in g`` to check whether or not DirectedEdge ``e`` is an edge in DirectedGraph ``g``
    - *method* **has_vertex** (*v*)
        - **Parameters**
            - **v** <DirectedVertex>
        - **Returns**
            - bool for whether or not *v* is a vertex in this graph
    - *method* **has_edge** (*e*)
        - **Parameters**
            - **e** <DirectedEdge>
        - **Returns**
            - bool for whether or not *e* is an edge in this graph
    - *method* **add_vertex** (*v*)
        - **Parameters**
            - **v** <DirectedVertex>
    - *method* **add_edge** (*v_from*, *v_to*)
        - **Parameters**
            - **v_from** <DirectedVertex>
            - **v_to** <DirectedVertex>
    - *method* **remove_vertex** (*v*)
        - **Parameters**
            - **v** <DirectedVertex>
    - *method* **remove_edge** (*v_from*, *v_to*)
        - **Parameters**
            - **v_from** <DirectedVertex>
            - **v_to** <DirectedVertex>
    - *method* **search** (*start*, *goal* =None, *method* ='breadth_first')
        - **Parameters**
            - **start** <DirectedVertex>
                - vertex to act as the root of the search algorithm
            - **goal** <DirectedVertex>
                - optional
                - if specified, the search algorithm terminates when this vertex is found
                - if not specified, the search algorithm goes through the entire graph
            - **method** <String>
                - optional (defaults to 'breadth_first')
                - one of ['breadth_first', 'depth_first']
                - specifies which search algorithm is used
        - **Returns**
            - DirectedVertex[] if *goal* is specified, representing the path from *start* to *goal*
            - dict mapping DirectedVertex -> DirectedVertex[] if *goal* is not specified, each value representing the path from *start* to that value's key

*exception* graph.graph.BadGraphInputException
    - Indicates there is something wrong with an input graph_dict

*exception* graph.graph.VertexAlreadyExistsException (*v*)
    - Cannot add a vertex to a graph that already has that vertex

*exception* graph.graph.VertexNameAlreadyExistsException (*name*)
    - Cannot add a vertex to a graph that already has a vertex with the same name

*exception* graph.graph.EdgeAlreadyExistsException (*e*)
    - Cannot add an edge to a graph that already has that edge

*exception* graph.graph.VertexAlreadyHasEdgesException (*v*)
    - Cannot add a vertex to a graph if that vertex already has edges
