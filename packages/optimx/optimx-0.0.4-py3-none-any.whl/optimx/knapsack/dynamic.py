class KnapsackDynamicProgram:

    def solve(self, weights, values, capacity):
        max_value, dp = self.knapsack_max_value(weights, values, capacity)
        best_combination = self.find_included_items(weights, dp)
        return best_combination, max_value
        

    def knapsack_max_value(self, weights, values, W):
        """
        Calculate the maximum value for the knapsack problem and return the DP table.

        :param weights: List of weights of the items
        :param values: List of values of the items
        :param W: Capacity of the knapsack
        :return: Maximum value and the DP table
        """
        n = len(weights)
        dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

        # Fill the DP table
        for i in range(1, n + 1):
            for w in range(1, W + 1):
                if weights[i - 1] <= w:
                    dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
                else:
                    dp[i][w] = dp[i - 1][w]

        max_value = dp[n][W]
        return max_value, dp
                          
    
    def find_included_items(self, weights, dp):
        """
        Find the items included in the optimal solution based on the DP table.

        :param weights: List of weights of the items
        :param dp: DP table computed by knapsack_max_value
        :return: List of included items (1-based index)
        """
        n = len(weights)
        W = len(dp[0]) - 1
        included_items = []
        i, w = n, W

        while i > 0 and w > 0:
            if dp[i][w] != dp[i - 1][w]:
                included_items.append(i)
                w -= weights[i - 1]
            i -= 1

        included_items.reverse()
        included_items = [item - 1 for item in included_items]
        return included_items
