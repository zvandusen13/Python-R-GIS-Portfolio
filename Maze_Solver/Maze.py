from __future__ import annotations

from enum import Enum
from typing import NamedTuple
from Stack import *
from Queue import *
from PriorityQueue import *
import random

###########################################################
class Contents(str, Enum):
    ''' create an enumeration to define what the visual contents 
        of a Cell are; using str as a "mixin" forces all the entries
        to be strings; using an enum means no cell entry can be 
        anything other than the options here '''
    EMPTY   = " "
    START   = "◎"  # "S"
    GOAL    = "◆"  # "G"
    BLOCKED = "░"  # "X"
    PATH    = "★"  # "*"

    def __str__(self) -> str: return self.value

###########################################################
class Position(NamedTuple):
    ''' named tuple that allows us to use .row and .col rather 
        than the less-easy-to-read [0] and [1] for accessing 
        values'''
    row: int
    col: int

    def __str__(self) -> str: return f"({self.row},{self.col})"

###########################################################
class Cell:
    ''' class that allows us to use Cell as a data type -- 
        row, column, & cell contents '''
    __slots__ = ('_position', '_contents', '_parent')

    def __init__(self, row: int, col: int, contents: Contents):
        self._position: Position = Position(row, col)
        self._contents: Contents = contents
        self._parent:   Cell     = None

    def __str__(self) -> str:
        contents = "[EMPTY]" if self._contents == Contents.EMPTY else self._contents
        result = f"({self._position.row},{self._position.col}): {contents}"
        if self._parent is not None: 
            result += f"({self._parent._position.row}, {self._parent._position.col})"
        return result

    def getPosition(self) -> Position:    return self._position
    def getParent(self)   -> Cell | None: return self._parent

    def setParent(self, parent: Cell) -> None:  self._parent = parent 
    def markOnPath(self)              -> None:  self._contents = Contents.PATH

    def isBlocked(self) -> bool:  return self._contents == Contents.BLOCKED
    def isGoal(self)    -> bool:  return self._contents == Contents.GOAL

    def __eq__(self, other: Cell) -> bool:
        return self._position == other._position and \
               self._contents == other._contents and \
               self._parent   is other._parent
        
###########################################################
class Maze:
    __slots__ = ('_num_rows', '_num_cols', '_start', '_goal', '_grid', '_num_cells_pushed', '_path_length')

    def __init__(self, num_rows: int = 10, num_cols: int = 10, \
                       start: Position = Position(0,0), \
                       goal:  Position = Position(9,9), \
                       proportion_blocked: float = 0.2, \
                       debug: bool = False) -> None:
        ''' Maze initializer method
        Parameters:
            num_rows:           number of rows in the grid
            num_cols:           number of columns in the grid
            start:              Position object indicating (row,col) of the start cell
            goal:               Position object indicating (row,col) of the goal cell
            proportion_blocked: proportion of cells to be blocked (between 0.0 and 1.0)
            debug:              whether to use one of the Maze examples from slides
        Raises:
            TypeError if proportion_blocked is not float
            TypeError if start of goal is not Position
            ValueError if proportion_blocked is outside (0,1)
        '''
        if not isinstance(proportion_blocked, float):
            raise TypeError("proportion_blocked argument must be a float")
        if proportion_blocked < 0 or proportion_blocked > 1:
            raise ValueError("proportion_blocked argument must be a float b/w 0 and 1")
        if not isinstance(start, Position) or not isinstance(goal, Position):
            raise TypeError("start and goal must both be Position objects")

        if debug:  # set up 6X5 maze example from course slides
            num_rows = 6; num_cols = 5;
            start = Position(5, 0)
            goal  = Position(0, 4)

        self._num_rows: int  = num_rows
        self._num_cols: int  = num_cols

        # set up the start and goal Cell objects
        self._start: Cell = Cell(start.row, start.col, Contents.START)
        self._goal:  Cell = Cell(goal.row,  goal.col,  Contents.GOAL)

        # create a 2D list of Cell objects, all initially empty
        self._grid: list[ list[Cell] ] = \
            [ [Cell(r,c, Contents.EMPTY) for c in range(num_cols)] \
              for r in range(num_rows) ]

        # overwrite the appropriate locations with the start and goal Cells
        self._grid[start.row][start.col] = self._start
        self._grid[goal.row][goal.col]   = self._goal

        #  counts number of cells pushed
        self._num_cells_pushed = 0
        # counts the path length
        self._path_length = 0

        if debug:
            # for example from slides
            blocked_cells = [(1,0),(1,3),(2,1),(2,4),(3,2),(5,1),(5,3),(5,4)]
            for pos in blocked_cells:
                p = Position(*pos)  # expand the pos tuple & pass to Position
                self._grid[p.row][p.col]._contents = Contents.BLOCKED
        else:
            options = [cell for row in self._grid for cell in row] #1D version of list
            options.remove(self._start)
            options.remove(self._goal)
            how_many = round((num_cols * num_rows -2) * proportion_blocked)
            blocked = random.sample(options, k = how_many)
            for cell in blocked:
                cell._contents = Contents.BLOCKED

    def showPath(self, goal: Cell) -> None:
        path = []
        cell = goal
        while cell._parent is not None:
            path.append(cell)
            self._path_length += 1
            cell = cell._parent
        path.append(cell)
        self._path_length += 1
        assert(cell == self._start)

        path.reverse() #reverse path list

        for cell in path:
            if cell not in [self._start, self._goal]:
                cell.markOnPath()

        print(self)

    def getStart(self) -> Cell: return self._start
    def getGoal(self) -> Cell: return self._goal
    def getSearchLocations(self, cell: Cell) -> list[Cell]:
        '''
        Gets the cells that need to be searched, which are cells that are not blocked and are in bounds of the maze
        Parameters:
            cell: a cell in the maze
        Returns:
            search_locations: a list of Cells which correspond to the desired search locations
        '''
        row =  cell.getPosition().row 
        col = cell.getPosition().col
        search_locations = []
        if row - 1 >= 0 and self._grid[row - 1][col].isBlocked() == False: # North
            search_locations.append(self._grid[row - 1][col])
        if row + 1 < self._num_rows and self._grid[row + 1][col].isBlocked() == False : # South
            search_locations.append(self._grid[row + 1][col])
        if col - 1 >= 0 and self._grid[row][col -1].isBlocked() == False: # West
            search_locations.append(self._grid[row][col - 1])
        if col + 1 < self._num_cols and self._grid[row][col +1].isBlocked() == False: # East
            search_locations.append(self._grid[row][col + 1])

        return search_locations


    def dfs(self) -> Cell | None:
        '''
        Solves a maze through depth first search
        Returns:
            current: returns the cell of the goal
        '''
        stack_dfs = Stack()
        current = self._start
        been_searched = []

        stack_dfs.push(current)
        self._num_cells_pushed += 1
        been_searched.append(current)

        while stack_dfs.is_empty() != True:
            current = stack_dfs.pop()
            if current.isGoal():
                print(f"Cells pushed DFS: {self._num_cells_pushed}")  
                return current
            search_locations = self.getSearchLocations(current)
            for cell in search_locations:
                if cell not in been_searched:
                    cell._parent = current
                    been_searched.append(cell)
                    stack_dfs.push(cell)
                    self._num_cells_pushed += 1

        return None


    def bfs(self) -> Cell | None:
        '''
        Solves a maze through breadth first search
        Returns:
            current: returns the cell of the goal
        '''
        queue_bfs = Queue()
        current = self._start
        been_searched = []

        queue_bfs.push(current)
        self._num_cells_pushed += 1
        been_searched.append(current)

        while queue_bfs.is_empty() != True:
            current = queue_bfs.pop()
            #print(current.getPosition())
            if current.isGoal():        
                print(f"Cells pushed BFS: {self._num_cells_pushed}")
                return current
            search_locations = self.getSearchLocations(current)
            for cell in search_locations:
                if cell not in been_searched:
                    cell._parent = current
                    been_searched.append(cell)
                    queue_bfs.push(cell)
                    self._num_cells_pushed += 1

        return None
    


    def a_star(self) -> Cell | None:
        '''
        solves a maze via a* method, returning the finishing cell
        Returns:
            n: the cell of the goal
        '''
        astar_queue = PriorityQueue()
        been_searched = dict()
        n = self._start
       # n._parent = None  
        end = self._goal
        g_n = 0.0
        h_n = abs(n.getPosition().row - end.getPosition().row) + abs(n.getPosition().col - end.getPosition().col)
        f_n = h_n + g_n
        astar_queue.insert(f_n, n)
        self._num_cells_pushed += 1
        been_searched[n.getPosition()] = g_n 
        while len(astar_queue) != 0:

            e = astar_queue.remove_min()
            n = e.value
            if n == self._goal:
                print(f"Cells pushed A*: {self._num_cells_pushed}")
                return n
            for m in self.getSearchLocations(n):
                g_m = been_searched[n.getPosition()] + 1
                if m.getPosition() not in been_searched or g_m < been_searched[m.getPosition()]:
                    m.setParent(n)  
                    been_searched[m.getPosition()] = g_m
                    h_m = abs(m.getPosition().row - end.getPosition().row) + abs(m.getPosition().col - end.getPosition().col)
                    f_m = g_m + h_m
                    astar_queue.insert(f_m, m)
                    self._num_cells_pushed += 1
        
        return None


    def __str__(self) -> str:
        ''' creates a str version of the Maze, showing contents, with cells
            delimited by vertical pipes
        Returns:
            a str representation of the Maze
        '''
        maze_str = ""
        for row in self._grid:  # row : list[Cell]
            maze_str += "|" + "|".join([cell._contents for cell in row]) + "|\n"
        return maze_str[:-1]  # remove the final \n


###########################################################
def main() -> None:

    random.seed(1234)
    m = Maze(10, 10, Position(0,0), Position(9,9), 0.2,False)
    #print(m)
    m.showPath(m.dfs())

    cell_a = Cell(2,2, Contents.EMPTY)
    cell_b = Cell(5,4, Contents.EMPTY)
    m.getSearchLocations(cell_a)
    m.getSearchLocations(cell_b)

    random.seed(54321)
    m = Maze(10, 10, Position(0,0), Position(9,9), 0.2,False)
    m.showPath(m.bfs())

    random.seed(1357)
    m = Maze(10, 10, Position(0,0), Position(9,9), 0.2,False)
    m.showPath(m.a_star())

    random.seed(3021)
    m = Maze(25, 25, Position(0,0), Position(21,21), 0.2, False)
    m.showPath(m.dfs())

    random.seed(3944)
    m = Maze(25, 25, Position(0,0), Position(20,20), 0.2, False)
    m.showPath(m.bfs())

    random.seed(2000)
    m = Maze(25, 25, Position(0,0), Position(16,24), 0.2, False)
    m.showPath(m.a_star())

    random.seed(74983)
    m = Maze(50, 50, Position(0,0), Position(40,40), 0.2, False)
    m.showPath(m.dfs())

    random.seed(230)
    m = Maze(50, 50, Position(0,0), Position(30,30), 0.2, False)
    m.showPath(m.bfs())

    random.seed(289)
    m = Maze(50, 50, Position(0,0), Position(49,49), 0.2, False)
    m.showPath(m.a_star())


if __name__ == "__main__":
    main()
