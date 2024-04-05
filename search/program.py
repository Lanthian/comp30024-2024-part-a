"""program.py: Provides an A* search algorithm for __main__.py's Single Player
Tetress game implementation

Usage: Used alongside supplied __main__.py file and other files in search module 
    python -m search < [game csv file]
    e.g.    python -m search < test-vis1.csv
            python -m search < tung-csvs/1.csv"""

__author__ = "Liam Anthian, and Anthony Hill"
__credits__ = ["Liam Anthian", "Anthony Hill"] 

# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

# === Imports ===
from dataclasses import dataclass
from functools import total_ordering

from .core import PlayerColor, Coord, PlaceAction, BOARD_N
from .tetrominoes import tetrominoes_plus
from .prioritydict import PriorityDict


@dataclass(frozen=True, slots=True)
@total_ordering
class State():
    """
    A dataclass representing a current "state" of the game, where `board` stores
    the game board as of current, `path` the list of PlaceActions to get to this
    board, `g` the cost of moves to get here and `h` a heuristic prediction of 
    best case moves to get to end goal.
    """
    board: dict[Coord, PlayerColor]
    path: list[PlaceAction]
    g: int                      # current actions count, equivalent to len(path)
    h: int                      # estimated optimal remaining actions

    @property
    def cost(self) -> int:
        return self.g+self.h
    
    def __eq__(self, other):
        return (self.board == other.board and
                self.cost == other.cost)
                # path doesn't matter if cost is equal
    
    def __lt__(self, other):
        return self.cost < other.cost


def search(
    board: dict[Coord, PlayerColor], 
    target: Coord
) -> list[PlaceAction] | None:
    """
    Searches through a tree of possible board states from potential red moves to 
    reach an OPTIMAL end state where the target coord provided has been removed.
    Returns a path of core.PlaceActions to get to this state. Implements an A*
    algorithm, using heuristics also defined in this file.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `target`: the target BLUE coordinate to remove from the board.
    
    Returns:
        A list of "place actions" as PlaceAction instances, or `None` if no
        solution is possible.
    """
    # Prepare board (remove already filled axes)
    clear_axes(board)

    """
    Plan:
    Using a custom priority dictionary (PD) of LIFO queues to store states, add 
    initial state as a node, then:
    1) Dequeue smallest node - return path if goal met and end search
    2) Generate children states - each possible PlaceAction from each possible
        red token currently on board.
    3) Insert nodes into PD using heuristic + step cost as evaluation functions
    Repeat steps 1-3 until a goal node is found, or PD exhausted (return None)    
    """
    
    pd = PriorityDict()
    # Seen states stored in hashable set rather than list to improve check time
    seen = set() 

    s = State(board, [], 0, heu_board(board, target))
    pd.put(s.cost, s)
    seen.add(flatten_board(board))

    # Work through states for as long as elements exist and goal not met
    while not pd.empty():
        curr = pd.get()

        # Check goal & return if done - guaranteed least/equal least cost path 
        if target not in curr.board:
            # (A) best solution found!
            return curr.path

        # Generate next moves from this step and enqueue them
        for move in possible_moves(curr.board, PlayerColor.RED):
            # Copy board as make_place() acts in place
            b2 = make_place(curr.board.copy(), move, PlayerColor.RED)

            # Skip duplciate boards
            flat_b2 = flatten_board(b2)
            if flat_b2 in seen: continue

            # Enqueue if unseen
            s = State(b2, curr.path + [move], curr.g + 1, heu_board(b2, target))
            pd.put(s.cost, s)
            seen.add(flat_b2)
        
    # If here, no solutions have been found in all possible board expansions
    return None


def possible_moves(board: dict[Coord, PlayerColor], 
                   player: PlayerColor) -> list[PlaceAction]:
    """
    Takes a game `board` and a `player` defined by their PlayerColor and returns 
    all possible next moves for said player in the form of a list of 
    PlaceActions.
    """
    moves = set()
    for (coord, color) in board.items():
        if color == player:
            # duplicate moves generated and ignored here (possible improvement)
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
        An admissible heuristic int equivalent to optimal least possible moves 
        needed to clear target coordinate.
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
        target: Coord) -> int:
    """A heuristic - finds the minimum piece cost from a source coord to either 
    of a target coord's axes PLUS the number of free cells to fill. 
    Piece cost/standardisation refers to perfectly placing a piece towards
    filling cells and approaching axis (dividing tile measure by 4 for number of
    tiles in tetromino and rounding up).

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
    # Find which axis is iterated over
    match axis:
        case "x" | "r" | "row":
            axis_iterator = lambda t: Coord(target.r, t)
        case "y" | "c" | "col":
            axis_iterator = lambda t: Coord(t, target.c)
        case _:
            print("ERROR free_cells: invalid axis specified.")
            return None

    free = BOARD_N
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
    Acts in place - clears filled rows and columns on a game `board`. Only 
    checks for clearable axes in the row and column ranges supplied, to make 
    targetted clearing more efficient. Checks all rows and columns by default. 
    Returns nothing (None).
    """
    IRRELEVANT = 0

    # Find all cells that exist in checked filled rows/cols
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
        # Add coordinate axes to tracking sets then place token
        placed_r.add(coord.r)
        placed_c.add(coord.c)
        board[coord] = color

    # If necessary, clear now full rows and columns
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
    DELIM = "."

    coord_colors = [(k.__str__() + v.__str__()) for (k,v) in board.items()]
    # Sort to ensure all dictionaries with the same values are equivalent
    coord_colors.sort()
    return DELIM.join(coord_colors)


def ceildiv(a, b):
    """Helper math function to perform ceiling division.
    Inspired by user @dlitz https://stackoverflow.com/users/253367/dlitz
        in post https://stackoverflow.com/a/17511341
    """
    return -(a // -b)
