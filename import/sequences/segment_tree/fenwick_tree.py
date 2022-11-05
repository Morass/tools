# Fenwick Tree
class FenwickTree:
    """ Data structure for logarithmic segment question for sum.

        Variables:
            tree (list[int]): The tree structure containing all the prefix sums.
            size (int): The number of element the tree contains (0 -> size-1)
    """
    tree = None
    size = None
    def __init__(self, size: int):
        """ Initialisation of the data structure for size elements

        Complexity:
            O(size)

        Args:
            size (int): The maximal element of the data structure.
        """
        self.size = size +1
        self.tree = [0]*(self.size)

    def increase(self, index: int, value: int = 1):
        """ Increase the value on "index" by "value".

        Args:
            index (int): The index of element we are increasing.
            value (int): The value by which we are increasing the element.
                Defaults to 1.

        Complexity:
            O(log(size))
        """
        while index < self.size:
            self.tree[index]+=value
            index|=index+1

    def prefix_sum(self, index: int) -> int:
        """ Return the sum of values on indices 0 to "index".

        Args:
            index (int): The last element of prefix sum we want to obtain.

        Returns:
            int: The prefix sum of elements from 0 to "index.

        Complexity:
            O(log(size))
        """
        total = 0
        while index != -1:
            total+=self.tree[index]
            index&=index+1
            index-=1
        return total

    def segment_sum(self, begin: int, end: int) -> int:
        """ Return the sum of values on indices "begin" to "end".

        Args:
            begin (int): The first index of segmental sum.
            end (int): The last index of segmental sum.

        Returns:
            int: The value of sum from "begin" to "end"

        Complexity:
            O(log(size))

        Note:
            This functions uses difference of two prefix_sum(s): [end] - [begin-1].
        """
        return self.prefix_sum(end) - self.prefix_sum(begin-1)

