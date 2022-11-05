# Dynamic Prefix sum -> first queries, then precalculations
class prefixSumDynamic:
    """ Data structure which can accept several queries "begin -> end: add value" and then produces prefix sum of such array.

    Requires:
        import prefixSum

    Variables:
        additions (list[int]): Temporal list with additions at the beginning and (negation) fter end of segment.
    """
    additions = None
    def __init__(self, size: int):
        """ Initialise "additions" by an empty array.

        Note:
            The size will be "size + 1" so we can place negation at the end of array.

        Complexity:
            O(size)

        Args:
            size (int): The size of array.
        """
        self.additions = [0]*(size+1)

    def add(self, begin: int, end: int, value: int = 1):
        """ Adds "value" to segment "begin" -> "end".

        Complexity:
            O(1)

        Args:
            begin (int): Start of segment to which we are adding value.
            end (int): End of segment to which we are adding value.
            value (int): Value we are adding to the segment. Defaults to 1.
        """
        self.additions[begin] += value
        self.additions[end+1] -= value

    def get_prefix_sum(self) -> prefixSum:
        """ Creates prefixSum data structure from queries added till this moment.

        Complexity:
            O(size)

        Returns:
            prefixSum: Prefix sum of arrays with calculated queries.

        Note:
            The size of prefix sum is same as original "size" in constructor (i.e. 1 lesser then additions array)
        """
        length = len(self.additions) - 1
        array = [0]*length
        array[0] = self.additions[0]
        for index in range(1, length):
            array[index] = array[index - 1] + self.additions[index]
        return prefixSum(array) Dynamic Prefix sum -> first queries, then precalculations
class prefixSumDynamic:
    """ Data structure which can accept several queries "begin -> end: add value" and then produces prefix sum of such array.

    Requires:
        import prefixSum

    Variables:
        additions (list[int]): Temporal list with additions at the beginning and (negation) fter end of segment.
    """
    additions = None
    def __init__(self, size: int):
        """ Initialise "additions" by an empty array.

        Note:
            The size will be "size + 1" so we can place negation at the end of array.

        Complexity:
            O(size)

        Args:
            size (int): The size of array.
        """
        self.additions = [0]*(size+1)

    def add(self, begin: int, end: int, value: int = 1):
        """ Adds "value" to segment "begin" -> "end".

        Complexity:
            O(1)

        Args:
            begin (int): Start of segment to which we are adding value.
            end (int): End of segment to which we are adding value.
            value (int): Value we are adding to the segment. Defaults to 1.
        """
        self.additions[begin] += value
        self.additions[end+1] -= value

    def get_prefix_sum(self) -> prefixSum:
        """ Creates prefixSum data structure from queries added till this moment.

        Complexity:
            O(size)

        Returns:
            prefixSum: Prefix sum of arrays with calculated queries.

        Note:
            The size of prefix sum is same as original "size" in constructor (i.e. 1 lesser then additions array)
        """
        length = len(self.additions) - 1
        array = [0]*length
        array[0] = self.additions[0]
        for index in range(1, length):
            array[index] = array[index - 1] + self.additions[index]
        return prefixSum(array)
