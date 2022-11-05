# DFU
class unionFind:
    """ DFU algorithm for components checking

    parent (list[int]): The component the node is in ("root" is stored here - in the end)
    size (list[int]): Size of component.
    components (int): Number of remaining components.
    """
    parent = None
    size = None
    components = None
    def __init__(self, size:int):
        """ Initialises structure. All node will be in its own component.

        Args:
            size (int): Size of graph.

        Note:
            Graph will be indexed from 0.

        Complexity:
            O(size)
        """
        self.parent = [i for i in range(size)]
        self.size = [1]*size
        self.components = size

    def get_component(self, node: int) -> int:
        """ Finds the component (its root) of input node.

        Args:
            node (int): The node whose component we want to find out.

        Complexity:
            O(log(N))

        Returns:
            int: The component of "node".
        """
        if node != self.parent[node]:
            self.parent[node] = self.get_component(self.parent[node])
        return self.parent[node]

    def connect_nodes(self, node_a: int, node_b: int) -> bool:
        """ Connect nodes "a" and "b" if they are in different component.

         Args:
            node_a (int): One of the nodes to be connected.
            node_b (int): Second node which is to be connected.

        Complexity:
            O(log(N)) -- O(1) amortised.

        Note:
            The smaller component is connected (rooted) to the bigger component.

        Returns:
            bool: True if the nodes were from different component. False otherwise.
        """
        first = self.get_component(node_a)
        second = self.get_component(node_b)
        if first == second:
            return False
        if self.size[first] < self.size[second]:
            first, second = second, first
        self.size[first] += self.size[second]
        self.size[second] = 0
        self.parent[second] = self.parent[first]
        self.components-=1
        return True

    def components_number(self) -> int:
        """ Return number of components of the graph.

        Returns:
            int: Number of components.

        Complexity:
            O(1)
        """
        return self.components

    def component_size(self, node: int) ->int:
        """ Return size of component to which node belongs.

        Args:
            node (int): The node whose component's size we are to get.

        Complexity:
            O(log(N)) -- Amortised O(1)

        Returns:
            The size of component of node.
        """
        return self.size[self.get_component(node)]

    def is_root(self, node: int) -> bool:
        """ Returns true if node is root (i.e. represents) of its component.

        Args:
            node (int): Node for which we check whether it is root.

        Returns:
            bool: True if node is root of component it is in.

        Complexity:
            O(log(N)) -- O(1) amortized.
        """
        return self.get_component(node) == node
