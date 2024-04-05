# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

# todo/temp - Terminal input
# python -m search < test-vis1.csv
# python -m search < tung-csvs/1.csv

# === Imports ===
from .core import PlayerColor, Coord, PlaceAction, BOARD_N
from .utils import render_board
from .tetrominoes import tetrominoes_plus
from .prioritydict import PriorityDict
from dataclasses import dataclass
from functools import total_ordering

# === Constants ===
DEBUG_PRINT = 2


@dataclass(frozen=True, slots=True)
@total_ordering
class State():
    """
    A dataclass representing a current "state" of the game, where `board` stores
    the game board as of current, `path` the list of PlaceActions to get to this
    board, `g` the cost of moves to get here, `h` a heuristic prediction of best 
    case moves to get to end goal, and `lifo_id` a counter to measure how old a
    state is in comparison with other equal cost states.
    """
    board: dict[Coord, PlayerColor]
    path: list[PlaceAction]
    g: int                      # current actions count, equivalent to len(path)
    h: float                    # estimated optimal remaining actions
    lifo_id: int

    @property
    def cost(self) -> float:
        return self.g+self.h
    
    def __eq__(self, other):
        return (self.board == other.board and
                self.cost == other.cost and
                self.lifo_id == other.lifo_id)
                # path doesn't matter if cost is equal
    
    def __lt__(self, other):
        # For equal costs, sort LIFO instead of default priority queue FIFO
        if self.cost == other.cost:
            return self.lifo_id < other.lifo_id 
        return self.cost < other.cost


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
    # Prepare board
    clear_axes(board)

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    if DEBUG_PRINT > 3: print(render_board(board, target, ansi=True))
    if DEBUG_PRINT > 3: print("===================================================")
    """
    Plan:
    Using a custom priority dictionary (PD) of LIFO queues to store states, add 
    initial state as a node, then:
    1) Dequeue smallest node - return path if goal met and end search
    2) Generate children states - each possible PlaceAction from each possible
        red token currently on board.
    3) Insert nodes into PD using heuristic + step cost as evaluation functions
    Repeat steps 1-3 until a goal node is found, or exhausted (return None)    
    """
    
    pd = PriorityDict()
    
    # Seen states stored in hashable set rather than list to improve check time
    seen = set() 
    count = 0
    h_min = float(15)

    h = heu_board(board, target)

    h_min = min(h_min, h) #new

    s = State(board, [], 0, h, count)
    count -= 1
    pd.put(s.cost, s)
    seen.add(flatten_board(board))

    # Work through states for as long as elements exist and goal not met
    if DEBUG_PRINT > 3: i = 0
    while not pd.empty():
        curr = pd.get()
        if DEBUG_PRINT > 3: 
            print(f"=== Lap: {i}, Queue Size: {pd.size} ===")
            i += 1
            print(render_board(curr.board, target, True))
            print(f"Path length: {curr.g}, Heu: {curr.h}")

        # Check goal & return if done - guaranteed least/equal least cost path 
        if target not in curr.board:
            # (A) best solution found!
            if DEBUG_PRINT > 1:
                print(render_board(board,target,True))
                for i in curr.path:
                    print(render_board(make_place(board,i,PlayerColor.RED),target,True))
            return curr.path

        # Generate next moves from this step and enqueue them
        if DEBUG_PRINT > 3: print("//Generating...")
        moves = possible_moves(curr.board, PlayerColor.RED)
        if DEBUG_PRINT > 3: print(f"//Inserting {len(moves)} moves")
        for move in moves:
            new_board = make_place(curr.board.copy(), move, PlayerColor.RED)
            # Skip duplciate boards
            if flatten_board(new_board) in seen: continue
            
            h = heu_board(new_board, target) #new
            if h < h_min:
                h_min = h
            if h <= (1+h_min) * 2: #hmin can become 0 so need +1 to counteract this
                s = State(new_board, curr.path + [move], curr.g+1, h, count)
                count -= 1
                pd.put(s.cost, s)
                seen.add(flatten_board(new_board))
            else:
                continue
            
            
                
            # s = State(new_board, curr.path + [move], curr.g+1, heu_board(new_board, target), count)
            # count -= 1
            # pd.put(s)
            # seen.add(flatten_board(new_board))
        
    # If here - no solutions found in all possible board expansions
    return None


def possible_moves(board: dict[Coord, PlayerColor], 
                   player: PlayerColor) -> list[PlaceAction]:
    """Takes a game `board` and a `player` defined by their PlayerColor and
      returns all possible next moves for said player in the form of a list of 
      PlaceActions.
    """
    moves = set()
    for (coord, color) in board.items():
        if color == player:
            # duplicate moves generated and ignored here - todo improve
            moves.update(tetrominoes_plus(coord, set(board.keys())))

    return list(moves)


def heu_board(board: dict[Coord, PlayerColor], target: Coord) -> float:
    """A heuristic - finds the distance (in tiles, not pieces) from any possible 
    source coord to either of a target coord's axes PLUS the number of free 
    cells to fill. 

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `target`: the target BLUE coordinate to remove from the board.
    
    Returns:
        An admissible heuristic float that can be rounded up to optimal least 
        possible moves to clear target coordinate.
    """
    # No moves necessary if target cleared
    if target not in board: return 0

    best = 15   # Worst possible h value
    # Iterate through red tiles in board
    for (tile, color) in board.items():
        if color == PlayerColor.RED:
            # Update board rating if new tile has better heuristic
            t = heuristic(board, tile, target)
            if t < best: best = t
    return best


def heuristic(
        board: dict[Coord, PlayerColor], 
        source: Coord, 
        target: Coord) -> float:
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
    # No moves necessary if target cleared
    if target not in board: return 0

    P_SIZE = 4                                  # 4 tiles in a tetromino
    # In terms of reaching a filled axis:
    # xy = x pieces then y pieces, yx = y pieces then x pieces
    # -1 done to drop off overlap between two measures
    xy = abs_distance(target.c,source.c) + free_cells(board,target,"c") - 1
    yx = abs_distance(target.r,source.r) + free_cells(board,target,"r") - 1
    return ceildiv((min(xy, yx)), P_SIZE)


def free_cells(
    board: dict[Coord, PlayerColor], 
    target: Coord,
    axis: str
) -> int | None:
    """Takes a dictionary of board tokens `board`, a Coord `target`, and an 
    `axis` flag to determine which board axis is counted over. Utilises the fact 
    that the board is a sparse representation of tokens present by checking if 
    dict contains each axis coordinate.

    Returns:
        Either the count of free cells in target axis, or None if invalid `axis`
        flag supplied.
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

    # Subtract occupied cells to find free count
    for i in range(BOARD_N):
        if axis_iterator(i) in board:
            free -= 1

    return free


def clear_axes(
    board: dict[Coord, PlayerColor],
    row_range: list[int]=range(BOARD_N),
    col_range: list[int]=range(BOARD_N)
) -> None:
    """
    In place - clears filled rows and columns on a game `board`. Only checks for
    clearable axes in the row and column ranges supplied, to make targetted 
    clearing more efficient. Checks all rows and columns by default. Returns 
    nothing.
    """
    IRRELEVANT = 0

    to_clear = set()
    for r in row_range:
        if free_cells(board, Coord(r,IRRELEVANT), "r") == 0:
            [to_clear.add(Coord(r,i)) for i in range(BOARD_N)]
    for c in col_range:
        if free_cells(board, Coord(IRRELEVANT,c), "c") == 0:
            [to_clear.add(Coord(i,c)) for i in range(BOARD_N)]

    # Drop these cells from board
    for tile in to_clear:
        board.pop(tile, 0)

    return None
    

def make_place(
    board: dict[Coord, PlayerColor], 
    place: PlaceAction, 
    color: PlayerColor,
) -> dict[Coord, PlayerColor]:
    """
    Assumes the place actions have been validated first, otherwise it can write
    over the top of existing cells. Places tetrominoes on a board, clearing rows
    / cols if filled. Acts in place - use with .copy() to generate new boards.

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
    clear_axes(board, list(placed_r), list(placed_c))
        
    return board


def abs_distance(a, b):
    """
    Takes in two numbers and returns the minimum absolute distance between 
    them, considering a scale of BOARD_N that loops infinitely.
    """
    absolute = abs(a-b)
    return min(absolute, BOARD_N-absolute)


def flatten_board(board: dict[Coord, PlayerColor]) -> str:
    """
    Takes a game board state and converts it into (and returns) a string
    representation, using .__str__() methods of Coord and PlayerColor.
    """
    temp = [(k.__str__() + v.__str__()) for (k,v) in board.items()]
    # Sort to ensure all dictionaries with the same values are equivalent
    temp.sort()
    return ".".join(temp)


def ceildiv(a, b):
    """Helper math function to perform ceiling division.
    Inspired by user @dlitz https://stackoverflow.com/users/253367/dlitz
        in post https://stackoverflow.com/a/17511341
    """
    return -(a // -b)

