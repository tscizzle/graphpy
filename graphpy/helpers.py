"""
Helpers for edge.py, vertex.py, and graph.py
"""
__all__ = ['is_hashable', 'keydefaultdict', 'PriorityQueue']


from collections import defaultdict


################################################################################
#                                                                              #
#                                Miscellaneous                                 #
#                                                                              #
################################################################################


def is_hashable(obj):
    try:
        hash(obj)
    except:
        return False
    else:
        return True

class keydefaultdict(defaultdict):

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


################################################################################
#                                                                              #
#                                Priority Queue                                #
#                                                                              #
################################################################################


class PriorityQueue(object):

    def __init__(self, data=None):
        """
        Each entry of self._heap, and thus the `data` parameter, is a tuple of
        the form (priority, item).

        The heap invariant

        self._heap[k] <= self._heap[2*k + 1] AND
        self._heap[k] <= self._heap[2*k + 2]

        (i.e. each node is less than its 2 children) is based on the priorities,
        so the invariant is technically

        self._heap[k][0] <= self._heap[2*k + 1][0] AND
        self._heap[k][0] <= self._heap[2*k + 2][0]

        The dictionary self._item_positions allows us to locate items in the
        heap in O(1) time. Otherwise, getting the position of an item would
        require a linear scan, which makes decrease-key slow. The pointers from
        items to indices in self._item_positions must be maintained as items
        move around in the heap.
        """
        self._heap = data or []
        # initialize the item-to-position pointers
        self._item_positions = {}
        for position, (_, item) in enumerate(self._heap):
            self._item_positions[item] = position
        # initialize the heap such that the heap invariant holds
        self._heapify()

    def __str__(self):
        return str(self._heap)

    def __len__(self):
        return len(self._heap)

    def __getitem__(self, item):
        return self._heap[self._item_positions[item]]

    def __contains__(self, item):
        return item in self._item_positions

    def _write_entry(self, entry, position):
        assert position <= len(self._heap), "Can't write past end of heap"
        _, item = entry
        n = len(self._heap)
        # if item has a previous position, mark it as no longer holding item
        if item in self._item_positions:
            old_position = self._item_positions[item]
            self._heap[old_position] = (None, None)
        # put the entry into the heap
        if position == n:
            self._heap.append(entry)
        elif position < n:
            overwritten_priority, overwritten_item = self._heap[position]
            # a priority of None signals that the position is actually empty
            if overwritten_priority is not None:
                del self._item_positions[overwritten_item]
            self._heap[position] = entry
        # point the item to its position in the heap
        self._item_positions[item] = position

    def _siftdown(self, start_position, current_position):
        # save the entry being bubbled up
        entry = self._heap[current_position]
        priority, _ = entry
        # bubble the entry up toward the root, moving parents down until finding
        # a place the entry fits
        while current_position > start_position:
            parent_position = (current_position - 1) >> 1
            parent_entry = self._heap[parent_position]
            parent_priority, _ = parent_entry
            # if the entry being bubbled up is less than the parent entry, move
            # the parent entry down and then keep going
            if priority < parent_priority:
                self._write_entry(parent_entry, current_position)
                current_position = parent_position
                continue
            # if the entry being bubbled up is not less than the parent entry,
            # stop the sift
            break
        # put the entry being bubbled up into the position found for it
        self._write_entry(entry, current_position)

    def _siftup(self, start_position):
        end_position = len(self._heap)
        entry = self._heap[start_position]
        current_position = start_position
        left_position = 2*current_position + 1 # leftmost child position
        # move up the smaller child until hitting a leaf
        while left_position < end_position:
            right_position = left_position + 1
            # find the smaller child
            left_priority, _ = self._heap[left_position]
            if right_position < end_position:
                right_priority, _ = self._heap[right_position]
            else:
                right_priority = float('inf')
            if right_priority < left_priority:
                smaller_child_position = right_position
            else:
                smaller_child_position = left_position
            # move the smaller child up
            smaller_child_entry = self._heap[smaller_child_position]
            self._write_entry(smaller_child_entry, current_position)
            current_position = smaller_child_position
            left_position = 2*current_position + 1
        # the leaf current_position is empty now.  put the entry there, and
        # bubble it up to its final resting place (by sifting its parents down)
        self._write_entry(entry, current_position)
        self._siftdown(start_position, current_position)

    def _heapify(self):
        n = len(self._heap)
        # from the bottom up, sift elements up into place
        # only need to position non-leaf nodes, so the first n//2 will do
        for position in reversed(xrange(n//2)):
            self._siftup(position)

    def find_min(self):
        return self._heap[0]

    def pop_min(self):
        arbitrary_leaf_entry = self._heap.pop()
        _, arbitrary_leaf_item = arbitrary_leaf_entry
        del self._item_positions[arbitrary_leaf_item]
        # if was not the last element, put the arbitrary leaf at the root, and
        # siftup into the root
        if len(self._heap) > 0:
            min_item = self._heap[0]
            self._write_entry(arbitrary_leaf_entry, 0)
            self._siftup(0)
        # if was the last element, simply return it
        else:
            min_item = arbitrary_leaf_entry
        return min_item

    def insert(self, item, priority):
        # make sure the item doesn't already exist
        if item in self._item_positions:
            raise ValueError("Duplicate item %s" % (item,))
        # add the item to the end of the heap
        entry = (priority, item)
        last_position = len(self._heap)
        self._write_entry(entry, last_position)
        # siftdown into the new position
        self._siftdown(0, last_position)

    def decrease_key(self, item, new_priority):
        # make sure the new priority would actually be a decrease
        current_priority, _ = self[item]
        if new_priority > current_priority:
            err_args = (new_priority, current_priority)
            raise ValueError("%s is greater than %s" % err_args)
        # set the new priority for the item
        position = self._item_positions[item]
        new_entry = (new_priority, item)
        self._write_entry(new_entry, position)
        # bubble the newly decreased entry up by sifting down its parents
        self._siftdown(0, position)
