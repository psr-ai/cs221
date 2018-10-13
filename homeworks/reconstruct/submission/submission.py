import shell
import util
import wordsegUtil

############################################################
# Problem 1b: Solve the segmentation problem under a unigram model

class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
        return 0
        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
        return state == len(self.query)
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        paths = []
        next_state = state + 1
        while next_state <= len(self.query):
            action = self.query[state:next_state]
            paths.append((action, next_state, self.unigramCost(self.query[state:next_state])))
            next_state += 1
        return paths
        # END_YOUR_CODE

def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    # BEGIN_YOUR_CODE (our solution is 10 lines of code, but don't worry if you deviate from this)
    return ' '.join(ucs.actions)
    # END_YOUR_CODE

############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 0, 0
        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)
        return state[0] == len(self.queryWords)
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 16 lines of code, but don't worry if you deviate from this)
        results = []
        previous_word = None
        if state == self.startState():
            previous_word = wordsegUtil.SENTENCE_BEGIN
        else:
            previous_possible_fills = self.possibleFills(self.queryWords[state[0] - 1])
            previous_word = list(previous_possible_fills)[state[1]] if previous_possible_fills and len(previous_possible_fills) > 0 else self.queryWords[state[0] - 1]

        fills = self.possibleFills(self.queryWords[state[0]]) or [self.queryWords[state[0]]]
        for index, possibleFill in enumerate(fills):
            next_state = (state[0] + 1, index)
            results.append((possibleFill, next_state, self.bigramCost(previous_word, possibleFill)))

        return results
        # END_YOUR_CODE

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(VowelInsertionProblem(queryWords, bigramCost, possibleFills))
    return ' '.join(ucs.actions) if len(ucs.actions) > 0 else ''
    # END_YOUR_CODE

############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
        # (current_node, prev_node, possible_fill_no)
        return 0, 0, 0
        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
        return state[0] == len(self.query)
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 23 lines of code, but don't worry if you deviate from this)
        results = []
        if state[0] == state[1]:
            current_word = wordsegUtil.SENTENCE_BEGIN
        else:
            possible_fills = self.possibleFills(self.query[state[1]: state[0]])
            current_word = list(possible_fills)[state[2]]
        new_state = [state[0] + 1, state[0], 0]
        while new_state[0] <= len(self.query):
            new_word = self.query[new_state[1]: new_state[0]]
            for index, possibleFill in enumerate(self.possibleFills(new_word)):
                new_state[2] = index
                results.append((possibleFill, (new_state[0], new_state[1], new_state[2]), self.bigramCost(current_word, possibleFill)))
            new_state[0] += 1
        return results
        # END_YOUR_CODE

def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''

    # BEGIN_YOUR_CODE (our solution is 11 lines of code, but don't worry if you deviate from this)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(JointSegmentationInsertionProblem(query, bigramCost, possibleFills))
    return ' '.join(ucs.actions) if len(ucs.actions) > 0 else ''
    # END_YOUR_CODE

############################################################

if __name__ == '__main__':
    shell.main()
