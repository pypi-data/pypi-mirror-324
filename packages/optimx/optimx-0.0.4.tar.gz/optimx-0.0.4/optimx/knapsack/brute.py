from itertools import combinations


class KnapsackBrute:

    def solve(self, weights, values, capacity):
        n = len(weights)
        max_value = 0
        best_combination = []

        for r in range(1, n + 1):
            for combination in combinations(range(n), r):
                total_weight = sum(weights[i] for i in combination)
                total_value = sum(values[i] for i in combination)

                if total_weight <= capacity and total_value > max_value:
                    max_value = total_value
                    best_combination = combination

        return best_combination, max_value