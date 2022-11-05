# Minimum Spanning Tree O(Nlog(N))
# REQUIRES UNION FIND!!!
class MST:
    """ Minimum spanning tree.

        Variables:
            edges (list[tuple]): Edges of the graph.
            size (int): Size of the graph

        Note:
            The graph is indexed from 0.
    """
    edges = None
    size = None
    def __init__(self, size: int):
        """ Initialisation of edges list.

        Complexity:
            O(1)

        Args:
            size (int): Size of the graph (number of nodes).
        """
        self.size = size
        self.edges = []

    def add_edge(self, first: int, second: int, value: int):
        """ Adds edge (with a price) to the graph.

        Args:
            first (int): One of the edges of the graph.
            second (int): Second edge of the graph.
            value (int): Price to travel through the edge.

        Note:
            The function accepts bidirectional edges.

        Complexity:
            O(1)
        """
        self.edges.append((value, first, second))

    def kruskal(self) -> tuple:
        """ Processes Kruskal's algorithm on edges obtaining minimal tree and its weight.

        Complexity:
            O(Elog(E))

        Returns:
            tuple[list, int]: Pair with tree (as list of lists) and its weight.
        """
        self.edges.sort()
        dfu = unionFind(self.size)
        graph = [list() for _ in range(self.size)]
        total = 0
        for p, a, b in self.edges:
            if dfu.connect_nodes(a, b):
                graph[a].append((b,p))
                graph[b].append((a,p))
                total += p
        return graph, total

