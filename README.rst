Graphpy
=======

A Python implementation of edges, vertices, and graphs

Use
---

There are two types of each object: ``Undirected`` and ``Directed``.

To begin, create a graph from a dictionary of vertex names::

    from graphpy.graph import UndirectedGraph

    g = UndirectedGraph.from_dict({'v0': ['v1'],
                                   'v1': []})

You can also initialize a graph, then add vertices and edges::

    from graphpy.edge import UndirectedEdge
    from graphpy.vertex import UndirectedVertex
    from graphpy.graph import UndirectedGraph

    g = UndirectedGraph()
    v0 = UndirectedVertex(name='v0')
    v1 = UndirectedVertex(name='v1')

    g.add_vertex(v0)
    g.add_vertex(v1)
    g.add_edge(v0, v1)

Index into a graph using the name of a vertex to retrieve a vertex object::

    v = g['v0']
    print v.degree

Perform graph algorithms, such as search::

    paths = g.search(start=v, method='depth_first')
    print paths

From there, use graphs to model situations, implement more graph algorithms, and whatever else you desire. And as always have fun!

(The tests found on Github at https://github.com/tscizzle/graphpy give many more examples and showcase the rest of the library's functionality.)

Documentation
-------------

Docs will be up on ReadTheDocs soon.

Installation
------------

Run the command ``pip install graphpy`` in your terminal.

To test your installation, start a Python interpreter with the ``python`` command and make sure you can run ``import graphpy`` in it without getting an error.

Contribute
----------

Find the code at: https://github.com/tscizzle/graphpy

Support
-------

Contact me (Tyler Singer-Clark) at tscizzle@gmail.com with any questions or concerns.

License
-------

The project is licensed under the MIT license.
