# Loncest Common Subsequence
class LCS:
    """ Finds longest common subsequence and its length.
        As there might be multiple such sequences, the one which fits comparator is chosen.

    Variables:
        lcs (list(list(int)): Table with length(s) of longest common subsequence.
        chosen (list(list(tuple))): List with chosen element and indices - where it is found.
        length_first (int): Size of first string.
        length_second (int): Size of second string.

    Complexity:
        O(N*M) - where N/M are sizes of input lists/strings.
    """
    lcs = None
    chosen = None
    length_first = None
    length_second = None
    def __init__(self, first, second, operator = lambda a, b: a < b):
        """ Calculates Longest Common Subsequence of two lists/strings

        Args:
            first (_T): List or string with "some" comparable object inside.
            second (_T): Another list or string with "some" comparable object inside.
            operator (<function(a, b)>): Comparator of two objects "_T" --> in case of two similar subsequences the one with "True" will be chosen.
                defaults = lesser, finds lowest LCS.

        Complexity:
            O(|first| * |second|) - || stands for size.

        Note:
            It is done over reversed strings.
        """
        # This is done due to the operator.
        first = list(reversed(first))
        second = list(reversed(second))
        self.length_first, self.length_second = len(first), len(second)
        self.lcs = [[0]*(self.length_second+1) for _ in range(self.length_first+1)]
        self.chosen = [[(0,(0, 0))]*(self.length_second+1) for _ in range(self.length_first+1)]
        for i in range(1, self.length_first + 1):
            for j in range(1, self.length_second + 1):
                if first[i-1] == second[j-1]:
                    self.lcs[i][j] = self.lcs[i-1][j-1] + 1
                    self.chosen[i][j] = (first[i-1],(i-1, j-1))
                else:
                    self.lcs[i][j] = max(self.lcs[i-1][j], self.lcs[i][j-1])
                    if self.lcs[i-1][j] == self.lcs[i][j-1]:
                        if operator(self.chosen[i-1][j][0], self.chosen[i][j-1][0]):
                            self.chosen[i][j] = self.chosen[i-1][j]
                        else:
                            self.chosen[i][j] = self.chosen[i][j-1]
                    elif self.lcs[i-1][j] > self.lcs[i][j-1]:
                        self.chosen[i][j] = self.chosen[i-1][j]
                    else:
                        self.chosen[i][j] = self.chosen[i][j-1]

    def get_lcs_length(self) -> int:
        """ Get the calculated Longest Common Subsequence.

        Returns:
            int: Size of longest common subsequence

        Complexity:
            O(1)
        """
        return self.lcs[self.length_first][self.length_second]

    def get_lcs(self) -> list:
        """ Gets Longest Common Subsequence which fulfills the operator.

        Returns:
            list: List with type _T of objects of the longest common subsequence.

        Complexity:
            O(N)

        Note:
            List is returned even though it was done above a string.
            TODO: Do it again with "type" when needed?!
        """
        result = []
        I, J = self.length_first, self.length_second
        while I > 0 and J > 0 and self.chosen[I][J][1] != (0, 0):
            result.append(self.chosen[I][J][0])
            I, J = self.chosen[I][J][1]
        return result

