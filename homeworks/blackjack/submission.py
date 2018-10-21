import util, math, random
from collections import defaultdict
from util import ValueIteration

############################################################
# Problem 2a

# If you decide 2a is true, prove it in blackjack.pdf and put "return None" for
# the code blocks below.  If you decide that 2a is false, construct a counterexample.
class CounterexampleMDP(util.MDP):
    # Return a value of any type capturing the start state of the MDP.
    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 'in'
        # END_YOUR_CODE

    # Return a list of strings representing actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return ['stay', 'quit'] if state == 'in' else ['quit']
        # END_YOUR_CODE

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # Remember that if |state| is an end state, you should return an empty list [].
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        if state == 'in' and action == 'stay':
            return [('in', 0.2, 4), ('end', 0.8, 4)]
        elif state == 'in' and action == 'quit':
            return [('end', 1, 4)]
        else:
            return []
        # END_YOUR_CODE

    # Set the discount factor (float or integer) for your counterexample MDP.
    def discount(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 1
        # END_YOUR_CODE

############################################################
# Problem 3a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: list of integers (face values for each card included in the deck)
        multiplicity: single integer representing the number of cards with each face value
        threshold: maximum number of points (i.e. sum of card values in hand) before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look closely at this function to see an example of state representation for our Blackjack game.
    # Each state is a tuple with 3 elements:
    #   -- The first element of the tuple is the sum of the cards in the player's hand.
    #   -- If the player's last action was to peek, the second element is the index
    #      (not the face value) of the next card that will be drawn; otherwise, the
    #      second element is None.
    #   -- The third element is a tuple giving counts for each of the cards remaining
    #      in the deck, or None if the deck is empty or the game is over (e.g. when
    #      the user quits or goes bust).
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be placed into the succAndProbReward function below.
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # A few reminders:
    # * Indicate a terminal state (after quitting, busting, or running out of cards)
    #   by setting the deck to None.
    # * If |state| is an end state, you should return an empty list [].
    # * When the probability is 0 for a transition to a particular new state,
    #   don't include that state in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if you deviate from this)
        if state[2] is None:
            return []
        total_remaining_cards = sum(i for i in state[2])
        if total_remaining_cards == 0:
            return (state[0], None, None), 1, state[0]
        results = []

        def card_drawing_probability(count_of_card): return float(count_of_card) / total_remaining_cards

        def set_value_at_index(tup, i, value): return tup[:i] + (value, ) + tup[i + 1:]
        if action == 'Take':
            if state[1] is not None:
                next_card_value_in_hand = state[0] + self.cardValues[state[1]]
                if next_card_value_in_hand > self.threshold:
                    results.append(((next_card_value_in_hand, None, None), 1, 0))
                else:
                    results.append(((next_card_value_in_hand, None, set_value_at_index(state[2], state[1], state[2][state[1]] - 1)), 1, 0))
            else:
                for index, card_count in enumerate(state[2]):
                    if card_count is not 0:
                        next_card_value_in_hand = state[0] + self.cardValues[index]
                        if next_card_value_in_hand > self.threshold:
                            results.append(((next_card_value_in_hand, None, None), card_drawing_probability(card_count), 0))
                        else:
                            results.append(((next_card_value_in_hand, None, set_value_at_index(state[2], index, state[2][index] - 1)), card_drawing_probability(card_count), 0))
        elif action == 'Peek':
            if state[1] is not None:
                return []
            else:
                for index, card_count in enumerate(state[2]):
                    if card_count is not 0:
                        results.append(((state[0], index, state[2]), card_drawing_probability(card_count), -self.peekCost))
        elif action == 'Quit':
            if state[0] > self.threshold:
                results.append(((state[0], None, None), 1, 0))
            else:
                results.append(((state[0], None, None), 1, state[0]))

        def end_if_no_remaining_cards(r):
            new_state = r[0]
            if new_state[2] is not None:
                t_r_c = sum(i for i in new_state[2])
                if t_r_c is 0:
                    return (new_state[0], None, None), r[1], new_state[0]
            return r

        return map(end_if_no_remaining_cards, results)
        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action at least 10% of the time.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    return BlackjackMDP([3, 5, 10, 12], 1, 20, 1)
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        v_opt = 0 if newState is None else max((self.getQ(newState, a) for a in self.actions(newState)))
        scale = self.getStepSize() * (self.getQ(state, action) - (reward + self.discount * v_opt))
        feature_vector = self.featureExtractor(state, action)
        for f, v in feature_vector:
            self.weights[f] -= scale * v
        # END_YOUR_CODE

# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning
# Small test case
smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)

def simulate_QL_over_MDP(mdp, featureExtractor):
    # NOTE: adding more code to this function is totally optional, but it will probably be useful
    # to you as you work to answer question 4b (a written question on this assignment).  We suggest
    # that you add a few lines of code here to run value iteration, simulate Q-learning on the MDP,
    # and then print some stats comparing the policies learned by these two approaches.
    # BEGIN_YOUR_CODE
    rl = QLearningAlgorithm(mdp.actions, mdp.discount(), featureExtractor)
    util.simulate(mdp, rl, 30000)
    zero_weight_count = 0
    total_weight_count = 0
    for key in rl.weights:
        weight = rl.weights[key]
        total_weight_count += 1
        if abs(weight - 0.0) <= 0.00001: zero_weight_count += 1
    print "Total Weights: %s, Zero Weights: %s" % (total_weight_count, zero_weight_count)
    rl.explorationProb = 0
    vi = ValueIteration()
    vi.solve(mdp)
    count = 0
    expected_result = 0
    for key in vi.pi:
        count += 1
        if vi.pi[key] is rl.getAction(key):
            expected_result += 1
    print "total (state, action) pairs: %s" % (count*3)
    print "Accuracy of MDP using the featureExtractor: %s" % (float(expected_result)/count * 100)
    # END_YOUR_CODE

############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs.
# (See identityFeatureExtractor() above for a simple example.)
# Include the following features in the list you return:
# -- Indicator for the action and the current total (1 feature).
# -- Indicator for the action and the presence/absence of each face value in the deck.
#       Example: if the deck is (3, 4, 0, 2), then your indicator on the presence of each card is (1, 1, 0, 1)
#       Note: only add this feature if the deck is not None.
# -- Indicators for the action and the number of cards remaining with each face value (len(counts) features).
#       Note: only add these features if the deck is not None.
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state

    # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
    features = [((action, total), 1)]
    if counts is not None:
        features.append(((action, tuple(map(lambda t: 1 if t > 0 else 0, counts))), 1))
        for index, count in enumerate(counts):
            features.append(((action, "card %s" % index, "count %s" % count), 1))
    return features
    # END_YOUR_CODE

############################################################
# Problem 4d: What happens when the MDP changes underneath you?!

# Original mdp
originalMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# New threshold
newThresholdMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)

def compare_changed_MDP(original_mdp, modified_mdp, featureExtractor):
    # NOTE: as in 4b above, adding more code to this function is completely optional, but we've added
    # this partial function here to help you figure out the answer to 4d (a written question).
    # Consider adding some code here to simulate two different policies over the modified MDP
    # and compare the rewards generated by each.
    # BEGIN_YOUR_CODE
    vi = ValueIteration()
    vi.solve(original_mdp)
    rewards = util.simulate(modified_mdp, util.FixedRLAlgorithm(vi.pi), 10000)
    print "Expected Reward on modified mdp using original mdp policy: %i" % (float(sum(r for r in rewards)) / len(rewards))
    rewards_new = util.simulate(modified_mdp, QLearningAlgorithm(modified_mdp.actions, original_mdp.discount(), featureExtractor, 0.1), 10000)
    print "Expected Reward on modified mdp using Q Learning: %i" % (float(sum(r for r in rewards_new)) / len(rewards_new))
    # END_YOUR_CODE
