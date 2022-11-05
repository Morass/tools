# HopcroftCarp - MaximumMatching algorithm
from collections import deque
class HopcroftCarp:
    """ Hopcroft-Carp algorithm for maximum matching.

    Note:
        The class uses "old graph representation" with "next" array.
        We also call the disjunct sets "left" and "right". Here "left" subset is source (yet it shall not matter).
        Sink is in node "0".

    Complexity:
        O(Nsqrt(N))

    Variables:
        next_edge (list[int]): Index of "next" edge with same index.
        target (list[int]): The node in second subset to which edge leads.
        graph (list[int]): Index of "last" edge for each node.
        left_subset_size (int): Maximal size of left subset.
        right_subset_size (int): Maximal size of right subset.
        pair (list[int]): List of pairs (nodes).
        layer (list[int]): List with marks of time of visited nodes (considering "back-edges") --> distance.
        infinite (int): A mark for layers indicating non-visited nodes.
    """
    next_edge = None
    target = None
    graph = None
    left_subset_size = None
    right_subset_size = None
    pair = None
    layer = None
    unseen = int(1e9)
    def __init__(self, left_size: int, right_size: int):
        """ Initializes data structure - lists and sizes.

        Args:
            left_size (int): Number of nodes in left subset.
            right_size (int): Number of nodes in right subset.

        Complexity:
            O(1)
        """
        self.left_subset_size = left_size
        self.right_subset_size = right_size
        total = left_size + right_size + 1
        self.next_edge = []
        self.target = []
        self.graph = [-1]*total
        self.pair = [0]*total
        self.layer = [0]*total

    #TODO: Init from same
    def add_edge(self, left: int, right: int):
        """ Connects left/right subsets by an edge.

        Args:
            left (int): Node from left subset (indexed from 0).
            right (int): Node from right subset (indexed from 0).

        Complexity:
            O(1)
        """
        left += 1
        right += self.left_subset_size + 1
        self.next_edge.append(int(self.graph[left]))
        self.graph[left]=len(self.target)
        self.target.append(right)

    def bfs(self) -> bool:
        """ Partitions the vertices of the graph into layers.

        Complexity:
            O(N)

        Returns:
            bool: True, if we got into sink (i.e. found augmenting path).
        """
        queue = deque()
        self.layer[0] = self.unseen
        # Note: Some of the nodes might be already visisted.
        for i in range(1,self.left_subset_size + 1):
            if self.pair[i]:
                self.layer[i] = self.unseen
            else:
                self.layer[i] = 0
                queue.append(i)
        while len(queue):
            node = queue.popleft()
            edge = self.graph[node]
            while edge != -1:
                paired = self.pair[self.target[edge]]
                if self.layer[paired] == self.unseen:
                    self.layer[paired] = self.layer[node] + 1
                    queue.append(paired)
                edge = self.next_edge[edge]
        return self.layer[0] != self.unseen

    def dfs(self, node: int):
        """ Depth First Search from "left" subset to "sink", searching for augmenting paths.

        Args:
            node (int): Node from which we are spreading.

        Returns:
            bool: True if we found augmenting path.

        Complexity:
            O(N) -- Note that it is also O(N) for while "dfs-round".
        """
        if not node: return True
        edge = self.graph[node]
        while edge != -1:
            target = self.target[edge]
            paired = self.pair[target]
            if self.layer[paired] == self.layer[node] + 1 and self.dfs(paired):
                self.pair[target] = node
                self.pair[node] = target
                return True
            edge = self.next_edge[edge]
        self.layer[node] = self.unseen
        return False

    def maximum_matching(self) -> int:
        """ Find maximum matching between subsets "left" and "right".

        Returns:
            int: The maximum possible matching.

        Complexity:
            O(Nsqrt(N))
        """
        matching = 0
        while self.bfs():
            for i in range(1, self.left_subset_size + 1):
                if not self.pair[i] and self.dfs(i):
                    matching += 1
        return matching

