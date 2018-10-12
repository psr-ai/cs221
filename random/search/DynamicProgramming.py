import TransportationProblem


def dynamicProgramming(problem):
    cache = {}

    def futureCost(state):
        if state == problem.isEnd(state):
            return 0

        if state in cache:
            return cache[state][0]

        # best action = (futureCost, action, newState, cost)
        bestAction = (float('inf'), None, None, None)
        for action, nextState, cost in problem.succAndCost(state):
            currentFutureCost = cost + futureCost(nextState)
            if currentFutureCost < bestAction[0]:
                bestAction = (currentFutureCost, action, nextState, cost)

        cache[state] = bestAction
        return bestAction[0]

    state = problem.startState()
    totalCost = futureCost(state)

    history = []
    while not problem.isEnd(state):
        _, action, newState, cost = cache[state]
        history.append((action, newState, cost))
        state = newState

    return totalCost, history


print dynamicProgramming(TransportationProblem.TransportationProblem(100))