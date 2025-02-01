import math

class TSPNearestNeighbor:

    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix
        self.num_nodes = len(distance_matrix)

    def solve(self, start_node=None, cycle=True):
        visited = [False] * self.num_nodes
        tour = []
        total_distance = 0

        # If start_node is None, default to the first node (0)
        if start_node is None:
            start_node = 0

        # Start at the specified node
        current_node = start_node
        tour.append(current_node)
        visited[current_node] = True

        # Repeat until all nodes have been visited
        while len(tour) < self.num_nodes:
            nearest_node = None
            nearest_distance = math.inf

            # Find the nearest unvisited node
            for node in range(self.num_nodes):
                if not visited[node]:
                    distance = self.distance_matrix[current_node][node]
                    if distance < nearest_distance:
                        nearest_node = node
                        nearest_distance = distance

            # Move to the nearest node
            current_node = nearest_node
            tour.append(current_node)
            visited[current_node] = True
            total_distance += nearest_distance

        # If cycle is True, complete the tour by returning to the starting node
        if cycle:
            tour.append(start_node)
            total_distance += self.distance_matrix[current_node][start_node]

        return tour