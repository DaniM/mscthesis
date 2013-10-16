'''
Created on 14/10/2013

@author: Dani

Basic implementation of an influence map, heavily based in 
http://aigamedev.com/open/tutorial/influence-map-mechanics/
'''

import math

#
# Some decay functions
#
def exponentialDecay(influence, distance, decay):
    return influence * math.exp( -distance * decay )

def linearDecay(influence, distance, decay):
    return ( influence / ( distance + 1) ) * decay

def quadraticDecay(influence, distance, decay):
    return ( influence / ( ( distance + 1) ** 2) ) * decay

class Unit:
    '''Just a basic wrapper for units in order to represent it in the map'''
    def __init__(self, strength, coords):
        self.strength = strength
        self.coords = coords

class InfluenceMap(object):
    '''
    Grid based influence map
    '''
    def __init__(self, momentum, decayFunction, threshold, decay, grid):
        '''
        Constructor
        '''
        self.momentum = momentum
        self.threshold = threshold
        self.decay = decay
        self.decayFunction = decayFunction
        self.map = grid
        self.height = len(grid)
        self.width = len(grid[0])
        
        #use double buffering
        self.buffer = []
        self.buffer_bk = []
        for i in xrange(self.height):
            b_row = []
            b_bkrow = []
            for _ in xrange(self.width):
                b_row.append(0)
                b_bkrow.append(0)
            self.buffer.append(b_row)
            self.buffer_bk.append(b_bkrow)
            
    def neighbors(self,location):
        '''8-neighbors'''
        #check if its the 
        x = location[0]
        y = location[1]
        neighbors = []
        
        left = x > 0
        right = x < (self.width - 1)
        up = y > 0
        down = y < (self.height - 1)
        
        #check diagonals
        if up and left and self.isWalkable([x-1,y-1]):
            neighbors.append((x-1,y-1))
        if right and down and self.isWalkable([x+1,y+1]):
            neighbors.append((x+1,y+1))
        if up and right and self.isWalkable([x+1,y-1]):
            neighbors.append((x+1,y-1))
        if left and down and self.isWalkable([x-1,y+1]):
            neighbors.append((x-1,y+1))
        #sides
        if left and self.isWalkable([x-1,y]):
            neighbors.append((x-1,y))
        if right and self.isWalkable([x+1,y]):
            neighbors.append((x+1,y))
        if up and self.isWalkable([x,y-1]):
            neighbors.append((x,y-1))
        if down and self.isWalkable([x,y+1]):
            neighbors.append((x,y+1))
            
        return neighbors
            
    def propagate(self):
        for i in xrange(self.height):
            for j in xrange(self.width):
                location = [j,i]
                if not self.isWalkable(location):
                    continue
                
                maxInfluence = 0
                neighbors = self.neighbors(location)
                for n in neighbors:
                    distance = self.distance(location,n)
                    influence = self.decayFunction(self.buffer[n[1]][n[0]],distance,self.decay)
                    maxInfluence = max(maxInfluence,influence)
                newInfluence = self.momentum * self.buffer[i][j] + (1-self.momentum) * maxInfluence
                if newInfluence < self.threshold:
                    newInfluence = 0
                self.buffer_bk[i][j] = newInfluence
        
        #swap buffers
        self.buffer,self.buffer_bk = self.buffer_bk, self.buffer
    
    def updatePropagators(self, units):
        '''Set the influence of the units over the cells it's in'''
        for u in units:
            self.buffer[u.coords[1]][u.coords[0]] = u.strength
    
    def isWalkable(self,location):
        return self.map[location[1]][location[0]] < 1
    
    def distance(self,location1,location2):
        '''Euclidean distance'''
        x = (location2[0] - location1[0])
        y = (location2[1] - location1[1])
        if x == 0 and y == 0:
            return 0
        elif x == 0 or y == 0:
            return 1
        else:
            return 1.4142
        
    def printBuffer(self):
        for i in xrange(self.height):
            print '['+ ', '.join('%.3f'%x for x in self.buffer[i]) + ']'
                

grid = [[0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 2, 0, 0, 1, 0, 0],
        [0, 2, 2, 0, 0, 2, 2, 0],
        [0, 0, 0, 0, 1, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1]]
        
if __name__ == '__main__':
    # one unit at [x=0,y=0] moves to the right [x=7,y=0]
    unit = Unit(10, [0,0])
    imap = InfluenceMap(0.5, linearDecay, 0.05, 1, grid)
    # update the propagators after 5 cycles
    for i in xrange(7):
        unit.coords = [i,0]
        imap.updatePropagators([unit])
        imap.printBuffer()
        # propagate 5 times
        for j in xrange(5):
            print j+1
            imap.propagate()
            imap.printBuffer()