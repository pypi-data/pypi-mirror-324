class TSPSolverMemoization:
    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix
        self.num_nodes = len(distance_matrix)
        self.memo = {}

    def _tsp_memoization_with_path(self, current_node, remaining_nodes, path=None, cycle=True):
        """
        Solves the TSP using dynamic programming with memoization.

        Parameters:
            - current_node: The node currently being visited.
            - remaining_nodes: The nodes that are yet to be visited.
            - path: List representing the current path taken.
            - cycle: Whether to return to the starting node at the end (True) or not (False).

        Returns:
            - min_distance: Minimum distance for the TSP path.
            - min_path: The path taken for this minimum distance.
        """
        if path is None:
            path = []

        # Convert remaining_nodes to a tuple for use as a dictionary key
        remaining_nodes = tuple(remaining_nodes)
        
        # Check if this state has already been computed
        if (current_node, remaining_nodes) in self.memo:
            return self.memo[(current_node, remaining_nodes)], path
        
        # Base case: no remaining nodes to visit
        if not remaining_nodes:
            # Return to start node if cycle is True
            final_distance = self.distance_matrix[current_node][path[0]] if cycle else 0
            return final_distance, path

        min_distance = float('inf')
        min_path = None
        
        # Recursive case: try visiting each remaining node
        for i in range(len(remaining_nodes)):
            next_node = remaining_nodes[i]
            new_remaining_nodes = remaining_nodes[:i] + remaining_nodes[i+1:]
            # Recur with the next node
            d, p = self._tsp_memoization_with_path(next_node, new_remaining_nodes, path + [next_node], cycle)
            d += self.distance_matrix[current_node][next_node]
            
            # Update minimum distance and path
            if d < min_distance:
                min_distance = d
                min_path = p

        # Memoize the result
        self.memo[(current_node, remaining_nodes)] = min_distance
        
        return min_distance, min_path

    def solve(self, start_node=None, cycle=True):
        """
        Solves the TSP by initializing parameters and calling the recursive memoized function.

        Parameters:
            - start_node: The node to start from (default is 0).
            - cycle: Whether to return to the starting node at the end (True) or not (False).

        Returns:
            - min_path: The path taken for the minimum distance.
            - min_distance: Minimum distance for the TSP path.
        """
        # If start_node is None, default to the first node (0)
        if start_node is None:
            start_node = 0
        
        # Initialize the remaining nodes (excluding the start node)
        remaining_nodes = list(range(self.num_nodes))
        remaining_nodes.remove(start_node)

        # Reset memoization dictionary
        self.memo = {}

        # Solve the TSP with memoization
        min_distance, min_path = self._tsp_memoization_with_path(start_node, remaining_nodes, path=[start_node], cycle=cycle)

        # If cycle is True, add start node to the end to complete the cycle
        if cycle:
            min_path.append(start_node)
            
        return min_path
