# Graph algorithm BFS to find fastest path from "X" to "Y" (edges have value 1)
class BFS:
    """ Class to search for shortest path from source to destination.

            g: graph
            size: Number of nodes
            seen: Length from source (-1 if there is no path)
            parent: parent node from which we got to i (not it might note be unique, just one is stored)
    """
    g = None
    size = 0
    seen = None
    parent = None
    def __init__(self, N: int):
        """ Initialises class -> preparation of empty graph
            Initialisation is done from 0 to N inclusive

        Args:
            N (int): Size of graph
        """
        self.size = N + 1
        self.g = [[] for _ in range(self.size)]

    def add_uni(self, a: int, b: int):
        """ Adds unidirectional edge from a -> to b

        Args:
            a (int): source node
            b (int): destination node

        Complexity:
            O(1)
        """
        self.g[a].append(b)

    def add_bi(self, a:int, b:int):
        """ Adds bidirectional edge from a -> to b and vice versa.

        Args:
            a (int): source/destination node
            b (int):source/destination node

        Complexity:
            O(1)
        """
        self.add_uni(a,b)
        self.add_uni(b,a)

    def bfs(self, source: int):
        """ Searches shortest path from source

        Args:
            source (int): Starting node

        Complexity:
            O(E+N), E stands for number of edges

        Returns:
            int: Length of shortest path from "source" to "destination"
        """
        # Import of queue
        from collections import deque
        self.parent = [-1]*self.size
        self.seen = [-1]*self.size
        self.seen[source] = 0
        Q = deque()
        Q.append(source)
        E = 1
        while E:
            node = Q.popleft()
            E -= 1
            for h in self.g[node]:
                if self.seen[h] == -1:
                    self.seen[h] = self.seen[node] + 1
                    self.parent[h] = node
                    Q.append(h)
                    E += 1

    def path_length(self, destination: int) -> int:
        """ Returns length from (previously calculated) source.

        Args:
            destination (int): Node for which we want to know the distance.

        Complexity:
            O(1)

        Returns:
            int: Distance from "source" to "destination"
                -1 if there is no path
        """
        return self.seen[destination]

    def shortest_path(self, destination: int) -> list:
        """ Returns list with nodes including shortest path from start to destination.

        Note:
            BFS must be proceeded before

        Note:
            There might be multiple paths but only one is returned. It prefers edges which were added earlier.

        Complexity:
            O(|path_length|)

        Args:
            destination (int): Last in in path from "start".

        Returns:
            list[int]: One of the shortest paths from "start" to "end".
        """
        path = []
        while self.parent[destination] != -1:
            path.append(destination)
            destination = self.parent[destination]
        path.append(destination)
        path.reverse()
        return path

