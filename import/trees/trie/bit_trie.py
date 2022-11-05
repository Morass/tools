# Trie for integers
class bitTrie:
    """ This is representation of one node of Trie for integers.

    Functionality:
        Insert integer
        Delete integer
        Get K-th integer
        Return size of (sub)trie

    Complexity:
        O(log(N)) per query
        O(1) initialisation

    Variables:
        total (int): Number of integers in this node
        left (bitTrie): Pointer to left node (initialised to none)
        right (bitTrie): Pointer to right node (initialised to none)
        bit (int): Number of bits in this node

    Note: Integers with highest bit on goes to right, others go to left node.
    """
    total = 0
    left = None
    right = None
    bit = None
    def __init__(self, bits: int = 32):
        """ Initialisation of one node of Trie.
        No new nodes are spawned here - it is done so when integer is added.
        Args:
            bits (int): Number of bits we are interested in
        """
        self.bit=bits

    def _mask(self) -> int:
        """ Returns mask to see only the interesting bits

        Complexity:
            O(1)

        Returns:
            int: Mask for all but first bit
        """
        return 0 if self.bit==1 else (1<<(self.bit-1))-1

    def add(self, N: int):
        """ Adds integer to actual node of Trie

        Args:
            N (int): The number we are adding to Trie

        Complexity:
            O(log(N))
        """
        self.total += 1
        # 0 bits == leaf node
        if not self.bit: return
        if not self.left: self.left = bitTrie(self.bit-1)
        if not self.right: self.right = bitTrie(self.bit-1)
        if (N>>(self.bit-1)):
            self.right.add(N&self._mask())
        else:
            self.left.add(N&self._mask())

    def delete(self, N:int):
        """ Deletes integer from actual node of Trie

        Raises:
            IndexError: Error is raised if integer is not in Trie

        Args:
            N (int): Integer which is to be deleted

        Complexity:
            O(log(N))

        Note:
            If an error is raised, the integrity for data structure is also wrong.
        """
        self.total-=1
        if self.total < 0:
            raise IndexError("Integer not found!")
        if not self.bit: return
        if self.left is None or self.right is None:
            raise IndexError("Integer not found!")
        if (N>>(self.bit-1)):
            self.right.delete(N&self._mask())
        else:
            self.left.delete(N&self._mask())

    def size(self) -> int:
        """ Returns size of (sub)trie

        Complexity:
            O(1)

        Note:
            This function is just getter for "total"

        Returns:
            int: Size of (sub)trie
        """
        return self.total

    def kth(self, K: int) -> int:
        """ Returns the K-th integer in Trie

        Complexity:
            O(bits)

        Raises:
            IndexError: Raises exception if size K is >= the size of (sub)Trie

        Returns:
            K-th integer in Trie

        Note:
            Indexed from "0"
        """
        if K >= self.size(): raise IndexError("Not enough integers in Trie")
        if not self.bit: return 0
        if K < self.left.size(): return self.left.kth(K)
        return self.right.kth(K-self.left.size())|(1<<(self.bit-1))

    def ith(self, N: int) -> int:
        """ Return the index of first occurrence of N (indexed from 0).

        Note:
            N shall be inside! Otherwise an exception is expected.

        Complexity:
            O(bits)

        Args:
            N (int): The integer we are interested in

        Returns:
            int: The index of integer "N"
        """
        if not self.bit: return 0
        if (N>>(self.bit-1)):
            return self.left.size() + self.right.ith(N&self._mask())
        return self.left.ith(N)

    def previous(self, N: int) -> int:
        """ Returns preceding element if "N" (-1 if N is first)

        Note:
            N shall be inside! Otherwise an exception is expected

        Complexity:
            O(bits)

        Args:
            N (int): Integer for which we want to get element right before it.

        Returns:
            int: The preceding element before N.
                -1 if N is first
        """
        K = self.ith(N)
        if not K:return -1
        return self.kth(K-1)

