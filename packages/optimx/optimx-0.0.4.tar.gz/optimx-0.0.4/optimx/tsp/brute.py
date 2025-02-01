from itertools import permutations


class TSPBrute:

    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix
        self.num_nodes = len(distance_matrix)

    def solve(self, start_node=None, cycle=False):
        nodes = list(range(self.num_nodes))

        if start_node is not None:
            nodes.remove(start_node)
        
        shortest_distance = float("inf")
        best_route = None

        for route in permutations(nodes):
            # If a starting node is specified, prepend it to the route
            complete_route = (start_node,) + route if start_node is not None else route
            current_distance = self._calculate_route_distance(complete_route, return_to_start=cycle)

            if current_distance < shortest_distance:
                shortest_distance = current_distance
                best_route = complete_route

        if cycle:
            best_route = best_route + (best_route[0],)
        return best_route
    
    def _calculate_route_distance(self, route, return_to_start=False):
        """Calculates the total distance of a given route based on the distance matrix."""
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += self.distance_matrix[route[i]][route[i + 1]]
        # If returning to the start, add the distance from the last node back to the first
        if return_to_start:
            total_distance += self.distance_matrix[route[-1]][route[0]]
        return total_distance