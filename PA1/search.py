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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import math

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    # initialize actions list
    actions = []
    if problem.isGoalState(problem.getStartState()):
        return actions
    else:
        # initialize fringe and explored
        fringe = util.Stack()
        explored = []
        fringe.push((problem.getStartState(), actions))
        # begin loop
        while True:
            if fringe.isEmpty():
                return actions
            else:
                # pop next node from the priority queue and add it to explored
                currentState, poppedActions = fringe.pop()
                if not currentState in explored:
                    explored.append(currentState)
                    if problem.isGoalState(currentState):
                        actions = poppedActions
                        return actions
                    for successor in problem.getSuccessors(currentState):
                        # get path to current node and add instruction returned with getSuccessors to get path to each successor
                        successorState, successorDirection, successorCost = successor
                        newActions = poppedActions + [successorDirection]
                        # add to fringe
                        fringe.push((successorState, newActions))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    # initialize actions list
    actions = []
    if problem.isGoalState(problem.getStartState()):
        return actions
    else:
        # initialize fringe and explored
        fringe = util.Queue()
        explored = []
        fringe.push((problem.getStartState(), actions))
        # begin loop
        while True:
            if fringe.isEmpty():
                return actions
            else:
                # pop next node from the priority queue and add it to explored
                currentState, poppedActions = fringe.pop()
                if not currentState in explored:
                    explored.append(currentState)
                    if problem.isGoalState(currentState):
                        actions = poppedActions
                        return actions
                    for successor in problem.getSuccessors(currentState):
                        # get path to current node and add instruction returned with getSuccessors to get path to each successor
                        successorState, successorDirection, successorCost = successor
                        newActions = poppedActions + [successorDirection]
                        # add to fringe
                        fringe.push((successorState, newActions))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # initialize actions list
    actions = []
    if problem.isGoalState(problem.getStartState()):
        return actions
    else:
        # initialize fringe and explored
        fringe = util.PriorityQueue()
        explored = []
        fringe.push((problem.getStartState(), actions, 0), 0)
        # begin loop
        while True:
            if fringe.isEmpty():
                return actions
            else:
                # pop next node from the priority queue and add it to explored
                currentState, poppedActions, poppedCost = fringe.pop()
                if not currentState in explored:
                    explored.append(currentState)
                    if problem.isGoalState(currentState):
                        actions = poppedActions
                        return actions
                    for successor in problem.getSuccessors(currentState):
                        # get path to current node and add instruction returned with getSuccessors to get path to each successor
                        successorState, successorDirection, successorCost = successor
                        newActions = poppedActions + [successorDirection]
                        newCost = poppedCost + successorCost
                        priority = newCost
                        # add to fringe
                        fringe.push((successorState, newActions, newCost), priority)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    # initialize actions list
    actions = []
    if problem.isGoalState(problem.getStartState()):
        return actions
    else:
        # initialize fringe and explored
        fringe = util.PriorityQueue()
        explored = []
        fringe.push((problem.getStartState(), actions, 0), 0)
        # begin loop
        while True:
            if fringe.isEmpty():
                return actions
            else:
                # pop next node from the priority queue and add it to explored
                currentState, poppedActions, poppedCost = fringe.pop()
                if not currentState in explored:
                    explored.append(currentState)
                    if problem.isGoalState(currentState):
                        actions = poppedActions
                        return actions
                    for successor in problem.getSuccessors(currentState):
                        # get path to current node and add instruction returned with getSuccessors to get path to each successor
                        successorState, successorDirection, successorCost = successor
                        newActions = poppedActions + [successorDirection]
                        newCost = poppedCost + successorCost
                        priority = newCost + heuristic(successorState, problem)
                        # add to fringe
                        fringe.push((successorState, newActions, newCost), priority)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch