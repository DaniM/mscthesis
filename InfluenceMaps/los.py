'''
Created on 13/11/2012

@author: Dani
'''
import math

def bresenham(x0, y0, x1, y1):
    '''
    http://en.wikipedia.org/wiki/Bresenham's_line_algorithm
    '''
    dx = abs(x1-x0)
    dy = abs(y1-y0) 
    
    x_inc = 0
    if x1 > x0:
        x_inc = 1
    elif x0 > x1:
        x_inc = -1
    
    y_inc = 0
    if y1 > y0:
        y_inc = 1
    elif y0 > y1:
        y_inc = -1
        
    err = dx-dy
    
    x = x0
    y = y0
    visited = []
    visited.append( [x, y] )
    
    while ( x != x1 or y != y1 ):
        e2 = 2*err
        if e2 > -dy: 
            err = err - dy
            x = x + x_inc
        if e2 <  dx : 
            err = err + dx
            y = y + y_inc       
        visited.append( [x, y] )
             
    return visited

def grid_linecasting( x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x = x0
    y = y0
    #the number of cells intersected are 1 + |x1-x0| + |y1-y0|
    n = 1 + dx + dy
    
    x_inc = 0
    if x1 > x0:
        x_inc = 1
    elif x0 > x1:
        x_inc = -1
    
    y_inc = 0
    if y1 > y0:
        y_inc = 1
    elif y0 > y1:
        y_inc = -1
        
    error = dx - dy
    # range is from -d to d
    dx *= 2
    dy *= 2

    visited = []

    for i in range(n):
        visited.append( [x, y] )
        if (error > 0):
            x += x_inc
            error -= dy
        else:
            y += y_inc
            error += dx
    return visited

def grid_linecast( x0, y0, x1, y1, grid, isBlockedFunction):
    '''
    Line cast to end point, fails if a value of isBlockedFunction is found. Returns a tuple with success or failure and the path to reached point
    '''
    
    x0 = int( x0 )
    x1 = int( x1 )
    y0 = int( y0 )
    y1 = int( y1 )
    
    dx = abs( x1 - x0 )
    dy = abs( y1 - y0 )
    
    x = x0
    y = y0
    #the number of cells intersected are 1 + |x1-x0| + |y1-y0|
    n = 1 + dx + dy
    
    x_inc = 0
    if x1 > x0:
        x_inc = 1
    elif x0 > x1:
        x_inc = -1
    
    y_inc = 0
    if y1 > y0:
        y_inc = 1
    elif y0 > y1:
        y_inc = -1
        
    error = dx - dy;
    # range is from -d to d
    dx *= 2;
    dy *= 2;

    visited = []
    success = True
    for i in range(n):
        visited.append( [x, y] )
        
        if isBlockedFunction( grid[y][x] ):
            success = False
            break
        
        if ( error > 0 ):
            x += x_inc
            error -= dy
        elif ( error < 0 ):
            y += y_inc
            error += dx
        else:
            #if it's 0, we "don't care" about which way, so take the one which is not blocked
            #NOTE: the way this algorithm works let us handle this extreme case
            if not isBlockedFunction( grid[y + y_inc][x] ):
                y += y_inc
                error += dx
            else:
                x += x_inc
                error -= dy
                
    return ( success, visited )

# sorry for the numbering, python doesn't support method override
def grid_linecast_checkhit1( x0, y0, x1, y1, grid, queryFunction, distance=float('inf')):
    '''
    From x0,y0 with the slope using x1,y1. Try to find a queryFunction value in that direction until it reach max distance or limits of grid or a blocked cell
    '''
    x0 = int( x0 )
    x1 = int( x1 )
    y0 = int( y0 )
    y1 = int( y1 )
    
    dx = abs( x1 - x0 )
    dy = abs( y1 - y0 )
    
    x = x0
    y = y0
    
    x_inc = 0
    if x1 > x0:
        x_inc = 1
    elif x0 > x1:
        x_inc = -1
    
    y_inc = 0
    if y1 > y0:
        y_inc = 1
    elif y0 > y1:
        y_inc = -1
        
    error = dx - dy;
    # range is from -d to d
    dx *= 2;
    dy *= 2;
    
    #line
    visited = []
    hit = False
    
    #dirty little trick, the distance must include the starting cell
    if distance < float('inf'):
        distance += 1
    
    #bounds
    width = len( grid[0] )
    height = len( grid )
    
    #out of bounds checking
    while( ( 0 <= x < width ) and ( 0 <= y < height ) and distance > 0 ):
        visited.append( [x, y] )
        
        if queryFunction( grid[y][x] ):
            hit = True
            break
        
        if ( error > 0 ):
            x += x_inc
            error -= dy
        elif ( error < 0 ):
            y += y_inc
            error += dx
        else:
            #try the query
            if queryFunction( grid[y + y_inc][x] ):
                y += y_inc
                error += dx
            else:
                x += x_inc
                error -= dy
        distance = distance - 1
        
    return ( hit, visited )

def grid_linecast_checkhit2( x0, y0, theta, grid, queryFunction, distance=float('inf')):
    '''
    From x0,y0 with the slope theta (angle). Try to find a queryFunction value in that direction until it reach max distance or limits of grid or a blocked cell
    '''
    x0 = int( x0 )
    y0 = int( y0 )
    
    dx = math.cos( math.radians( theta ) )
    dy = math.sin( math.radians( theta ) )
    
    x = x0
    y = y0
    
    x_inc = 0
    if dx > 0:
        x_inc = 1
    elif dx < 0:
        x_inc = -1
    
    y_inc = 0
    if dy > 0:
        y_inc = 1
    elif dy < 0:
        y_inc = -1
        
    error = dx - dy;
    # range is from -d to d
    dx *= 2;
    dy *= 2;
    
    #line
    visited = []
    hit = False
    
    #dirty little trick, the distance must include the starting cell
    if distance < float('inf'):
        distance += 1
    
    #bounds
    width = len( grid[0] )
    height = len( grid )
    
    #out of bounds checking
    while( ( 0 <= x < width ) and ( 0 <= y < height ) and distance > 0 ):
        visited.append( [x, y] )
        
        if queryFunction( grid[y][x] ):
            hit = True
            break
        
        if ( error > 0 ):
            x += x_inc
            error -= dy
        elif ( error < 0 ):
            y += y_inc
            error += dx
        else:
            #try the query
            if queryFunction( grid[y + y_inc][x] ):
                y += y_inc
                error += dx
            else:
                x += x_inc
                error -= dy
        distance = distance - 1
        
    return ( hit, visited )

def print_grid(grid):
        for i in range(len(grid)):
            print '['+ ', '.join('%i'%x for x in grid[i]) + ']'
        print ' '

grid = [[0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0]]

#neighborhood [x,y] relative, 8-neighborhood
neighboursTest1 = [[-1,0],#left
                   [-1,-1],#up-left
                   [0,-1],#up
                   [1,-1],#up-right
                   [1,0],#right
                   [1,1],#right-down
                   [0,1],#down
                   [-1,1]]#left-down 

blockedGridTest1 = [[0,0,0],
                    [0,0,1],
                    [1,1,1]]

blockedGridTest = [[0,0,0],
                   [0,1,0],
                   [0,0,0]]

blockedGridTest2 = [[0,1,0],
                    [1,0,1],
                    [0,1,0]]

blockedGridTest3 = [[0,0,0,0,0],
                    [0,0,1,0,0],
                    [0,1,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0]]

#test as a convolution matrix
neighborhoodConvTest3 = [[0,0,1,0,0],
                         [0,1,1,1,0],
                         [1,1,0,1,1],
                         [0,1,1,1,0],
                         [0,0,1,0,0]]

blockedGridTest4 = [[0,0,0,0,0],
                    [0,0,1,0,0],
                    [0,1,0,1,0],
                    [0,0,1,0,0],
                    [0,0,0,0,0]]


blockedGridTest5 =      [[0,0,0,0,0,0,0],
                         [0,0,1,0,0,0,0],
                         [0,1,1,0,1,1,0],
                         [1,1,1,0,1,0,0],
                         [0,1,1,1,1,1,0],
                         [0,0,1,1,1,0,0],
                         [0,0,0,1,0,0,0]]

neighborhoodConvTest5 = [[0,0,0,1,0,0,0],
                         [0,0,1,1,1,0,0],
                         [0,1,1,1,1,1,0],
                         [1,1,1,0,1,1,1],
                         [0,1,1,1,1,1,0],
                         [0,0,1,1,1,0,0],
                         [0,0,0,1,0,0,0]]

def isBlocked1Meter( value ):
    return value >= 1

if __name__ == '__main__':
    
    line = grid_linecasting(0, 3, 2, 0)
    for cell in line:
        grid[cell[1]][cell[0]] = 1
    print_grid(grid)
    
    grid = [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]
    
    line = bresenham(0, 10, 4, 0)
    for cell in line:
        grid[cell[1]][cell[0]] = 1
    print_grid(grid)
    
    
    print 'Linecast grid Testing'
    
    for n in neighboursTest1:
        print [1 + n[0], 1 + n[1]], grid_linecast(1, 1, 1 + n[0], 1 + n[1], blockedGridTest, isBlocked1Meter)
    
    print 'Test 1'
    for n in neighboursTest1:
        print [1 + n[0], 1 + n[1]], grid_linecast(1, 1, 1 + n[0], 1 + n[1], blockedGridTest1, isBlocked1Meter)
        
    print 'Test 2'
    #test 2 -> all failures
    for n in neighboursTest1:
        testResult = grid_linecast(1, 1, 1 + n[0], 1 + n[1], blockedGridTest2, isBlocked1Meter)
        assert testResult[0] is False
        print [1 + n[0], 1 + n[1]], testResult 
    
    print 'Test 3'
    
    #convolution matrix size
    size = 5
    for i in range( size ):
        for j in range( size ):
            if neighborhoodConvTest3[i][j] == 1:
                testResult = grid_linecast(2, 2, j, i, blockedGridTest3, isBlocked1Meter)
                print [i, j], testResult 
    
    print 'Test 4'
    #all failures
    for i in range( size ):
        for j in range( size ):
            if neighborhoodConvTest3[i][j] == 1:
                testResult = grid_linecast(2, 2, j, i, blockedGridTest4, isBlocked1Meter)
                assert testResult[0] is False
                print [i, j], testResult 
                
    print 'line check hit'
    
    grid = [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,1,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]
    
    hit = grid_linecast_checkhit1(0, 10, 1, 0, grid, isBlocked1Meter, 100)
    assert hit[0] is True
    for cell in hit[1]:
        grid[cell[1]][cell[0]] = 1
    print_grid(grid)
    