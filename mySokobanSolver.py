
'''

    2020 CAB320 Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.
No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.


You are NOT allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and results in a fail for the test of your code.
This is not negotiable! 


'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [(10482822, 'Jackson', 'Sugars'), (1,' ', '' )]
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo'  if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable. Cells outside the warehouse should not be tagged as taboo.
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the puzzle with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    ##         "INSERT YOUR CODE HERE" 
    #--------------------------------------------------------------------------------------------
    def find_spaces():   
        '''
        auxiliary function to find avaliable spaces (not including target/s) within a warehouse

        @return
            a list of the coordinates of spaces in a warehouse
        '''
        spaces = []
        for column in range(warehouse.ncols):
            for row in range(warehouse.nrows):
                if (column, row) not in (warehouse.walls + warehouse.targets):
                    spaces.append((column,row))
        return spaces
    #--------------------------------------------------------------------------------------------

    spaces = find_spaces()
    #find corner taboos
    taboos = []
    while True:
        for coord in spaces:
            for xSeekCoord in ((coord[0]+1, coord[1]), (coord[0]-1, coord[1])):
                #check if cell to left or right of space is a wall
                if xSeekCoord in (warehouse.walls):
                    for ySeekCoord in ((coord[0], coord[1]+1), (coord[0], coord[1]-1)):
                        #check diagonal to determine a corner
                        if ySeekCoord in (warehouse.walls):
                            #check taboo cell is within the warehouse walls by checking up-down-left-right
                            checks = [False, False, False, False]
                            for wallcoord in warehouse.walls:      
                                #check up
                                if coord[0] == wallcoord[0]:
                                    if wallcoord[1] < coord[1]:
                                        checks[0] = True
                                #check down
                                if coord[0] == wallcoord[0]:
                                    if wallcoord[1] > coord[1]:
                                        checks[1] = True
                                #check left
                                if coord[1] == wallcoord[1]:
                                    if wallcoord[0] < coord[0]:
                                        checks[2] = True
                                #check right
                                if coord[1] == wallcoord[1]:
                                    if wallcoord[0] > coord[0]:
                                        checks[3] = True
                            if sum(checks) == len(checks):
                                taboos.append(coord)
                                continue
        break
    #check for taboo cells inbetween other taboo cells and parralel to a full wall
    newtaboos = []
    for taboo1 in taboos:
        for taboo2 in taboos:
            #check for taboo cells sharing the same x value
            if taboo1[0] == taboo2[0]:
                if taboo1[1] < taboo2[1]:
                    print("checking cells between " + str(taboo1) + "and " + str(taboo2))
                    #make list of points between
                    line = []
                    for ycoord in range(taboo1[1], taboo2[1]+1):
                        line.append((taboo1[0], ycoord))
                    #check for lack of target squares in line, and parralel walls
                    leftWalls = 0
                    rightWalls = 0
                    targetInLine = False
                    for cell in line:
                        if cell in warehouse.targets:
                            targetInLine = True
                            break
                        #check for parralel walls on either side
                        if (cell[0]+1, cell[1]) in warehouse.walls:
                            rightWalls += 1
                        if (cell[0]-1, cell[1]) in warehouse.walls:
                            leftWalls += 1
                    #determine a full wall on either side
                    if ((leftWalls > (taboo2[1] - taboo1[1])) or (rightWalls > (taboo2[1] - taboo1[1])) and targetInLine == False):
                        newtaboos.extend(line)
            #check for taboo cells sharing the same y value
            if taboo1[1] == taboo2[1]:
                if taboo1[0] < taboo2[0]:
                    #make list of points between
                    line = []
                    for xcoord in range(taboo1[0], taboo2[0]+1):
                        line.append((xcoord, taboo1[1]))
                    #check for lack of target squares in line, and parralel walls
                    upperWalls = 0
                    lowerWalls = 0
                    targetInLine = False
                    for cell in line:
                        if cell in warehouse.targets:
                            targetInLine = True
                            break
                        #check for parralel walls on either side
                        if (cell[0], cell[1]+1) in warehouse.walls:
                            lowerWalls += 1
                        if (cell[0], cell[1]-1) in warehouse.walls:
                            upperWalls += 1
                    #determine a full wall on either side
                    if ((upperWalls > (taboo2[0] - taboo1[0])) or (lowerWalls > (taboo2[0] - taboo1[0])) and targetInLine == False):
                        newtaboos.extend(line)
    taboos.extend(newtaboos)

    #return in string form
    X, Y = zip(*warehouse.walls)
    x_size, y_size = 1 + max(X), 1 + max(Y)
    vis = [[" "] * x_size for y in range(y_size)]
    for (x, y) in warehouse.walls:
        vis[y][x] = "#"
    for (x, y) in taboos:
        vis[y][x] = "X"
    return "\n".join(["".join(line) for line in vis])
    # raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    Each SokobanPuzzle instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.        
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.

    
    def __init__(self, warehouse):
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        raise NotImplementedError

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    #raise NotImplementedError()
    def move(coord, direction, distance):
        '''
        finds and returns the coordinates of an element if it were moved in
        a given direction

        @param coord: the current coordinates of an element ex. (3, 4)

        @param direction

        @return
            the new coordinates of a moved element
        '''
        if direction == 'Up':
            return (coord[0], coord[1] - distance)
        if direction == 'Down':
            return (coord[0], coord[1] + distance)
        if direction == 'Left':
            return (coord[0] - distance, coord[1])
        if direction == 'Right':
            return (coord[0] + distance, coord[1])

    for action in action_seq:
        if move(warehouse.worker, action, 1) in warehouse.walls:
            return ('Impossible')
        if move(warehouse.worker, action, 1) in warehouse.boxes:
            if move(warehouse.worker, action, 2) in (warehouse.boxes + warehouse.walls):
                return ('Impossible')
        warehouse.worker = move(warehouse.worker, action, 1)
    return warehouse.__str__()
                

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using A* algorithm and elementary actions
    the puzzle defined in the parameter 'warehouse'.
    
    In this scenario, the cost of all (elementary) actions is one unit.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using using A* algorithm and macro actions the puzzle defined in 
    the parameter 'warehouse'. 
    
    A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    In this scenario, the cost of all (macro) actions is one unit. 

    @param warehouse: a valid Warehouse object

    @return
        If the puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban_elem(warehouse, push_costs):
    '''
    In this scenario, we assign a pushing cost to each box, whereas for the
    functions 'solve_sokoban_elem' and 'solve_sokoban_macro', we were 
    simply counting the number of actions (either elementary or macro) executed.
    
    When the worker is moving without pushing a box, we incur a
    cost of one unit per step. Pushing the ith box to an adjacent cell 
    now costs 'push_costs[i]'.
    
    The ith box is initially at position 'warehouse.boxes[i]'.
        
    This function should solve using A* algorithm and elementary actions
    the puzzle 'warehouse' while minimizing the total cost described above.
    
    @param 
     warehouse: a valid Warehouse object
     push_costs: list of the weights of the boxes (pushing cost)

    @return
        If puzzle cannot be solved return 'Impossible'
        If a solution exists, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

