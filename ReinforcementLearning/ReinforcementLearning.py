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
    
    def isTerminalState(self):
        pass
    
class QValueStore:
    """Common interface for storagement"""
    def getQValue(self,state,action):
        pass
    
    def getBestAction(self,state,actions):
        pass
    
    def storeQValue(self,state,action,value):
        pass
    
def QLearning(problem,qstorage,iterations,alpha,gamma,rho,nu):
    '''Primarily used when there's no terminal state'''
    state = problem.getRandomState()
    for i in xrange(iterations):
        #pick a random state once in a while
        if random.random() < nu:
            state = problem.getRandomState()
        actions = problem.getAvailableActions(state)
        #make a random choice sometimes
        if random.random() < rho:
            action = random.choice(actions)
        #otherwise pick the best
        else:
            action = qstorage.getBestAction(state,actions)
        #reward and next state
        newState,reward = problem.takeAction(state,action)
        q = qstorage.getQValue(state,action)
        maxQ = qstorage.getQValue(newState,qstorage.getBestAction(newState,problem.getAvailableActions(newState)))
        
        #apply learning rule
        Q = (1-alpha) * q + alpha * (reward + gamma * maxQ)
        
        qstorage.storeQValue(state,action,Q)
        
        state = newState
        
        

def QLearningEpisodic(problem,qstorage,episodes,alpha,gamma,rho):
        for e in xrange(episodes):
            print 'episode ',e
            state = problem.getRandomState()
            while not problem.isTerminalState(state):
                actions = problem.getAvailableActions(state)
                #make a random choice sometimes
                if random.random() < rho:
                    action = random.choice(actions)
                #otherwise pick the best
                else:
                    action = qstorage.getBestAction(state,actions)
                #reward and next state
                newState,reward = problem.takeAction(state,action)
                q = qstorage.getQValue(state,action)
                maxQ = qstorage.getQValue(newState,qstorage.getBestAction(newState,problem.getAvailableActions(newState)))
                
                #apply learning rule
                Q = (1-alpha) * q + alpha * (reward + gamma * maxQ)
                
                qstorage.storeQValue(state,action,Q)
                
                state = newState
            print 'episode end'
                
        


class RAndNStoragement(QValueStore):
    '''Simple matrix storagement implementation for the problem.'''
    def __init__(self, states, actions, initialValue):
        self._values = [ [initialValue]*actions for r in xrange(states) ]
            

    def getQValue(self, state, action):
        stateIdx = self._stateHash(state)
        actionsIdx =  self._actionHash(action)
        return self._values[stateIdx][actionsIdx]


    def getBestAction(self, state, actions):
        stateIdx = self._stateHash(state)
        actionIdx = self._actionHash( max(actions, key=lambda x: self._values[stateIdx][self._actionHash(x)]) )
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
        actionsIdx =  self._actionHash(action)
        self._values[stateIdx][actionsIdx] = value
        
    def _stateHash(self,state):
        '''Return an integer id based on agent position'''
        return state.agentPosition[1] * RAndNAgentProblem._columns + state.agentPosition[0] 
    
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
        
 
class RAndNAgentProblem(ReinforcementProblem):
    '''Russell & Norvig agent implementation'''
    
    #dimensions of the world
    _rows = 3
    _columns = 4
    
    #_rewards as a table
    _rewards = [[-0.04,-0.04,-0.04,      1],
                [-0.04,    0,-0.04,     -1],
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
            newState = RAndNState( [state.agentPosition[0]-1, state.agentPosition[1]] )
            return ( newState, RAndNAgentProblem._rewards[newState.agentPosition[1]][newState.agentPosition[0]] )
        elif action == 'right':
            newState = RAndNState( [state.agentPosition[0]+1, state.agentPosition[1]] )
            return ( newState, RAndNAgentProblem._rewards[newState.agentPosition[1]][newState.agentPosition[0]] )
        elif action == 'up':
            newState = RAndNState( [state.agentPosition[0], state.agentPosition[1] - 1] )
            return ( newState , RAndNAgentProblem._rewards[newState.agentPosition[1]][newState.agentPosition[0]] )
        elif action == 'down':
            newState = RAndNState( [state.agentPosition[0], state.agentPosition[1] + 1] )
            return ( newState, RAndNAgentProblem._rewards[newState.agentPosition[1]][newState.agentPosition[0]] )
        else:
            return ( state, RAndNAgentProblem._rewards[state.agentPosition[1]][state.agentPosition[0]] )
        
    def isTerminalState(self,state):
        return state.agentPosition[0] == 3 and ( state.agentPosition[1] == 0 or state.agentPosition[1] == 1 ) 
        


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
    problem = RAndNAgentProblem([])
    #initialize the storagement with 0 for all the cells
    storage = RAndNStoragement(12, 4, 0 )
    QLearningEpisodic(problem, storage, 10000, 0.3, 0.75, 0.2)
    
    print 'Learned Policy'
    #policy print
    policy = []
    for y in xrange(RAndNAgentProblem._rows):
        row = []
        for x in xrange(RAndNAgentProblem._columns):
            if RAndNState._grid[y][x] == 1:
                row.append('X')
            else:
                state = RAndNState([x,y])
                
                if problem.isTerminalState(state):
                    row.append('o')
                    continue
                
                actions = problem.getAvailableActions(state)
                bestAction = storage.getBestAction(state, actions)
                row.append(bestAction)
        policy.append(row)
        
    for r in xrange(len(policy)):
        print policy[r]
    
    print 'RL supponsing there\'s no terminal state'
    #initialize the storagement with 0 for all the cells
    storage = RAndNStoragement( 12, 4, 0 )
    QLearning(problem, storage, 10000, 0.3, 0.75, 0.2, 0.1)
    
    #policy print
    print 'Learned policy'
    policy = []
    for y in xrange(RAndNAgentProblem._rows):
        row = []
        for x in xrange(RAndNAgentProblem._columns):
            if RAndNState._grid[y][x] == 1:
                row.append('X')
            else:
                state = RAndNState([x,y])
                
                if problem.isTerminalState(state):
                    row.append('o')
                    continue
                
                actions = problem.getAvailableActions(state)
                bestAction = storage.getBestAction(state, actions)
                row.append(bestAction)
        policy.append(row)
        
    for r in xrange(len(policy)):
        print policy[r]
    
if __name__ == '__main__':
    main()