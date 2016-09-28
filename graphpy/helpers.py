"""
Helpers for edge.py, vertex.py, and graph.py
"""


def is_hashable(val):
    try:
        hash(val)
    except:
        return False
    else:
        return True
