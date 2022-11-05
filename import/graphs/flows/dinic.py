from collections import deque
class dinic:
    """ Maximum-Flow Dinic's algorithm

        Variables:
            size (int): Number of nodes of the graph.
            graph (list[list[edge]]): List of edges for each node.
            source (int): Source node.
            sink (int): Sink node.
            last_edge (list[int]): The last edge owned by a node.
    """
    class Edge:
        """ Named tuple (not constant)
            Variables:
                neighbor (int): The destination of the edge.
                pair (int): The index of the edge which goes backward.
                    (graph[neighbor][pair])
                capacity (int): The maximal capacity of the edge.
                flow (int): The flow which goes through the edge.
        """
        neighbor = None
        flow = None
        capacity = None
        pair = None
        def __init__(self, neighbor: int, pair: int, capacity: int = 1, flow: int = 0):
            self.neighbor, self.pair, self.capacity, self.flow = neighbor, pair, capacity, flow
    graph = None
    size = None
    source = None
    sink = None
    def __init__(self, size: int, source: int, destination: int):
        """ Initialises graph by its size and by source/destination nodes.

        Args:
            size (int): The number of nodes in graph (source/destination must be included).
            source (int): The source of the flow.
            destination (int): The sink of the flow.

        Complexity:
            O(N)
        """
        self.size, self.source, self.sink = size, source, destination
        self.graph = [list() for _ in range(size)]


    def add_edge(self, begin: int, end: int, capacity: int = 1, reverse_capacity = 0):
        """ Adds bidirectional edge to the graph, while the capacity from start to end is "capacity" and is "reverse_capacity" the other way.

        Args:
            begin (int): Start node of the edge.
            end (int): End node of the edge.
            capacity (int): The capacity of edge from "begin" to "end".
            reverse_capacity (int): The capacity of edge from "end" to "begin".

        Complexity:
            O(1)

        Note:
            If the edge is unidirectional (which is in most cases), the reverse capacity shall remain 0.
        """
        self.graph[begin].append(self.Edge(end, len(self.graph[end]), capacity))
        self.graph[end].append(self.Edge(begin,len(self.graph[begin]) - 1 , reverse_capacity))

    def bfs(self) -> bool:
        """ Bread First Search through graph searching for shortest paths of reserves.

        Complexity:
            O(M)

        Returns:
            bool: True if there is still path to sink.
        """
        Q = deque()
        self.layer = [-1]*self.size
        self.layer[self.source] = 0
        Q.append(self.source)
        elements = 1
        while elements:
            node = Q.popleft()
            elements -=1
            for edge in self.graph[node]:
                if edge.flow < edge.capacity and self.layer[edge.neighbor] == -1:
                    self.layer[edge.neighbor] = self.layer[node] + 1
                    Q.append(edge.neighbor)
                    elements += 1
        return self.layer[self.sink] != -1

    def dfs(self, node: int, flow: int) -> int:
        """ Search through graph of shortest paths (acyclic).

        Args:
            node (int): Actual node which is being searched.
            flow (int): The maximal possible flow.

        Complexity:
            O(N)

        Returns:
            int: A flow found in an "arbitrary" path.

        TODO: Implement non-recursive version if this would be too slow.
        """
        if node == self.sink:
            return flow
        for edge in self.graph[node]:
            if edge.flow<edge.capacity and self.layer[node]+1==self.layer[edge.neighbor]:
                max_flow = self.dfs(edge.neighbor, min(flow, edge.capacity - edge.flow))
                if max_flow > 0:
                    edge.flow += max_flow
                    self.graph[edge.neighbor][edge.pair].flow -= max_flow
                    return max_flow
        return 0

    def get_flow(self) -> int:
        """ Gets maximum flow from source to sink.

        Note:
            The graph becomes unusable (in the final state) after this call.

        Complexity:
            O(N^2M)

        Returns:
            int: Maximum possible flow from source to sink.
        """
        flow = 0
        while(self.bfs()):
            while True:
                d_flow = self.dfs(self.source, int(1e18))
                if not d_flow:
                    break
                flow += d_flow
        return flow
