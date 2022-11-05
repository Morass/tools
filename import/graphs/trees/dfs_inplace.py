# Standard DFS algorithm on tree (yet not recursive)
class DFS:
    """ Inplace DFS algorithm with custom function served results of sub-trees.

    Variables:
        graph (list[list[int]]): List with list of neighbors for each node.
        size (int): Size of graph
        parent (list[int]): List of parents of each node (-1 for root).
        order (list[int]): The order in which the DFS proceeded.
    """
    graph = None
    size = None
    order = None
    parent = None
    def __init__(self, N: int):
        """ Initialisation of tree structure.

        Complexity:
            O(N)

        Args:
            N (int) Size of tree

        Note:
            Nodes are expected to be from 0 to N-1
        """
        self.graph = [list() for _ in range(N)]
        self.size = N

    def add(self, a: int, b:int):
        """ Adds bidirectional edge between "a" and "b"

        Complexity:
            O(1)

        Args:
            a (int): Start/End of edge
            b (int): Start/End of edge
        """
        self.graph[a].append(b)
        self.graph[b].append(a)

    def dfs(self, foo, node: int = 0) :
        """ DFS search with start in "node"

        Complexity:
            O(N)

        Args:
            foo: Function which takes "node" and "output values of sub-trees (list) as argument
            node (int): Starting node.

        Returns:
            The output of foo function for starting node.

        Note:
            The function is not recursive (as it might be very slow in python)
        """
        self.order = []
        self.parent = [-1]*self.size
        # Node, Operation, Parent
        stack = [(node, True, -1)]
        ret = [list() for _ in range(self.size)]
        while True:
            node, operation, parent = stack.pop()
            if operation:
                stack.append((node, False, parent))
                for neighbor in self.graph[node]:
                    if neighbor != parent:
                        stack.append((neighbor, True, node))
            else:
                self.parent[node] = parent
                self.order.append(node)
                if parent == -1: return foo(node, ret[node])
                ret[parent].append(foo(node, ret[node]))

