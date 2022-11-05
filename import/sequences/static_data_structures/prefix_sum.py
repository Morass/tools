# Prefix sum
from __future__ import annotations
class prefixSum:
    """ Class for prefix sums of an array with fast queries on given range

    Variables:
        prefix_sum (list): Array with prefix sums created from input array

    Complexity:
        O(N): Initialisation
        O(1): Query
    """
    prefix_sum = None

    def __init__(self, array: list):
        """ Initialisation of prefix sum

        Args:
            array (list[int]): List of integers whose sum is to be calculated

        Complexity:
            O(N)
        """
        length = len(array)
        self.prefix_sum = [0]*length
        self.prefix_sum[0] = array[0]
        for i in range(1, length):
            self.prefix_sum[i] = self.prefix_sum[i-1] + array[i]

    def get(self, begin: int, end: int) -> int:
        """ Gets the sum on array between "begin" and "end" (inclusive).

        Args:
            begin (int): First element of array to be taken into account
            end (int): Last element of array to be taken into account

        Complexity:
            O(1)

        Returns:
            int: The sum on range "begin" to "end"
        """
        if begin > end: return 0
        if not begin: return self.prefix_sum[end]
        return self.prefix_sum[end] - self.prefix_sum[begin-1]

    @classmethod
    def from_string(cls, string: str, char: str) -> prefixSum:
        """  Creates prefix sum from string where all characters equal to "char" will be "1" and the others zeroes.

        Args:
            string (str): Input string over which the prefix sum will be done
            char (str): Characters which will be represented as "1" in the string

        Complexity:
            O(len(string))

        Returns:
            prefixSum: Class initialised with "1" on indices of "char" and "0" elsewhere
        """
        return cls([1 if c == char else 0 for c in string])


