# Leo Weiner -- lzweine@emory.edu
# THIS  CODE  WAS MY OWN WORK , IT WAS  WRITTEN  WITHOUT  CONSULTING  ANY
# SOURCES  OUTSIDE  OF THOSE  APPROVED  BY THE  INSTRUCTOR. Leo Weiner


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
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

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
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood() #food available from current state
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor) 
        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print('successorGameState = ', successorGameState) # gamestate
        # print('newPos = ', newPos)                         # coordinates
        # print('currentFood = ', currentFood)               # grid instance
        # print('newFood = ', newFood)                       # grid instance
        # print('currentCapsules = ', currentCapsules)       # list
        # print('newCapsules = ', newCapsules)               # list
        # print('newGhostStates = ', newGhostStates)         # agent state
        # print('newScaredTimes = ', newScaredTimes)         # number of moves

        # loop through each possible action
        # is this successor state "better" than standing still?
        # if so, hold that as bestMove, and if a "better" yet option comes along, update
        # if there are no "better" options, stay still
        # ^^but this is done already in getAction
        newFoodAsList = newFood.asList()
        # print ('newFoodAsList = ', newFoodAsList)


        # how do you define "better"?
            # from pacman               # newPos
            # how close are the ghosts? newGhostStates
            # are they scared?          newScaredTimes
            # how close is more food?   currentFood & newFood
            # how close is a power pellet? currentCapsules & newCapsules

        foodScore = 0
        for food in newFoodAsList:
            distanceToFood = util.manhattanDistance(food, newPos)
            if not (distanceToFood == 0):
                foodScore += (1.0/distanceToFood)

        ghostScore = 0
        for ghost in newGhostStates:
            distanceToGhost = util.manhattanDistance(ghost.getPosition(), newPos)
            if (distanceToGhost < 6 and distanceToGhost != 0):
                ghostScore += (1.0/distanceToGhost)
        # print('ghost score = ', ghostScore)

        pelletScore = 0
        for pellet in newCapsules:
            distanceToPellet = util.manhattanDistance(pellet, newPos)
            # print(distanceToPellet)
            if not (distanceToPellet == 0):
                pelletScore += (1.0/distanceToPellet)



        foodWeight = 1
        ghostWeight = 3
        pelletWeight = 0

        foodVar = foodWeight*foodScore
        ghostVar = ghostWeight*ghostScore
        pelletVar = pelletWeight*pelletScore

        # print('pelletVar', pelletVar)
        # print('foodVar', foodVar)
        # print('ghostVar', ghostVar)
        # print('-----')

        weightedScore = foodVar + pelletVar - ghostVar
        weightedScore += successorGameState.getScore()
        # return successorGameState.getScore()
        return weightedScore


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

        def maxValue(state, depth, agentNum):
            # if state.isWin() or state.isLose() or depth == self.depth: #check for terminal nodes
            #     return self.evaluationFunction(state)

            v = -100000000  # initalize v to negative inf

            Actions = state.getLegalActions(0)  # PACMAN is agent 0, get his possible actions

            for successor in Actions:  # check each possible action
                v = max(v, value(state.generateSuccessor(0, successor), depth + 1, agentNum + 1))
            return v  # value remains previous greatest, unless it finds a higher payoff in minValue


        def minValue(state, depth, agentNum):

            v = 100000000  # initalize v to inf

            Actions = state.getLegalActions(agentNum)  # ghostNum is agent 1 or more, get his possible actions

            for successor in Actions:
                v = min(v, value(state.generateSuccessor(agentNum, successor), depth + 1, agentNum + 1))
            return v # value remains previous smallest, unless it finds a better payoff in maxValue

        def value(state, depth, agentNum):
            numAgents = gameState.getNumAgents() #track number of agents in the game
            if state.isWin() or state.isLose() or depth == self.depth*numAgents:  # check for terminal nodes
                return self.evaluationFunction(state)

            if (agentNum == state.getNumAgents()): #if we've moved through each of the agents
                agentNum = 0 #reset to PACMAN
            if (agentNum == 0): #if the current agent is PACMAN
                return maxValue(state, depth, agentNum) #return his MAX
            else: #it's a ghost
                return minValue(state, depth, agentNum) #otherwise, return the ghost's MIN


        Actions = gameState.getLegalActions(0) #get PACMAN's possible moves
        maximumValue = -100000000 #initalize max to negative inf
        bestAction = Actions[0] #
        agentNum = 0

        for action in Actions:
            successor = gameState.generateSuccessor(0, action)
            currentValue = value(successor, 1, 1)
            if maximumValue < currentValue:
                maximumValue = currentValue
                bestAction = action

        return bestAction
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

        def maxValue(state, depth, agentNum, alpha, beta):
            # if state.isWin() or state.isLose(): #check for terminal nodes
            #     return self.evaluationFunction(state)

            v = -100000000  # initalize v to negative inf

            Actions = state.getLegalActions(0)  # PACMAN is agent 0, get his possible actions
            bestMove = Directions.STOP
            for successor in Actions:  # check each possible action
                little = value(state.generateSuccessor(0, successor), depth + 1, 1, alpha, beta)
                # v = max(v, temp)
                if little > v:
                    v = little
                    bestMove = successor

                if (v > beta):
                    return v
                alpha = max(alpha, v)
            if depth == 0:
                return bestMove
            return v  # value remains previous greatest, unless it finds a higher payoff in minValue


        def minValue(state, depth, agentNum, alpha, beta):
            # if state.isWin() or state.isLose(): #check for terminal nodes
            #     return self.evaluationFunction(state)
            # if depth >= self.depth*state.getNumAgents():
            #     return self.evaluationFunction(state)

            if agentNum == state.getNumAgents():
                return value(state, depth, 0, alpha, beta)

            v = 100000000  # initalize v to inf

            Actions = state.getLegalActions(agentNum)  # ghostNum is agent 1 or more, get his possible actions

            for successor in Actions:
                v = min(v, value(state.generateSuccessor(agentNum, successor), depth + 1, agentNum + 1, alpha, beta))

                if (v < alpha):
                    return v
                beta = min(beta, v)
            return v # value remains previous smallest, unless it finds a better payoff in maxValue

        def value(state, depth, agentNum, alpha, beta):
            numAgents = gameState.getNumAgents() #track number of agents in the game
            if state.isWin() or state.isLose():  # check for terminal nodes
                return self.evaluationFunction(state)

            # if (agentNum == state.getNumAgents()): #if we've moved through each of the agents
            #     agentNum = 0 #reset to PACMAN

            if (agentNum == 0): #if the current agent is PACMAN
                return maxValue(state, depth, agentNum, alpha, beta) #return his MAX
            else: #it's a ghost
                if depth >= self.depth * state.getNumAgents():
                    return self.evaluationFunction(state)
                return minValue(state, depth, agentNum, alpha, beta) #otherwise, return the ghost's MIN


        Actions = gameState.getLegalActions(0) #get PACMAN's possible moves
        maximumValue = -100000000 #initalize max to negative inf
        bestAction = Actions[0] #
        agentNum = 0

        alpha = -100000000
        beta = 100000000
        # print('pass')

        # for action in Actions:
        #     successor = gameState.generateSuccessor(0, action)
        #     currentValue = value(successor, 1, 1, alpha, beta)
        #     print('alpha = ', alpha)
        #     print('beta = ', beta)
        #     print('currentValue = ', currentValue)
        #     if maximumValue < currentValue:
        #         maximumValue = currentValue
        #         bestAction = action


        return value(gameState, 0, 0, alpha, beta)


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

        def maxValue(state, depth, agentNum):
            # if state.isWin() or state.isLose() or depth == self.depth: #check for terminal nodes
            #     return self.evaluationFunction(state)

            v = -100000000  # initalize v to negative inf

            Actions = state.getLegalActions(0)  # PACMAN is agent 0, get his possible actions

            for successor in Actions:  # check each possible action
                v = max(v, value(state.generateSuccessor(0, successor), depth + 1, agentNum + 1))
            return v  # value remains previous greatest, unless it finds a higher payoff in minValue


        def expValue(state, depth, agentNum):

            v = 0  # initalize v to 0

            Actions = state.getLegalActions(agentNum)  # ghostNum is agent 1 or more, get his possible actions

            for successor in Actions:
                prob = 1.0 / len(Actions)
                v += prob*value(state.generateSuccessor(agentNum, successor), depth + 1, agentNum + 1)
            return v # value remains previous smallest, unless it finds a better payoff in maxValue

        def value(state, depth, agentNum):
            numAgents = gameState.getNumAgents() #track number of agents in theame
            if state.isWin() or state.isLose() or depth == self.depth*numAgents:  # check for terminal nodes
                return self.evaluationFunction(state)

            if (agentNum == state.getNumAgents()): #if we've moved through each of the agents
                agentNum = 0 #reset to PACMAN
            if (agentNum == 0): #if the current agent is PACMAN
                return maxValue(state, depth, agentNum) #return his MAX
            else: #it's a ghost
                return expValue(state, depth, agentNum) #otherwise, return the ghost's MIN


        Actions = gameState.getLegalActions(0) #get PACMAN's possible moves
        maximumValue = -100000000 #initalize max to negative inf
        bestAction = Actions[0] #
        agentNum = 0

        for action in Actions:
            successor = gameState.generateSuccessor(0, action)
            currentValue = value(successor, 1, 1)
            if maximumValue < currentValue:
                maximumValue = currentValue
                bestAction = action

        return bestAction





        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>



      0. have I won or lost?

      1. avoid the ghosts
        how close is the closest ghost?

      2. hunt scared ghosts
        how close is thr closest scared ghost?

      3. gobble the food
        how close is the closest food?
        how much food is left?

      4. nab the pellets
        is there a pellet nearby?
        how many pellets are left?



    """
    "*** YOUR CODE HERE ***"
    mario = currentGameState.getPacmanPosition()
    mushrooms = currentGameState.getFood()  # food available from current state
    mushroomsList = mushrooms.asList()
    fireFlowers = currentGameState.getCapsules()  # power pellets/capsules available from current state
    booStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in booStates]

    if currentGameState.isWin():
        return 100000000
    if currentGameState.isLose():
        return -100000000

    # find how far each ghost (boo!) is
    # also check if those ghosts are scared (boo! boo!)

    myBoos = []
    myBooBoos = []

    for kingBoo in booStates:
        if kingBoo.scaredTimer > 0:
            # mr. Boo is scared
            myBooBoos.append(util.manhattanDistance(mario, kingBoo.getPosition()))
        elif kingBoo.scaredTimer == 0:
            # mario is scared of mr Boo
            myBoos.append(util.manhattanDistance(mario, kingBoo.getPosition()))

    # find the closest ghost (boo!)
    kingBooDistance = -1
    kingBooBooDistance = -1

    if len(myBoos) > 0:
        kingBooDistance = min(myBoos)

    if len(myBooBoos) > 0:
        kingBooBooDistance = min(myBooBoos)

    # find out how far each food (mushroom) is

    myMushrooms = []

    for giantMushroom in mushroomsList:
        myMushrooms.append(util.manhattanDistance(mario, giantMushroom))

    # find the closest food (mushroom)
    giantMushroomDistance = min(myMushrooms)

    # set Weights
    booWeight = -2
    booBooWeight = -2
    giantMushroomWeight = -1.5
    mushroomsWeight = -4
    fireFlowersWeight = -20



    #calculate the HIGH SCORE
    highScore = scoreEvaluationFunction(currentGameState)

    highScore -= (booWeight) * (1.0/kingBooDistance)

    highScore += (booBooWeight) * (kingBooBooDistance)

    highScore += (giantMushroomWeight) * (giantMushroomDistance)

    highScore += (mushroomsWeight) * (len(mushroomsList))




    return highScore


    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

