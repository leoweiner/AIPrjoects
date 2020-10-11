
# Leo Weiner -- lzweine@emory.edu
# THIS  CODE  WAS MY OWN WORK , IT WAS  WRITTEN  WITHOUT  CONSULTING  ANY
# SOURCES  OUTSIDE  OF THOSE  APPROVED  BY THE  INSTRUCTOR. Leo Weiner



# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    "*** YOUR CODE HERE ***"
    #initalize the frontier using the initial state of problem
    initialNode = problem.getStartState()
    fringe = util.Stack()
    fringe.push((initialNode, []))
    #initalize the explored set to be empty
    exploredSet = []
    #loop DO
    #if the frontier is empty then return failure
    while not (fringe.isEmpty()):
        #choose a leaf node and remove it from the frontier
        coordinates, steps = fringe.pop()
        #if the node contains a goal state then return corresoponding solution
        if problem.isGoalState(coordinates):
            return steps
        #add the node to the explored set
        exploredSet.append(coordinates)
        #expand the chosen node, adding the resulting nodes to the frontier
            #only if not in the frontier or explored set
        for successor in problem.getSuccessors(coordinates):
            inFringe = False
            inExplored = False
            for node in fringe.list:
                if successor[0] == node:
                    inFringe = True
            for node in exploredSet:
                if successor[0] == node:
                    inExplored = True
            if not inExplored and not inFringe:
                action = steps + [successor[1]]
                fringe.push((successor[0], action))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    # same as DFS, use Queue as fringe instead of stack
    initialNode = problem.getStartState()
    fringe = util.Queue()
    fringe.push((initialNode, []))
    exploredSet = []
    while not (fringe.isEmpty()):
        coordinates, steps = fringe.pop()
        if problem.isGoalState(coordinates):
            return steps
        exploredSet.append(coordinates)
        for successor in problem.getSuccessors(coordinates):
            inFringe = False
            inExplored = False
            for node in fringe.list:
                if successor[0] == node:
                    inFringe = True
            for node in exploredSet:
                if successor[0] == node:
                    inExplored = True
            if not inExplored and not inFringe:
                action = steps + [successor[1]]
                fringe.push((successor[0], action))
                # add successor to exploredSet
                exploredSet.append(successor[0])

    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    # search is the same, use PQ as fringe.
    # ((coordinates , stepss , cost), priority)

    initialNode = problem.getStartState()
    fringe = util.PriorityQueue()
    fringe.push((initialNode, [], 0), 0)
    exploredSet = []
    while not (fringe.isEmpty()):
        coordinates, steps, cost = fringe.pop()

        # check if coordinates have been explored
        inExplored = False
        for node in exploredSet:
            if coordinates == node:
                inExplored = True

        # if they havent been, check if goal and loop through successors
        if not inExplored:
            if problem.isGoalState(coordinates):
                return steps

            exploredSet.append(coordinates)

            for successor in problem.getSuccessors(coordinates):

                price = cost + successor[2]
                action = steps + [successor[1]]
                fringe.push((successor[0], action, price), price)


    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    # same as UCS but priority is the heuristic
    initialNode = problem.getStartState()
    if problem.isGoalState(initialNode):
        return []
    fringe = util.PriorityQueue()
    fringe.push((initialNode, [], 0), heuristic(initialNode, problem))
    exploredSet = []
    while not (fringe.isEmpty()):
        coordinates, steps, cost = fringe.pop()

        inExplored = False
        for node in exploredSet:
            if coordinates == node:
                inExplored = True

        if not inExplored:
            if problem.isGoalState(coordinates):
                return steps

            exploredSet.append(coordinates)

            for successor in problem.getSuccessors(coordinates):
                price = cost + successor[2]
                action = steps + [successor[1]]
                # f(n) = h(n) + g(n)
                fringe.push((successor[0], action, price), (heuristic(successor[0], problem)+price))


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
