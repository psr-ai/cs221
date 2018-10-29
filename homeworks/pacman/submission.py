from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument
    is an object of GameState class. Following are a few of the helper methods that you
    can use to query a GameState object to gather information about the present state
    of Pac-Man, the ghosts and the maze.

    gameState.getLegalActions():
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action):
        Returns the successor state after the specified agent takes the action.
        Pac-Man is always agent 0.

    gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.configuration.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    gameState.getScore():
        Returns the score corresponding to the current state of the game


    The GameState class is defined in pacman.py and you might want to look into that for
    other helper methods, though you don't need to.
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best


    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following:
      pacman won, pacman lost or there are no legal moves.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game

      gameState.getScore():
        Returns the score corresponding to the current state of the game

      gameState.isWin():
        Returns True if it's a winning state

      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue

    """

    # BEGIN_YOUR_CODE (our solution is 26 lines of code, but don't worry if you deviate from this)
    def recurse(state, depth, agent_index):
      if state.isWin() or state.isLose() or len(state.getLegalActions(agent_index)) is 0:
        return state.getScore(), None
      if depth is 0:
        return self.evaluationFunction(state), None
      next_depth = depth - 1 if agent_index == state.getNumAgents() - 1 else depth
      next_agent_index = 0 if agent_index == state.getNumAgents() - 1 else agent_index + 1
      candidates = [(recurse(state.generateSuccessor(agent_index, action), next_depth, next_agent_index)[0], action) for action in state.getLegalActions(agent_index)]
      if agent_index == self.index:
        return max(candidates)
      else:
        return min(candidates)

    utility, action = recurse(gameState, self.depth, 0)
    return action
    # END_YOUR_CODE

######################################################################################
# Problem 2a: implementing alpha-beta

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    # BEGIN_YOUR_CODE (our solution is 49 lines of code, but don't worry if you deviate from this)
    def min_fn(state, next_depth, agent_index, next_agent_index, alpha, beta):
      min_value = float('+inf')
      min_value_action = None
      for action in state.getLegalActions(agent_index):
        next_value = recurse(state.generateSuccessor(agent_index, action), next_depth, next_agent_index, alpha, beta)[0]
        if next_value < min_value:
          min_value = next_value
          min_value_action = action
        if next_value <= alpha:
          break
        if next_value < beta:
          beta = next_value
      return min_value, min_value_action

    def max_fn(state, next_depth, agent_index, next_agent_index, alpha, beta):
      max_value = float('-inf')
      max_value_action = None
      for action in state.getLegalActions(agent_index):
        next_value = recurse(state.generateSuccessor(agent_index, action), next_depth, next_agent_index, alpha, beta)[0]
        if next_value > max_value:
          max_value = next_value
          max_value_action = action
        if next_value >= beta:
          break
        if next_value > alpha:
          alpha = next_value
      return max_value, max_value_action

    def recurse(state, depth, agent_index, alpha, beta):
      if gameState.isWin() or gameState.isLose() or len(state.getLegalActions(agent_index)) is 0:
        return gameState.getScore(), None
      if depth is 0:
        return self.evaluationFunction(state), None
      next_depth = depth - 1 if agent_index == state.getNumAgents() - 1 else depth
      next_agent_index = 0 if agent_index == state.getNumAgents() - 1 else agent_index + 1
      if agent_index == self.index:
        return max_fn(state, next_depth, agent_index, next_agent_index, alpha, beta)
      else:
        return min_fn(state, next_depth, agent_index, next_agent_index, alpha, beta)

    utility, action = recurse(gameState, self.depth, 0, float('-inf'), float('inf'))
    return action
    # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    # BEGIN_YOUR_CODE (our solution is 25 lines of code, but don't worry if you deviate from this)
    def recurse(state, depth, agent_index):
      if state.isWin() or state.isLose() or len(state.getLegalActions(agent_index)) is 0:
        return state.getScore(), None
      if depth is 0:
        return self.evaluationFunction(state), None
      next_depth = depth - 1 if agent_index == state.getNumAgents() - 1 else depth
      next_agent_index = 0 if agent_index == state.getNumAgents() - 1 else agent_index + 1
      candidates = [(recurse(state.generateSuccessor(agent_index, action), next_depth, next_agent_index)[0], action) for action in state.getLegalActions(agent_index)]
      if agent_index == self.index:
        return max(candidates)
      else:
        return float(sum([a for a, b in candidates]))/len(candidates), None

    utility, action = recurse(gameState, self.depth, 0)
    return action
    # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function

def betterEvaluationFunction(currentGameState):
  """
    Your extreme, unstoppable evaluation function (problem 4).

    DESCRIPTION: <write something here so we know what you did>
  """

  # BEGIN_YOUR_CODE (our solution is 26 lines of code, but don't worry if you deviate from this)
  if currentGameState.isLose():
    return -float("inf")

  current_pacman_position = currentGameState.getPacmanPosition()
  food_list = currentGameState.getFood().asList()
  closest_distance_from_food = min([util.manhattanDistance(current_pacman_position, food_position) for food_position in food_list])
  number_of_capsules_left = len(currentGameState.getCapsules()) or 0.1
  food_left = currentGameState.getNumFood()

  active_ghosts = [ghost for ghost in currentGameState.getGhostStates() if not ghost.scaredTimer]
  closest_ghost_active = currentGameState.getFood().width + currentGameState.getFood().height
  if len(active_ghosts) > 0:
    closest_ghost_active = min([util.manhattanDistance(current_pacman_position, g.getPosition()) for g in active_ghosts])

  scared_ghosts = [ghost for ghost in currentGameState.getGhostStates() if ghost.scaredTimer]
  closest_ghost_scared = float('inf')
  if len(scared_ghosts) > 0:
    closest_ghost_scared = min([util.manhattanDistance(current_pacman_position, g.getPosition()) for g in scared_ghosts])

  mobility = 0
  if currentGameState.hasWall(current_pacman_position[0], current_pacman_position[1]):
    mobility = -100

  score = 1 * currentGameState.getScore() + \
          10. / closest_distance_from_food + \
          50. / closest_ghost_scared + \
          1 * closest_ghost_active + \
          20. / number_of_capsules_left + \
          10. / food_left + \
          mobility
  return score
  # END_YOUR_CODE

# Abbreviation
better = betterEvaluationFunction
