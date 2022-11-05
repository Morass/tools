# Segment tree - it is possible to "SET" segment to a value
class SegmentTreeSet:
    """ In this segment tree it is possible to set a segment onto a value and then query segments with respect to stored functions.

                operation: Function which evaluates two different elements
                operation_long: Functions which evaluates one element applied for K consecutive fields
                size: Maximal number of elements (power of 2)
                neutral: Item which has no impact on operation (i.e. 0 for SUM or -INF for MAX)
                val: Value in each node
                lazy: Lazily propagated value in each node
    """
    operation = None
    operation_long = None
    size = 0
    neutral = 0
    val = None
    lazy = None
    def __init__(self, N: int, foo, foo_large, inf=0):
        """ Initialises segment tree to size which is power of 2 larger then N

        Args:
            N(int): Minimal size of segment tree necessary
            foo (lambda(_T, _T)): Returns result of operation on two input values
            foo_large(_T, int): Returns operation result on "N" consecutive elements of type _T
            inf (_T): Element which does not mangle the result of operation (neutral item)
        """
        self.operation = foo
        self.operation_long = foo_large
        self.neutral = inf
        from math import log2
        self.size = 1<<(int(log2(N)-1e-9)+1)
        self.val = [inf for _ in range(self.size*2)]
        self.lazy = [None] * (self.size*2)

    def _get_one(self, node: int, first: int, last: int):
        """Returns value in node

        Args:
            node(int): Index of node.
            first(int): First element covered by node.
            last(int): Last element covered by node.

        Note:
            This is internal function, do not use it without any knowledge!

        Complexity:
            O(1)
        """
        return self.val[node] if self.lazy[node] is None else self.operation_long(self.lazy[node], last-first+1)


    def set(self, begin: int, end: int, value):
        """ Sets segment begin -> end to value

        Args:
            begin (int): First node to be set.
            end (int): Last node to be set.
            value (_T): The value to which they are to be set.

        Complexity:
            O(log(size))
        """
        self._set(begin, end, value, 1, 0, self.size-1)

    def set_one(self, element: int, value):
        """ Sets an "element" to "value"

        Args:
            element (int): Node to be set.
            value (_T): The value to which they are to be set.

        Complexity:
            O(log(size))
        """
        self.set(element, element, value)

    def set_different(self, elements: list):
        """ Sets first len(elements) elements to value in elements.

        Args:
            elements (list[_T]): Values of first list(elements) elements

        Complexity:
            O(len(elements*log(len(elements)))
        """
        for i, val in enumerate(elements):
            self.set_one(i, val)

    def _set(self, begin: int, end: int, value, node: int, first: int, last: int):
        """ Private function which is not meant to be used directly yet called by all "setters".

        Args:
            begin (int): First element in segment to be set.
            end (int): Last element in segment to be set.
            value (_T): The value to which they are to be set.
            node (int): The actual node number
            first (int): First element in segment under control of node.
            last (int): Last element in segment under control of node.

        Complexity:
            O(log(size))
        """
        # The control of node does not range of segment
        if first > end or last < begin: return
        if begin <= first and end >= last:
            # Leaf case
            if first == last:
                self.val[node] = value
            else:
                self.lazy[node] = value
            return
        if not (self.lazy[node] is None):
            self._set(first, last, self.lazy[node], node*2, first, (first+last)//2)
            self._set(first, last, self.lazy[node], node*2+1, (first+last)//2 +1, last)
            self.val[node] = self.operation_long(self.lazy[node], first, last)
            self.lazy[node] = None
        self._set(begin, end, value, node*2, first, (first+last)//2)
        self._set(begin, end, value, node*2 + 1, (first+last)//2 +1, last)
        self.val[node] = self.operation(self._get_one(node*2, first, (first+last)//2),
                                        self._get_one(node*2 + 1, (last-first)//2 + 1, last))

    def get(self, begin: int, end: int):
        """ Gets value from segment begin -> end

        Args:
            begin (int): First node of getter.
            end (int): Last node of getter.

        Complexity:
            O(log(size))

        Returns:
            _T: The evaluated segment "begin" -> "end"
        """
        return self._get(begin, end, 1, 0, self.size-1)

    def _get(self, begin: int, end: int, node: int, first: int, last: int):
        """ Private function which is not meant to be used directly yet called by all "getters".

        Args:
            begin (int): First element in segment to be set.
            end (int): Last element in segment to be set.
            node (int): The actual node number
            first (int): First element in segment under control of node.
            last (int): Last element in segment under control of node.

        Complexity:
            O(log(size))

        Returns:
            _T: The evaluated segment "begin" -> "end"
        """
        if last < begin or first > end: return self.neutral
        if first >= begin and last <= end: return self._get_one(node, first, last)
        if not (self.lazy[node] is None):
            return self.operation_long(lazy[node], min(last, end)-max(first, begin) + 1)
        return self.operation(self._get(begin, end, node*2    , first, (first+last)//2),
                              self._get(begin, end, node*2 + 1, (first + last)//2 + 1, last))

    @classmethod
    def max_segment_tree(context: SegmentTreeSet, N: int) -> SegmentTreeSet:
        """ Creates Segment Tree for operation "maximum"

        Args:
            N (int): Minimal size of segment tree

        Returns:
            SegmentTreeSet: Initialised SegmentTreeSet with "maximum" as desired operation
        """
        return context(N, max, lambda a, l: a, inf=-int(1e18))
