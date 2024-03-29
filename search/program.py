# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

# todo/temp - Terminal input
# python -m search < test-vis1.csv

from .core import PlayerColor, Coord, PlaceAction, BOARD_N
from .utils import render_board
from queue import PriorityQueue
from .tetrominoes import *
from dataclasses import dataclass
from functools import total_ordering


# @dataclass(frozen=True)
@dataclass(frozen=True, slots=True)
@total_ordering
class State():
    """
    A dataclass representing a current "state" of the game, where `board` stores
    the game board as of current, `path` the list of PlaceActions to get to this
    board, `tile` the current cell of interest to build from, `g` the cost of
    moves to get here, `h` a heuristic prediction of best case moves to get to
    end goal.
    """
    board: dict[Coord, PlayerColor]
    path: list[PlaceAction]
    tile: Coord
    g: int                          # current actions count, todo - maybe redundant with len(path)?
    h: float                          # estimated remaining actions; cost to goal

    @property
    def cost(self) -> float:
        return self.g+self.h
    
    def __eq__(self, other):
        return (self.board == other.board and
                self.tile == other.tile and
                self.g == other.g and
                self.h == other.h)
                # path doesn't matter if cost is equal
    def __lt__(self, other):
        return self.cost < other.cost
    
    """ in the case of creating a hash function and using state in a set.
    def __hash__(self):
        # Hash is a combination of board, tile, g, and h
        return hash((self.board, self.tile, self.g, self.h))
    """
    

def search(
    board: dict[Coord, PlayerColor], 
    target: Coord
) -> list[PlaceAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `target`: the target BLUE coordinate to remove from the board.
    
    Returns:
        A list of "place actions" as PlaceAction instances, or `None` if no
        solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, target, ansi=True))
    print("===============================================================")
    

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...
    
    #28/04/2024. Sorry haven't done much work, will get on it especially over break - Anthony
    """
    Plan:
    scan all red coords and simultaneously calculate heuristic manhattan value.
    Generate state and store state node.
    Skip pre-existing states, removes possiblity of infinite loop of generating
    Insert into priority queue with values

    For each consequent generation:
    1) Dequeue node
    2) generate expanded nodes and insert using heuristic + step cost as evaluation functions
    3) Insert. 
    4) Repeatedly scan board state to identify if target coord is gone, if so return with this node state.
    5) Function to get path of this node state and submit these place actions

    Talked to people in my tutorial and main issue is an admissable heuristic, especially with the possibility of needing
    to clear multiple axes first. Manhatten distance won't cut it.
    WILL WORK ON IT BEGINNING TOMORROW AND GRIND. Want to get this done before Monday
    """
    
    ### attempt 2!
    # ========================================================================= WIP
    
    pq = PriorityQueue()
    seen = []
    for (coord, color) in board.items():
        if color == PlayerColor.RED:
            print(f"bb + {coord}")
            # Find heuristic cost of coord for state
            h = heu3(board, coord, target)
            #h = heu2(board, coord, target)
            s = State(board, [], coord, 0, h)
            # Skip preexisting states
            if s in seen: 
                print("duplicate found")
                continue
            # States comparable via total_ordering so can be inserted directly
            pq.put(s)
            seen.append(s)
    
    i = 0
    # Work through queue for as long as elements exist and goal not met
    while not pq.empty():
        curr = pq.get()
        print(f"Lap: {i}")
        i += 1
        # print(render_board(curr.board, target, True))
        print(f"Path: {curr.path}")

        # Check goal & return if done - guaranteed least/equal least cost path 
        if check_win(target, curr.board): 
            # print(render_board(board,target,True))      # todo -temp
            return curr.path

        # Generate next moves from this step and enqueue them
        next_moves = tetrominoes_plus(curr.tile, curr.board)
        for move in next_moves:
            # If move is valid - enqueue following states
            if valid_place(curr.board, move):
                next_board = make_place(curr.board.copy(), move, PlayerColor.RED)

                # Queue a state for each new
                for (coord, color) in next_board.items():
                    if color == PlayerColor.RED:
                        h = heu3(next_board, coord, target)
                        #h = heu2(next_board, coord, target)
                        s = State(next_board, curr.path + [move], coord, curr.g+1, h)
                        if s in seen: continue
                        pq.put(s)
                        seen.append(s)
        

        print(curr.cost)
        print()

        #todo - SUPER INEFFICIENT, but basic idea layed out
    
    # ========================================================================= WIP
    """
    successors = PriorityQueue() #initilaise priority queue for nodes to be explored, https://www.educative.io/answers/what-is-the-python-priority-queue for how PQ works
    failed_Set = set()
    for (coord, color) in board.items():
        if color == PlayerColor.RED:
            
            f_n = heu2(board, coord, target)  # g(n) is 0 for starting nodes
            successors.put((f_n, coord)) #need to adapt this to add board states rather than coords

    while not successors.empty() and target in board: #after every node placement checks if target has not been deleted from board yet
        b
    """


    # -- Start search by finding valid red tokens to build off of --
    """
    starting_srcs = []              # [(Coord, int)]
    HEURISTIC_INDEX = 1

    for (coord, color) in board.items():
        # Generate possible starting locations, inserted via target heuristic 
        if color == PlayerColor.RED:
            # todo - an intelligent insert making use of generating a sorted 
            # list would be better here. For now, append + sort will do...
            starting_srcs.append((coord, heu2(board, coord,target)))
            starting_srcs.sort(key=lambda x : x[HEURISTIC_INDEX])
    """


    # test prints
    # print(starting_srcs)                        # temp
    # print(F"Free cells - {free_cells(board, target, "r")}")       # temp

    # maybe find open air neighbours of these points instead...

    # next, need to try placing all possible tetrominoes down, centred from this 
    # point, and measure which move is best via similar heuristic
    # then, repeat - finding open air spots next to these

    # from this note here, I'm discovering that the process of queuing and 
    # selecting next moves is really quite complex, or elusive to me right now 
    # at the very least


    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.

    temp = [
        PlaceAction(Coord(2, 5), Coord(2, 6), Coord(3, 6), Coord(3, 7)),
        PlaceAction(Coord(1, 8), Coord(2, 8), Coord(3, 8), Coord(4, 8)),
        PlaceAction(Coord(5, 8), Coord(6, 8), Coord(7, 8), Coord(8, 8)),
    ]


    # temp : print out board state changes
    # for i in temp:
    #     board = make_place(board, i, PlayerColor.RED)
    #     print(render_board(board, target, ansi=True))

    # print (valid_place(board,temp[0]))                        # temp
    # print (make_place(board, temp[0], PlayerColor.RED))       # temp

    return temp


def distance_from_axes(source: Coord, target: Coord) -> int:
    """Heuristic: Finds the minimum distance from a source coord to either of a 
    target coord's axes. Returns this integer.
    """
    row_distance = abs_distance(target.c,source.c)
    col_distance = abs_distance(target.r,source.r)
    
    return min(row_distance, col_distance)


# need a g(n) heuristic which will be step cost / 4 to generalise it to heu2 value? (the cost from the start node to n, initially 0 for starting nodes) 

# heuristic 3 h(n)
def heu3(board: dict[Coord, PlayerColor], 
        source: Coord, 
        target: Coord) -> float:
    """
    Calculate the heuristic distance from start to goal on a grid that wraps around
    at the edges, considering pieces.

    :param start: A tuple (x, y) representing the start coordinate.
    :param goal: A tuple (x, y) representing the goal coordinate.
    :return: The estimated number of pieces needed to reach the goal, rounded to 1 decimal place

    Chose not to include obstacles to not overestimate cost, and increase complexity/runtime by exploring unecessary pathways
    """
    # Manhattan distances
    dx = abs(target.c - source.c)
    dy = abs(target.r - source.r)

    # Wraparound distances
    dx_wrap = BOARD_N - dx
    dy_wrap = BOARD_N - dy

    min_dx = min(dx, dx_wrap)
    min_dy = min(dy, dy_wrap)

    total_distance = min_dx + min_dy

    # Adjust by the maximum coverage of a Tetris piece
    estimated_pieces = total_distance / 4

    # free 
    free_in_row = free_cells(board, target, "row")
    free_in_col = free_cells(board, target, "col")
    
    free_path_weight = (min(free_in_row, free_in_col))/BOARD_N 
    
    return estimated_pieces + free_path_weight

    # Ceiling to ensure at least one piece is needed if there's any distance
    return max(1, round(estimated_pieces, 1))


# heuristic 2 in A* fulfills the h(n) (the heuristic estimate from n to the target)
def heu2(board: dict[Coord, PlayerColor], 
        source: Coord, 
        target: Coord) -> int:
    """A heuristic - finds the minimum piece cost from a source coord to either 
    of a target coord's axes PLUS the number of free cells to fill. 
    Piece cost/standardisation refers to perfectly placing a piece towards
    filling cells and approaching axis (dividing tile measure by 4 for number of
    tiles in tetromino).

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `source`: a starting RED coordinate to build off of on the board.
        `target`: the target BLUE coordinate to remove from the board.
    
    Returns:
        An admissible heuristic integer of optimal least possible moves to clear
        target coordinate.
    """
    P_SIZE = 4                                  # 4 tiles in a tetromino
    # In terms of reaching a filled axis:
    # xy = x pieces then y pieces, yx = y pieces then x pieces
    xy = ceildiv(abs_distance(target.c,source.c) + free_cells(board,target,"c"), P_SIZE)
    yx = ceildiv(abs_distance(target.r,source.r) + free_cells(board,target,"r"), P_SIZE)
    return min(xy, yx)


def free_cells(
    board: dict[Coord, PlayerColor], 
    target: Coord,
    axis: str
) -> int | None:
    """Takes a dictionary of board tokens `board`, a Coord `target`, and an 
    `axis` flag to determine which board axis is counted over. Utilises the fact 
    that the board is a sparse representation of tokens present by checking if 
    dict contains each axis coordinate.

    Returns either the count of free cells in target axis, or None if incorrect 
    use / error. 
    """
    free = BOARD_N
    
    # Find which axis is iterated over
    match axis:
        case "x" | "r" | "row":
            axis_iterator = lambda x: Coord(target.r, x)
        case "y" | "c" | "col":
            axis_iterator = lambda x: Coord(x, target.c)
        case _:
            print("ERROR free_cells: invalid axis specified.")
            return None

    # Subtract occupied cells to find free cdount
    for i in range(BOARD_N):
        if axis_iterator(i) in board:
            free -= 1

    return free


def valid_place(board: dict[Coord, PlayerColor], place: PlaceAction) -> int:
    """
    Checks is a tetromino placement is valid for a given board state. Assumes
    tetromino coords themselves are in a valid shape.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `place`: a `PlaceAction`instance of four coordinates of a tetromino
            piece to place onto the board.
    
    Returns:
        A binary int for whether or not given PlaceAction can be reasonably 
        performed on given board. Returns 1 if valid, 0 if not.
    """
    for coord in place.coords:
        if coord in board:
            return 0
    return 1


def make_place(
    board: dict[Coord, PlayerColor], 
    place: PlaceAction, 
    color: PlayerColor
) -> dict[Coord, PlayerColor]:
    """
    Assumes the place actions have been validated first, otherwise it can write
    over the top of existing cells. Places tetrominoes on a board, clearing rows
    if filled. 
    Note: can only clear rows/cols currently being placed in - previously filled
    axes will remain full.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `place`: a `PlaceAction`instance of four coordinates of a tetromino
            piece to place onto the board.
        `color`: the core.py `PlayerColor` of the tetromino piece being played
    
    Returns:
        An altered board containing the changes of adding given tetromino piece
        and clearing now full axes.
    """
    placed_r = set()
    placed_c = set()

    for coord in place.coords:
        # Add coordinate axes to tracking sets and place token
        placed_r.add(coord.r)
        placed_c.add(coord.c)
        board[coord] = color


    # - If necessary, clear now full rows and columns -
    to_clear = set()
    IRRELEVANT = 0

    # Find all cells that need to be dropped (existing in full rows / cols)
    for r in placed_r:
        if free_cells(board, Coord(r,IRRELEVANT), "r") == 0:
            [to_clear.add(Coord(r,i)) for i in range(BOARD_N)]
    for c in placed_c:
        if free_cells(board, Coord(IRRELEVANT,c), "c") == 0:
            [to_clear.add(Coord(i,c)) for i in range(BOARD_N)]

    # Drop these cells from board
    for tile in to_clear:
        board.pop(tile, 0)
        
    return board


def ceildiv(a, b):
    """Helper math function to perform ceiling division.
    Inspired by user @dlitz https://stackoverflow.com/users/253367/dlitz
        in post https://stackoverflow.com/a/17511341
    """
    return -(a // -b)


def abs_distance(a, b):
    """Takes in two numbers and returns the minimum absolute distance between 
    them, considering a scale of BOARD_N that loops infinitely.
    """
    absolute = abs(a-b)
    return min(absolute, BOARD_N-absolute)


def check_win(target: Coord, board: dict[Coord,PlayerColor]) -> bool:
    """Function added to make checking goal state more readable. Returns true if
    goal has been reached, false if not.
    """
    return target not in board