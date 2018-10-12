import TransportationProblem


def backtrackingSearch(problem):
    bestTotalCost = [float('inf')]
    bestPath = [None]

    def recurse(state, cost, history):
        if problem.isEnd(state):
            if cost < bestTotalCost[0]:
                bestTotalCost[0] = cost
                bestPath[0] = history

        for action, nextState, nextCost in problem.succAndCost(state):
            recurse(nextState, cost + nextCost, history + [(action, nextState, cost + nextCost)])

    recurse(problem.startState(), cost=0, history=[])
    return bestPath[0]


print backtrackingSearch(TransportationProblem.TransportationProblem(10))
