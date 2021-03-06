graphpy
=======

graphpy.edge
------------

*class* graphpy.edge.UndirectedEdge(*vertices*, *attrs* =None)
    - **Parameters**
        - **vertices** <tuple>
            - tuple of length 2 of UndirectedVertex objects
        - **attrs** <dict>
    - *property* **vertices**
        - frozenset of the two UndirectedVertex objects this edge connects
    - *property* **attrs**
        - dict of attributes this edge has
    - *property* **is_self_edge**
        - bool for whether or not this edge connects a vertex to itself
    - *method* **__eq__** (*other*)
        - can do ``e0 == e1`` to check edge equality
        - equality is based on the ``vertices`` property
    - *method* **__ne__** (*other*)
        - can do ``e0 != e1`` to check edge non-equality
        - non-equality is based on the ``vertices`` property
    - *method* **__hash__**
        - can do ``hash(e)`` to hash this edge, and that hash is also used for the hashing of dictionary keys
        - hashing is based on the ``vertices`` property
    - *method* **get** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - key in this edge's *attrs* dict
        - **Returns**
            - any object, whatever value the key *attr* points to in this edge's *attrs* dict
            - None, if this edge does not have the attribute
    - *method* **set** (**attr**, **value**)
        - **Parameters**
            - **attr** <hashable>
                - to be a key in this edge's *attrs* dict
            - **value** <any object>
                - to be the value pointed to by *attr* in this edge's *attrs* dict
    - *method* **has_attr** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - potential key in this edge's *attrs* dict
        - **Returns**
            - bool for whether or not this edge has *attr*
    - *method* **del_attr** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - key in this edge's *attrs* dict

*class* graphpy.edge.DirectedEdge(*vertices*, *attrs* =None)
    - **Parameters**
        - **vertices** <tuple>
            - tuple of length 2 of DirectedVertex objects
        - **attrs** <dict>
    - *method* **__eq__** (*other*)
        - can do ``e0 == e1`` to check edge equality
        - equality is based on the ``v_from`` and ``v_to`` properties
    - *method* **__ne__** (*other*)
        - can do ``e0 != e1`` to check edge non-equality
        - non-equality is based on the ``v_from`` and ``v_to`` properties
    - *method* **__hash__**
        - can do ``hash(e)`` to hash this edge, and that hash is also used for the hashing of dictionary keys
        - hashing is based on the ``v_from`` and ``v_to`` properties
    - *property* **v_from**
        - DirectedVertex object from which this edge points (the tail)
    - *property* **v_to**
        - DirectedVertex object to which this edge points (the head)
    - *property* **attrs**
        - dict of attributes this edge has
    - *method* **get** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - key in this edge's *attrs* dict
        - **Returns**
            - any object, whatever value the key *attr* points to in this edge's *attrs* dict
            - None, if this edge does not have the attribute
    - *method* **set** (**attr**, **value**)
        - **Parameters**
            - **attr** <hashable>
                - to be a key in this edge's *attrs* dict
            - **value** <any object>
                - to be the value pointed to by *attr* in this edge's *attrs* dict
    - *method* **has_attr** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - potential key in this edge's *attrs* dict
        - **Returns**
            - bool for whether or not this edge has *attr*
    - *method* **del_attr** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - key in this edge's *attrs* dict

graphpy.vertex
--------------

*class* graphpy.vertex.UndirectedVertex(*val* =None, *attrs* =None)
    - **Parameters**
        - **val** <hashable>
        - **attrs** <dict>
    - *property* **val**
        - hashable val of this vertex
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
    - *method* **get** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - key in this vertex's *attrs* dict
        - **Returns**
            - any object, whatever value the key *attr* points to in this vertex's *attrs* dict
            - None, if this vertex does not have the attribute
    - *method* **set** (**attr**, **value**)
        - **Parameters**
            - **attr** <hashable>
                - to be a key in this vertex's *attrs* dict
            - **value** <any object>
                - to be the value pointed to by *attr* in this vertex's *attrs* dict
    - *method* **has_attr** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - potential key in this vertex's *attrs* dict
        - **Returns**
            - bool for whether or not this vertex has *attr*
    - *method* **del_attr** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - key in this vertex's *attrs* dict

*class* graphpy.vertex.DirectedVertex(*val* =None, *attrs* =None)
    - **Parameters**
        - **val** <hashable>
        - **attrs** <dict>
    - *property* **val**
        - hashable val of this vertex
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
    - *method* **get** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - key in this vertex's *attrs* dict
        - **Returns**
            - any object, whatever value the key *attr* points to in this vertex's *attrs* dict
            - None, if this vertex does not have the attribute
    - *method* **set** (**attr**, **value**)
        - **Parameters**
            - **attr** <hashable>
                - to be a key in this vertex's *attrs* dict
            - **value** <any object>
                - to be the value pointed to by *attr* in this vertex's *attrs* dict
    - *method* **has_attr** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - potential key in this vertex's *attrs* dict
        - **Returns**
            - bool for whether or not this vertex has *attr*
    - *method* **del_attr** (*attr*)
        - **Parameters**
            - **attr** <hashable>
                - key in this vertex's *attrs* dict

graphpy.graph
-------------

*class* graphpy.graph.UndirectedGraph()
    - *classmethod* **from_lists** (*vertices*, *edges*)
        - **Parameters**
            - **vertices** <tuple[]>
                - each tuple is of the form (hashable,) representing (val,), or (hashable, dict) representing (val, attrs)
            - **edges** <tuple[]>
                - each tuple is of the form ((hashable, hashable),) representing ((v0_val, v1_val),), or ((hashable, hashable), dict) representing ((v0_val, v1_val), attrs)
        - **Returns**
            - UndirectedGraph object defined by *vertices* and *edges*
    - *classmethod* **from_dict** (*graph_dict*, *vertex_attrs* =None)
        - **Parameters**
            - **graph_dict** <dict>
                - hashable -> tuple[]
                - each vertex's val maps to a list of elements which each represent an edge from that vertex
                - each element (i.e. edge) in the mapped-to list is in one of two forms
                    - (hashable,), length-1 tuple containing the val of the vertex to which the edge points
                    - (hashable, dict), length-2 tuple containing the val of the vertex to which the edge points and the edge's attributes
                - if there are duplicate declarations of an edge (like v1 appearing in v0's list and v0 appearing in v1's list) with different attributes, the one to keep is chosen arbitrarily
            - **vertex_attrs** <dict>
                - hashable -> dict
                - each vertex's val mapped to an attrs dict, as used in vertex creation
                - vertices in vertex_attrs but not in graph_dict are added as new vertices
        - **Returns**
            - UndirectedGraph object defined by *graph_dict*
    - *classmethod* **from_directed_graph** (*directed_graph*)
        - **Parameters**
            - **directed_graph** <DirectedGraph>
                - the directed graph version of the desired undirected graph
        - **Returns**
            - UndirectedGraph object version of *directed_graph*
                - duplicate edges are treated as a single edge
    - *classmethod* **random_graph** (*vertex_vals*, *p* =0.5)
        - **Parameters**
            - **vertex_vals** <hashable[]>
                - List of vals of the vertices to include
            - **p** <float>
                - float between 0 and 1
                - represents the probability each pair of vertices has of having an edge between them
        - **Returns**
            - UndirectedGraph object with edges between random pairs of vertices
    - *classmethod* **complete_graph** (*vertex_vals*)
        - **Parameters**
            - **vertex_vals** <hashable[]>
                - List of vals of the vertices to include
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
    - *method* **__iter__**
        - Can do ``for v in g`` to iterate through the vertices of UndirectedGraph ``g``
    - *method* **clone**
        - **Returns**
            - UndirectedGraph, a copy of this graph with all new UndirectedVertex and UndirectedEdge objects
            - all vertex and edge attrs are deepcopied
    - *method* **has_vertex** (*v_val*)
        - **Parameters**
            - **v_val** <hashable>
        - **Returns**
            - bool for whether or not *v_val* is a vertex in this graph
    - *method* **has_edge** (*v_vals*)
        - **Parameters**
            - **v_vals** <tuple>
        - **Returns**
            - bool for whether or not there is an edge in this graph between v_vals[0] and v_vals[1]
    - *method* **get_vertex** (*v_val*)
        - **Parameters**
            - **v_val** <hashable>
        - **Returns**
            - UndirectedVertex object with val of *v_val*, or None if no such vertex is in this graph
    - *method* **get_edge** (*v_vals*)
        - **Parameters**
            - **v_vals** <tuple>
        - **Returns**
            - UndirectedEdge object with vertices with vals of v_vals[0] and v_vals[1], or None if no such edge is in this graph
    - *method* **add_vertex** (*val* =None, *attrs* =None)
        - **Parameters**
            - **val** <hashable>
            - **attrs** <dict>
        - **Returns**
            - the new vertex's val, which is an arbitrary id if *val* is None
    - *method* **add_edge** (*v_vals*, *attrs* =None)
        - **Parameters**
            - **v_vals** <tuple>
            - **attrs** <dict>
    - *method* **remove_vertex** (*val*)
        - **Parameters**
            - **val** <hashable>
    - *method* **remove_edge** (*v_vals*)
        - **Parameters**
            - **v_vals** <tuple>
    - *method* **search** (*start_val*, *goal_val* =None, *method* ='breadth_first')
        - **Parameters**
            - **start_val** <hashable>
                - vertex to act as the root of the search algorithm
            - **goal_val** <hashable>
                - optional
                - if specified, the search algorithm terminates when this vertex is found
                - if not specified, the search algorithm goes through the entire graph
            - **method** <String>
                - optional (defaults to 'breadth_first')
                - one of ['breadth_first', 'depth_first']
                - specifies which search algorithm is used
        - **Returns**
            - hashable[] if *goal_val* is specified, representing the path from *start_val* to *goal_val*
            - dict mapping hashable -> hashable[] if *goal_val* is not specified, each value representing the path from *start_val* to that value's key
    - *method* **dijkstra** (*start_val*, *goal_val* =None, *return_distances* =False, *priority_queue* =PriorityQueue)
        - **Parameters**
            - **start_val** <hashable>
                - vertex to act as the root of the search algorithm
            - **goal_val** <hashable>
                - optional
                - if specified, the search algorithm terminates when this vertex is found
                - if not specified, the search algorithm goes through the entire graph
            - **return_distances** <bool>
                - optional
                - whether or not to return distances instead of full paths
            - **priority_queue** <class>
                - optional
                - specs for a suitable priority queue class can be found in the **extras** section of these docs
        - **Returns**
            - hashable[] if *goal_val* is specified, representing the path from *start_val* to *goal_val*
            - dict mapping hashable -> hashable[] if *goal_val* is not specified, each value representing the path from *start_val* to that value's key
            - if *return_distances* is True, instead of the path (hashable[]) it is just the distance (number)
            - if a vertex is not reachable from *start_val*, its path is None and its distance is `inf`

*class* graphpy.graph.DirectedGraph()
    - *classmethod* **from_lists** (*vertices*, *edges*)
        - **Parameters**
            - **vertices** <tuple[]>
                - each tuple is of the form (hashable,) representing (val,), or (hashable, dict) representing (val, attrs)
            - **edges** <tuple[]>
                - each tuple is of the form ((hashable, hashable),) representing ((v_from_val, v_to_val),), or ((hashable, hashable), dict)) representing ((v_from_val, v_to_val), attrs))
        - **Returns**
            - DirectedGraph object defined by *vertices* and *edges*
    - *classmethod* **from_dict** (*graph_dict*, *vertex_attrs* =None)
        - **Parameters**
            - **graph_dict** <dict>
                - hashable -> tuple[]
                - each vertex's val maps to a list of elements which each represent an edge from that vertex
                - each element (i.e. edge) in the mapped-to list is in one of two forms
                    - (hashable,), length-1 tuple containing the val of the vertex to which the edge points
                    - (hashable, dict), length-2 tuple containing the val of the vertex to which the edge points and the edge's attributes
                - if there are duplicate declarations of an edge (like v1 appearing in v0's list and v0 appearing in v1's list) with different attributes, the one to keep is chosen arbitrarily
            - **vertex_attrs** <dict>
                - hashable -> dict
                - each vertex's val mapped to an attrs dict, as used in vertex creation
                - vertices in vertex_attrs but not in graph_dict are added as new vertices
        - **Returns**
            - DirectedGraph object defined by *graph_dict*
    - *classmethod* **from_transpose** (*transpose_graph*)
        - **Parameters**
            - **transpose_graph** <DirectedGraph>
                - a directed graph with the opposite orientation of the desired graph
        - **Returns**
            - DirectedGraph object with all edges of *transpose_graph* reversed
    - *classmethod* **random_graph** (*vertex_vals*, *p* =0.5)
        - **Parameters**
            - **vertex_vals** <hashable[]>
                - List of vals of the vertices to include
            - **p** <float>
                - float between 0 and 1
                - represents the probability each pair of vertices has of having an edge between them in a certain direction
                    - (so for any pair (v0, v1) there is *p* probability this graph has the edge (v0 -> v1), and this is separate from and independent of whether this graph has the edge (v1 -> v0))
        - **Returns**
            - DirectedGraph object with edges between random pairs of vertices
    - *classmethod* **complete_graph** (*vertex_vals*)
        - **Parameters**
            - **vertex_vals** <hashable[]>
                - List of vals of the vertices to include
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
    - *method* **__iter__**
        - Can do ``for v in g`` to iterate through the vertices of DirectedGraph ``g``
    - *method* **clone**
        - **Returns**
            - DirectedGraph, a copy of this graph with all new DirectedVertex and DirectedEdge objects
            - all vertex and edge attrs are deepcopied
    - *method* **has_vertex** (*v_val*)
        - **Parameters**
            - **v_val** <hashable>
        - **Returns**
            - bool for whether or not *v_val* is a vertex in this graph
    - *method* **has_edge** (*v_vals*)
        - **Parameters**
            - **v_vals** <tuple>
        - **Returns**
            - bool for whether or not there is an edge in this graph from v_vals[0] to v_vals[1]
    - *method* **get_vertex** (*v_val*)
        - **Parameters**
            - **v_val** <hashable>
        - **Returns**
            - DirectedVertex object with val of *v_val*, or None if no such vertex is in this graph
    - *method* **get_edge** (*v_vals*)
        - **Parameters**
            - **v_vals** <tuple>
        - **Returns**
            - DirectedEdge object with vertices with vals of v_vals[0] and v_vals[1], or None if no such edge is in this graph
    - *method* **add_vertex** (*val* =None, *attrs* =None)
        - **Parameters**
            - **val** <hashable>
            - **attrs** <dict>
        - **Returns**
            - the new vertex's val, which is an arbitrary id if *val* is None
    - *method* **add_edge** (*v_vals*, *attrs* =None)
        - **Parameters**
            - **v_vals** <tuple>
            - **attrs** <dict>
    - *method* **remove_vertex** (*val*)
        - **Parameters**
            - **val** <hashable>
    - *method* **remove_edge** (*v_vals*)
        - **Parameters**
            - **v_vals** <tuple>
    - *method* **search** (*start_val*, *goal_val* =None, *method* ='breadth_first')
        - **Parameters**
            - **start_val** <hashable>
                - vertex to act as the root of the search algorithm
            - **goal_val** <hashable>
                - optional
                - if specified, the search algorithm terminates when this vertex is found
                - if not specified, the search algorithm goes through the entire graph
            - **method** <String>
                - optional (defaults to 'breadth_first')
                - one of ['breadth_first', 'depth_first']
                - specifies which search algorithm is used
        - **Returns**
            - hashable[] if *goal_val* is specified, representing the path from *start_val* to *goal_val*
            - dict mapping hashable -> hashable[] if *goal_val* is not specified, each value representing the path from *start_val* to that value's key
    - *method* **dijkstra** (*start_val*, *goal_val* =None, *return_distances* =False, *priority_queue* =PriorityQueue)
        - **Parameters**
            - **start_val** <hashable>
                - vertex to act as the root of the search algorithm
            - **goal_val** <hashable>
                - optional
                - if specified, the search algorithm terminates when this vertex is found
                - if not specified, the search algorithm goes through the entire graph
            - **return_distances** <bool>
                - optional
                - whether or not to return distances instead of full paths
            - **priority_queue** <class>
                - optional
                - specs for a suitable priority queue class can be found in the **extras** section of these docs
        - **Returns**
            - hashable[] if *goal_val* is specified, representing the path from *start_val* to *goal_val*
            - dict mapping hashable -> hashable[] if *goal_val* is not specified, each value representing the path from *start_val* to that value's key
            - if *return_distances* is True, instead of the path (hashable[]) it is just the distance (number)
            - if a vertex is not reachable from *start_val*, its path is None and its distance is `inf`

*exception* graphpy.graph.VertexAlreadyExistsException (*v*)
    - Cannot add a vertex to a graph that already has that vertex

*exception* graphpy.graph.EdgeAlreadyExistsException (*e*)
    - Cannot add an edge to a graph that already has that edge
