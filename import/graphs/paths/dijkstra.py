# Shortest Path: Dijkstra
from heapq import heappush, heappop
class dijkstra:
    """ Dijkstra's shortest path algorithm.

            - Create graph
            - Start algorithm from a start node.
            - Query path length

        Variables:
            graph (list[tuple]): Edges to neighbors (with values).
            parent (list[int]): The parent of each edge during algorithm.
            seen (list[int]): Length from "start" to "node"
            size (int): Number of nodes in graph
    """
    graph = None
    parent = None
    seen = None
    size = None
    def __init__(self, size: int):
        """ Initialisation of class -- creates empty lists of edges.

        Complexity:
            O(size)

        Args:
            size (int): Size of list
        """
        self.size = size
        self.graph = [list() for _ in range(size)]

    def add_uni(self, begin: int, end: int, price: int):
        """ Adds uni-directional edge to the graph

        Args:
            begin (int): Start of the edge.
            end (int): End of the edge.
            price (int): Price of the travel through the edge.

        Complexity:
            O(1)
        """
        self.graph[begin].append((end, price))

    def add_bi(self, first: int, second: int, price: int):
        """ Adds bi-directional edge to the graph

        Args:
            first (int): Start/end of the edge.
            second (int): End/start of the edge.
            price (int): Price of the travel through the edge.

        Complexity:
            O(1)
        """
        self.add_uni(first, second, price)
        self.add_uni(second, first, price)

    def search(self, start: int, operation = lambda a, b: a + b):
        """ Process the graph from start. Find the shortest distance to each possible node.

        Args:
            start (int): The node from which we spread
            operation (function)

        Complexity:
            O(Nlog(M))
        """
        self.parent = [-1]*self.size
        self.seen = [None]*self.size
        p_queue = []
        S = 1
        heappush(p_queue, (0, start))
        self.seen[start] = 0
        while S:
            price, node = heappop(p_queue)
            S-=1
            if self.seen[node] != price: continue
            for neighbor, value in self.graph[node]:
                if self.seen[neighbor] is None or self.seen[neighbor] > operation(price, value):
                    self.parent[neighbor] = node
                    self.seen[neighbor] = operation(price, value)
                    S+=1
                    heappush(p_queue, (operation(price, value), neighbor))

    def path_length(self, destination: int, bad = None) -> int:
        """ Obtains the length of path from "start" to "destination"

        Args:
            destination (int): The final node to which the length is to be obtained.

        Complexity:
            O(1)

        Returns:
            int: Length of path from "start" to "destination".
                None is returned if there is no path.
        """
        if self.seen[destination] is None: return bad
        return self.seen[destination]

