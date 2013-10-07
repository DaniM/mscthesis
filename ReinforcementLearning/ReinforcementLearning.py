'''
Created on 07/10/2013

@author: Dani

Reinforcement learning implementation extracted from
'Artificial Intelligence for Games' http://ai4g.com/

Example test from AI: a modern approach http://aima.cs.berkeley.edu/

'''

import random

class ReinforcementProblem:
    """Common interface to all problems"""
    
    def getRandomState(self):
        pass
    
    def getAvailableActions(self,state):
        pass
    
    def takeAction(self,state,action):
        pass
    
class QValueStore:
    """Common interface for storagement"""
    def getQValue(self,state,action):
        pass
    
    def getBestAction(self,state):
        pass
    
    def storeQValue(self,state,action,value):
        pass
    
def QLearning(problem,qstorage,iterations,alpha,gamma,rho,nu):
    pass


class RAndNStoragement(QValueStore):
    '''Simple matrix storagement implementation for the problem.'''
    def __init__(self, states, initialValues):
        if len(initialValues) == 0:
            self._values = [ [0]*4 for r in states ]
        else:
            self._values = initialValues
            

    def getQValue(self, state, action):
        stateIdx = self._stateHash(state)
        actionsIdx =  self._actionHash(action)
        return self._values[stateIdx][actionsIdx]


    def getBestAction(self, state):
        stateIdx = self._stateHash(state)
        actionIdx = max(xrange(len(self._values[stateIdx])), key=lambda x: self._values[stateIdx][x])
        if actionIdx == 0:
            return 'left'
        if actionIdx == 1:
            return 'up'
        if actionIdx == 2:
            return 'right'
        if actionIdx == 3:
            return 'down'

    def storeQValue(self, state, action, value):
        stateIdx = self._stateHash( state )
        actionsIdx =  self._actionHash
        self._values[stateIdx][actionsIdx] = value
        
    def _stateHash(self,state):
        '''Return an integer id based on agent position'''
        return 0
    
    def _actionHash(self,action):
        '''Convert the four actions to integers'''
        if action == 'left':
            return 0
        if action == 'up':
            return 1
        if action == 'right':
            return 2
        if action == 'down':
            return 3
        
    def printLearnedPolicy(self):
        '''print the learned policy from the Q-values'''
        pass
        
 
class RAndNAgentProblem(ReinforcementProblem):
    '''Russell & Norvig agent implementation'''
    
    #dimensions of the world
    _rows = 3
    _columns = 4
    
    #_rewards as a table
    _rewards = [[-0.04,-0.04,-0.04,      1],
               [-0.04,-0.04,-0.04,     -1],
               [-0.04,-0.04,-0.04,  -0.04]]
    
    def __init__(self, agentInitialPosition ):
        if len(agentInitialPosition) == 0:
            self.initialState = self.getRandomState()
        else:
            self.initialState = RAndNState(agentInitialPosition) 

    def getRandomState(self):
        '''Return a (valid) random state'''
        # note: not all states are valid
        while True:
            position = [random.randint(0,RAndNAgentProblem._columns-1)
                           ,random.randint(0,RAndNAgentProblem._rows-1)]
            if RAndNState._grid[position[1]][position[0]] == 0:
                return RAndNState(position)


    def getAvailableActions(self, state):
        return state.getAvailableActions()


    def takeAction(self, state, action):
        '''Return a tuple with the new state and the reward'''
        
        #For this problem we trait the actions as strings
        if action == 'left':
            return ( RAndNState( [state.agentPosition[0]+1, state.agentPosition[1]] ), RAndNAgentProblem._rewards[state.agentPosition[1]][state.agentPosition[0]] )
        elif action == 'right':
            pass
        


class RAndNState:
    '''Representation of the state. Only the agent position is needed'''
    
    _grid = [[0,0,0,0],
             [0,1,0,0],
             [0,0,0,0]]
    
    def __init__(self, agentInitialPosition):
        self.agentPosition = agentInitialPosition
    
    def getAvailableActions(self):
        actions = []
        if self.agentPosition[0] > 0 and RAndNState._grid[self.agentPosition[1]][self.agentPosition[0] - 1] == 0:
            actions.append('left')
        if self.agentPosition[1] > 0 and RAndNState._grid[self.agentPosition[1] - 1][self.agentPosition[0]] == 0:
            actions.append('up')
        if self.agentPosition[0] < RAndNAgentProblem._columns - 1 and RAndNState._grid[self.agentPosition[1]][self.agentPosition[0] + 1] == 0:
            actions.append('right')
        if self.agentPosition[1] < RAndNAgentProblem._rows - 1 and RAndNState._grid[self.agentPosition[1] + 1][self.agentPosition[0]] == 0:
            actions.append('down')
        return actions
    
def main():
    #start from a random state
    problem = RAndNAgentProblem([])
    #initialize the storagement with 0 for all the cells but the unwalkable one
    storage = RAndNStoragement(12,
                               [[0,0,               0,0],
                                [0,float('-inf'),   0,0],
                                [0,0,               0,0]])   
    
if __name__ == '__main__':
    main()