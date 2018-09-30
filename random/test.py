def min_cost(i, j, cost_matrix):

    # iterating over first column and computing cost
    # for traversing till the element (i, 0)
    for m in range(1, i + 1):
        cost_matrix[m][0] = cost_matrix[m - 1][0] + cost_matrix[m][0]

    # iterating over first row and computing cost
    # for traversing till the element (j, 0)
    for n in range(1, j + 1):
        cost_matrix[0][n] = cost_matrix[0][n - 1] + cost_matrix[0][n]

    # iterating over remaining entries for which the
    # cost for top and left elements have already
    # been computed
    for m in range(1, i + 1):
        for n in range(1, j + 1):
            cost_matrix[m][n] = min(cost_matrix[m - 1][n], cost_matrix[m][n - 1]) \
                                      + cost_matrix[m][n]

    return cost_matrix[i][j]


cost_matrix = [[1,1,1], [1,1,3]]
print(min_cost(1,1,cost_matrix))