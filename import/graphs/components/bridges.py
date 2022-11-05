# Data structure for finding bridges and sudden manipulation(s)
class bridges:
    """ Data structure for searching of bridges in graph and manipulation with such graph.

    Note:
        Nodes in the graph are to be indexed from 0 to size-1.

    Variables:
        graph (list[list[int]]): List of list of neighbors (for each node).
        size (int): Number of nodes in the graph.
        bridges (set[Tuple[int,int]]): Set with pairs - 2 nodes connected by an edge.
            Every bridge will be in set exactly once in "sorted" order.
        bridged_graph (list[list[int]]): List of list of neighbors of "bridged graph" (forest of components without bridges connected by bridges).
        dfu (unionFind): Union Find structure with components of bridged forest.
        subtree_size (list[int]): Size of subtree of bridged-forest.
        tree_size (unionFind): Union Find data structure for trees.
    """
    graph = None
    size = None
    bridges = None
    bridged_graph = None
    dfu = None
    subtree_size = None
    tree_size = None
    def __init__(self, size: int):
        """ Initialises variables of the data structure.

        Args:
            size (int): The number of nodes of the graph.

        Complexity:
            O(size)
        """
        self.size = size
        self.graph = [list() for _ in range(size)]

    @staticmethod
    def __normalize(first: int, second: int) -> tuple[int, int]:
        """ Returns an edge in normalized state => as tuple where first node has lower index.

        Args:
            first (int): First node connected by an edge.
            second (int): Second node connected by an edge.

        Returns:
            tuple(int,int): Edge with first lower index. (i.e. minmax function in C++)

        Complexity:
            O(1)
        """
        return min(first, second), max(first, second)

    def add_edge(self, first: int, second: int):
        """ Adds bidirectional edge to graph.

        Args:
            first (int): First node of the edge.
            second (int): Second node of the edge.

        Complexity:
            O(N)

        Note:
            Edges shall be indexed from 0 to "size - 1"
        """
        self.graph[first].append(second)
        self.graph[second].append(first)

    def bridges_search(self):
        """ Searches for bridges in graph.

        Complexity:
            O(N) -- times complexity to access hashed set.
        """
        self.bridges = set()
        seen = [False]*self.size
        time_1 = [0]*self.size
        time_2 = [0]*self.size
        time = 0
        # In case the graph is not connected.
        for start in range(self.size):
            if not seen[start]:
                stack = [(start, 0, -1)]
                while len(stack):
                    node, index, parent = stack.pop()
                    if not index:
                        seen[node] = True
                        time_1[node] = time_2[node] = time
                        time += 1
                    else:
                        # After dfs
                        previous_neighbor = self.graph[node][index-1]
                        if previous_neighbor != parent:
                            time_1[node] = min (time_1[node], time_1[previous_neighbor])
                            if time_1[previous_neighbor] > time_2[node]:
                                self.bridges.add(self.__normalize(node, previous_neighbor))
                    if index != len(self.graph[node]):
                        stack.append((node, index + 1, parent))
                        neighbor = self.graph[node][index]
                        if neighbor == parent: continue
                        if seen[neighbor]:
                            time_1[node] = min(time_1[node], time_1[neighbor])
                        else:
                            stack.append((neighbor, 0, node))

    def get_bridges(self) -> list[tuple]:
        """ Returns list of edges which are bridge. The edges will have first index lower and will be sorted.

            Returns:
                list[tuple[int, int]]: Sorted list of bridges.

            Complexity:
                O(Nlog(N))
        """
        return sorted(list(self.bridges))

    def is_bridge(self, first: int, second: int) -> bool:
        """ Check if given edge is a bridge.

        Args:
            first (int): One of the ends of an edge.
            second (int): Second end of an edge.

        Note:
            The order shall not matter.

        Returns:
            bool: True if the edge is bridge.

        Complexity:
            O(hash-table-access)
        """
        return self.__normalize(first, second) in self.bridges

    def get_bridges_number(self) -> int:
        """ Gets number of found bridges.

        Returns:
            int: The number of bridges in graph.

        Complexity:
            O(1)
        """
        return len(self.bridges)

    def create_bridged_forest(self):
        """ Creates bridged forest.

        Requires:
            bridges_search (tho it will call the function if it was not called yet before).
            unionFind: Import of unionFind data structure.

        Complexity:
            O(Nlog(N))
        """
        # Proceeds bridges search if it was not done before.
        if self.bridges is None: self.bridges_search()
        self.dfu = unionFind(self.size)
        # Create components for bridged forest
        # Complexity: O(NlogN)
        for node in range(self.size):
            for neighbor in self.graph[node]:
                if not self.is_bridge(node, neighbor):
                    self.dfu.connect_nodes(node, neighbor)
        # Connect nodes by bridges / create forest graph
        # Note: From now on, only dfu components will be considered as nodes
        # Complexity: O(len(self.bridges)
        self.bridged_graph = [list() for _ in range(self.size)]
        for first, second in self.bridges:
            comp_one = self.dfu.get_component(first)
            comp_two = self.dfu.get_component(second)
            self.bridged_graph[comp_one].append(comp_two)
            self.bridged_graph[comp_two].append(comp_one)
        # Creates "order" - list with walk through tree (some kind of dfs).
        # Complexity: O(size)
        order = []
        parents = [-1] * self.size
        seen  = [0] * self.size
        stack = []
        for start in range(self.size):
            if not seen[start] and self.dfu.is_root(start):
                stack.append((start, True, -1))
                while len(stack):
                    node, operation, parent = stack.pop()
                    parents[node] = parent
                    if operation:
                        stack.append((node, False, parent))
                        for neigbor in self.bridged_graph[node]:
                            if neigbor != parent:
                                stack.append((neigbor, True, node))
                    else:
                        order.append(node)
                        seen[node] = True
        # Find sizes of bridged subtrees.
        # Complexity: O(Nlog(N))
        self.subtree_size = [0]*self.size
        for node in order:
            self.subtree_size[node] = self.dfu.component_size(node)
            for neigbor in self.bridged_graph[node]:
                if neigbor != parents[node]:
                    self.subtree_size[node] += self.subtree_size[neigbor]
        # Find size of each subtree
        # Complexity: O(Nlog(N))
        self.tree_size = unionFind(self.size)
        for node in range(self.size):
            for neigbor in self.graph[node]:
                self.tree_size.connect_nodes(node, neigbor)

    def get_bridge_sizes(self, first: int, second: int) -> int:
        """ Finds sizes of each component which would be created by splitting given bridge.

        Args:
            first (int): One of the nodes of the bridge.
            second (int): The second node of the bridge.

        Returns:
            tuple(int, int): Sizes of component created by splitting by the bridge.

        Note:
            None is returned if edge is not bridge (or edge...)

        Complexity:
            O(log(N)) -- O(1) amortized.
        """
        if not self.is_bridge(first, second): return None
        component_first = self.dfu.get_component(first)
        component_second = self.dfu.get_component(second)
        if self.subtree_size[component_first] < self.subtree_size[component_second]:
            return self.subtree_size[component_first], self.tree_size.component_size(second) - self.subtree_size[component_first]
        return self.tree_size.component_size(first) - self.subtree_size[component_second], self.subtree_size[component_second]
