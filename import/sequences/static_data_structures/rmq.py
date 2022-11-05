# RMQ - Range minimum/maximum query
class RMQ:
    """ Range minimum/maximum query:
            Static data structure which allows questions for segment onto an operation.

        Variables:
            operation (<function with two parameters>): Must be an operation where two segments can cover (i.e. min/max but not sum)
            logarithms (list[int]): List of logarithms - i.e. showing to which group the number belongs.
            rmq (list[list[int]]): The 2D list which preprocessed operation query for each logarithmic length.
        Complexity:
            Pre-process: O(NlogN)
            Query:       O(1)
            Memory:      O(NlogN)
    """
    operation = None
    logarithms = None
    rmq = None
    def __init__(self, array: list, operation = min):
        """ Prepares "RMQ" array.

        Args:
            array (list[int]): List with integers
            operation (<function>(int, int)): Function for queries.

        Complexity:
            O(NlogN)
        """
        self.operation = operation
        power = 1
        size = len(array)
        while (1 << power) <= size:
            power += 1
        max_size = 1 << power
        self.logarithms = [0]*max_size
        logarithm = 0
        for i in range(2, max_size):
            if not (i & (i-1)):
                logarithm += 1
            self.logarithms[i] = logarithm
        self.rmq = [[0]*max_size for _ in range(power+2)]
        self.rmq[0] = list(array)
        for k in range(1, power):
            for i in range(size + 1 - (1<<k)):
                self.rmq[k][i] = operation(self.rmq[k-1][i], self.rmq[k-1][i+(1<<(k-1))])

    def query(self, begin: int, end: int) -> int:
        """ Returns result of operation on range "begin" -> "end".

        Args:
            begin (int): First element of queried segment.
            end (int): Last element of queried segment.

        Returns:
            int: Result of operation on queried segment.

        Complexity:
            O(1)
        """
        logarithm = self.logarithms[end - begin + 1]
        return self.operation(self.rmq[logarithm][begin], self.rmq[logarithm][end-(1<<logarithm)+1])

