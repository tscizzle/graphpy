Graphpy
=======

.. image:: https://travis-ci.org/tscizzle/graphpy.svg?branch=master
    :target: https://travis-ci.org/tscizzle/graphpy

.. image:: http://readthedocs.org/projects/graphpy/badge/?version=latest
    :target: http://graphpy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/tscizzle/graphpy/badge.svg?branch=master
    :target: https://coveralls.io/github/tscizzle/graphpy?branch=master

.. image:: https://badge.fury.io/py/graphpy.svg
    :target: https://badge.fury.io/py/graphpy

A Python implementation of edges, vertices, and graphs


Use
---

There are two types of each object: ``Undirected`` and ``Directed``.

To begin, import one of the graph classes::

    from graphpy.graph import UndirectedGraph

and create a graph from a dictionary of vertex vals::

    # graph with vertices 'v0' and 'v1', with an edge between them

    g = UndirectedGraph.from_dict({'v0': [('v1',)],
                                   'v1': []})

or from a list of vertices and a list of edges::

    g = UndirectedGraph.from_lists([('v0',), ('v1',)],
                                   [('v0', 'v1')])

You can also initialize a graph, then add vertices and edges::

    g = UndirectedGraph()

    g.add_vertex('v0')
    g.add_vertex('v1')
    g.add_edge(('v0', 'v1'))

A vertex's val can be any hashable object, like a string, int, tuple, etc.::

    # graph with vertices 'v0', 1, and (2, 2), with some edges

    g = UndirectedGraph.from_dict({'v0': [(1,)],
                                   1: [('v0',), ((2, 2),)],
                                   (2, 2): [(1,)]})

Retrieve vertex and edge objects::

    # v is an UndirectedVertex object, and e is an UndirectedEdge object

    v = g.get_vertex('v0')
    print v.degree

    e = g.get_edge(('v0', 'v1'))
    print e.vertices

Iterate through a graph's vertices::

    for v in g:
        print v

Perform graph algorithms, such as search::

    paths = g.search(start='v0', method='depth_first')
    print paths

Create graphs with vertices and edges that have whatever attributes you want (for example, edge weights)::

    g = UndirectedGraph.from_lists([('v0', {'city': 'Paris'}), ('v1', {'city': 'London'})],
                                   [('v0', 'v1', {'weight': 5})])

From there, use graphs to model situations, implement more graph algorithms, and whatever else you desire. And, as always, have fun!

(The tests found on Github at https://github.com/tscizzle/graphpy/tree/master/tests give many more examples and showcase the rest of the library's functionality.)

Documentation
-------------

Find the full documentation at: http://graphpy.readthedocs.org/en/latest

Installation
------------

If you don't have pip, get pip at: https://pip.pypa.io/en/stable/installing

Run the command ``pip install graphpy`` in your terminal to get the graphpy library.

To test your installation, start a Python interpreter with the ``python`` command in your terminal and make sure you can run ``import graphpy`` in it without getting an error.

Contribute
----------

Find the code on Github at: https://github.com/tscizzle/graphpy

Support
-------

Contact me (Tyler Singer-Clark) at tscizzle@gmail.com with any questions or concerns.

License
-------

The project is licensed under the MIT license.
