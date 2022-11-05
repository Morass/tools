# Segment tree - it is possible to "ADD" segment to a value
class SegmentTreeAdd:
    """ In this segment tree it is possible to add a value to a segment and then query segments with respect to stored functions.

                operation: Function which evaluates two different elements
                operation_long: Functions which evaluates addition to K consecutive elements.
                size: Maximal number of elements (power of 2)
                neutral: Item which has no impact on operation (i.e. 0 for SUM or -INF for MAX)
                val: Value in each node
                lazy: Lazily propagated sum in each node.
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
            foo (lambda(int, int)): Returns result of operation on two input values
            foo_large(int, int, int): Returns operation of addition "X" to  "N" consecutive elements of type int
            inf (int): Element which does not mangle the result of operation (neutral item)
        """
        self.operation = foo
        self.operation_long = foo_large
        self.neutral = inf
        from math import log2
        self.size = 1<<(int(log2(N)-1e-9)+1)
        self.val = [inf for _ in range(self.size*2)]
        self.lazy = [0] * (self.size*2)

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
        size = last - first + 1
        return self.operation_long(self.val[node], self.lazy[node], size)


    def add(self, begin: int, end: int, value: int):
        """ Adds value to segment begin -> end to value

        Args:
            begin (int): First node of segment .
            end (int): Last node of segment.
            value (int): The value to which they are to be added.

        Complexity:
            O(log(size))
        """
        self._add(begin, end, value, 1, 0, self.size-1)

    def add_one(self, element: int, value: int):
        """ Sets an "element" to "value"

        Args:
            element (int): Node to be added.
            value (int): The value to which they are to be added.

        Complexity:
            O(log(size))
        """
        self.add(element, element, value)

    def add_different(self, elements: list):
        """ Sets first len(elements) elements to value in elements.

        Args:
            elements (list[int]): Values of first list(elements) elements

        Complexity:
            O(len(elements*log(len(elements)))
        """
        for i, val in enumerate(elements):
            self.add_one(i, val)

    def _add(self, begin: int, end: int, value: int, node: int, first: int, last: int):
        """ Private function which is not meant to be used directly yet called by all "setters".

        Args:
            begin (int): First element in segment to be set.
            end (int): Last element in segment to be set.
            value (int): The value to which they are to be set.
            node (int): The actual node number
            first (int): First element in segment under control of node.
            last (int): Last element in segment under control of node.

        Complexity:
            O(log(size))
        """
        # The control of node does not range of segment
        if first > end or last < begin: return
        if begin <= first and end >= last:
            self.lazy[node] += value
            return
        self._add(begin, end, value, node*2, first, (first+last)//2)
        self._add(begin, end, value, node*2 + 1, (first+last)//2 +1, last)
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
            int: The evaluated segment "begin" -> "end"
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
            int: The evaluated segment "begin" -> "end"
        """
        if last < begin or first > end: return self.neutral
        if first >= begin and last <= end: return self._get_one(node, first, last)
        result = self.operation(self._get(begin, end, node*2    , first, (first+last)//2),
                                self._get(begin, end, node*2 + 1, (first + last)//2 + 1, last))
        return self.operation_long(result, self.lazy[node], min(end, last) - max(begin, first) + 1)

    @classmethod
    def addition_segment_tree(context: SegmentTreeAdd, N: int) -> SegmentTreeAdd:
        """ Creates Segment Tree for operation "maximum"

        Args:
            N (int): Minimal size of segment tree

        Returns:
            SegmentTreeAdd: Initialised SegmentTreeAdd with "maximum" as desired operation
        """
        return context(N, lambda a, b: a + b, lambda a, b, l: a + b*l)

