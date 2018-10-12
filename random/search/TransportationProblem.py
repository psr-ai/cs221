class TransportationProblem:

    def __init__(self, N):
        self.N = N

    def startState(self):
        return 1

    def isEnd(self, state):
        return state == self.N

    def succAndCost(self, state):
        # List of (action, nextState, cost)
        results = []
        if state + 1 <= self.N:
            results.append(('Walk', state + 1, 1))

        if state + 2 <= self.N:
            results.append(('Tram', state * 2, 2))

        return results
