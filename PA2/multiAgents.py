# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        if successorGameState.isWin():
            return 999999

        score = successorGameState.getScore()

        if successorGameState.isLose():
            score -= 300

        newGhostPositions = successorGameState.getGhostPositions()
        closestGhost = 150
        for ghost in newGhostPositions:
            testDistance = util.manhattanDistance(newPos, ghost)
            if testDistance < closestGhost:
                closestGhost = testDistance
        score += closestGhost

        foodList = newFood.asList()
        if successorGameState.getNumFood() < currentGameState.getNumFood():
            score += 75

        closestFood = 150
        for food in foodList:
            if util.manhattanDistance(newPos, food) < closestFood:
                closestFood = util.manhattanDistance(newPos, food)
        score -= 2 * closestFood #relative score will go up as closest food gets closer

        capsules = currentGameState.getCapsules()
        if newPos in capsules:
            score += 100

        if action == Directions.STOP:
            score -= 5

        return score

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def maxValue(gameState, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0: #if terminal state return evaluation function
                return self.evaluationFunction(gameState)
            utility = -999999
            actions = gameState.getLegalActions(0)
            for action in actions:
                utility = max(utility, minValue(gameState.generateSuccessor(0, action), depth, 1))
            return utility

        def minValue(gameState, depth, agent):
            if gameState.isWin() or gameState.isLose() or depth == 0: #if terminal state return evaluation function
                return self.evaluationFunction(gameState)
            utility = 999999
            actions = gameState.getLegalActions(agent)
            if agent == gameState.getNumAgents() - 1:
                for action in actions:
                    utility = min(utility, maxValue(gameState.generateSuccessor(agent, action), depth - 1))
            else:
                for action in actions:
                    utility = min(utility, minValue(gameState.generateSuccessor(agent, action), depth, agent + 1))
            return utility

        actionsList = gameState.getLegalActions()
        choice = Directions.STOP
        score = -999999
        for action in actionsList:
            lastScore = score
            score = max(score, minValue(gameState.generateSuccessor(0, action), self.depth, 1))
            if score > lastScore:
                choice = action
        return choice

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def maxValue(gameState, alpha, beta, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0: #if terminal state return evaluation function
                return self.evaluationFunction(gameState)
            utility = -999999
            actions = gameState.getLegalActions(0)
            for action in actions:
                utility = max(utility, minValue(gameState.generateSuccessor(0, action), alpha, beta, 1, depth))
                if utility > beta:
                    return utility
                alpha = max(alpha, utility)
            return utility

        def minValue(gameState, alpha, beta, agent, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0: #if terminal state return evaluation function
                return self.evaluationFunction(gameState)
            utility = 999999
            actions = gameState.getLegalActions(agent)
            for action in actions:
                if agent == gameState.getNumAgents() - 1:
                    utility = min(utility, maxValue(gameState.generateSuccessor(agent, action), alpha, beta, depth - 1))
                    if utility < alpha:
                        return utility
                    beta = min(beta, utility)
                else:
                    utility = min(utility, minValue(gameState.generateSuccessor(agent, action), alpha, beta, agent + 1, depth))
                    if utility < alpha:
                        return utility
                    beta = min(beta, utility)
            return utility

        actionsList = gameState.getLegalActions(0)
        choice = Directions.STOP
        score = -999999
        alpha = -999999
        beta = 999999
        for action in actionsList:
            lastScore = score
            score = max(score, minValue(gameState.generateSuccessor(0, action), alpha, beta, 1, self.depth))
            if score > lastScore:
                choice = action
            if score > beta:
                return choice
            alpha = max(alpha, score)
        return choice

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectedValue(gameState, agent, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0: #if terminal state return evaluation function
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agent)
            numerator = 0
            for action in actions:
                if agent == gameState.getNumAgents() - 1:
                    numerator += maxValue(gameState.generateSuccessor(agent, action), depth - 1)
                else:
                    numerator += expectedValue(gameState.generateSuccessor(agent, action), agent + 1, depth)
            return numerator / len(actions) #can use average when assuming uniform probabilities

        def maxValue(gameState, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0: #if terminal state return evaluation function
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(0)
            utility = -999999
            for action in actions:
                utility = max(utility, expectedValue(gameState.generateSuccessor(0, action), 1, depth))
            return utility

        if gameState.isWin() or gameState.isLose(): #if terminal state return evaluation function
            return self.evaluationFunction(gameState)
        legalActions = gameState.getLegalActions(0)
        choice = Directions.STOP
        score = -999999
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            lastScore = score
            score = max(score, expectedValue(nextState, 1, self.depth))
            if score > lastScore:
                choice = action
        return choice

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>

    The basic strategy here is fairly simple. The score of state should be higher when compared to another state when:
        a food has been eaten
        the distance to the closest food is smaller
        the distance to the closest ghost is larger

    After setting those criteria it was just a matter of playing around with the weights and seeing what works best.
    I added the section with the scaredTimer in an effort to  persuade pacman to eat a power pellet when near one and
    also to make him behave more aggressively when the ghost closest to him is scared

    I added the 'min(closestGhostDistance, 6)' because I didn't want pacman to worry about moving away form the ghost if
    it was already 6 or more spaces away

    """
    "*** YOUR CODE HERE ***"

    if currentGameState.isWin():
        return 999999 + 10
    if currentGameState.isLose():
        return -999999

    score = currentGameState.getScore()
    foodList = currentGameState.getFood().asList()
    closestFood = 999999
    for food in foodList:
        distance = util.manhattanDistance(food, currentGameState.getPacmanPosition())
        if distance < closestFood:
            closestFood = distance

    index = 1
    closestGhostDistance = 999999
    while index <= currentGameState.getNumAgents() - 1:
        distance = util.manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getGhostPosition(index))
        if distance < closestGhostDistance:
            closestGhostDistance = distance
            closestGhostState = currentGameState.getGhostState(index)
        index += 1

    if closestGhostState.scaredTimer > 0:
        score += 25
        score += (1 / closestFood) * 90
        score += 200 * (1 / len(foodList))
    else:
        score += min(closestGhostDistance, 6) * 3
        score += (1/closestFood) * 9
        score += 20 * (1 / len(foodList))

    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

