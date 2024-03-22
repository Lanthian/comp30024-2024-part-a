# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

# todo/temp - Terminal input
# temp - python -m search < test-vis1.csv

from .core import PlayerColor, Coord, PlaceAction, BOARD_N
from .utils import render_board


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
    print(render_board(board, target, ansi=False))
    

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...


    # -- Start search by finding valid red tokens to build off of --
    starting_srcs = []              # [(Coord, int)]
    HEURISTIC_INDEX = 1

    for (coord, color) in board.items():
        # Generate possible starting locations, inserted via target heuristic 
        if color == PlayerColor.RED:
            # todo - an intelligent insert making use of generating a sorted 
            # list would be better here. For now, append + sort will do...
            starting_srcs.append((coord, heu2(board, coord,target)))
            starting_srcs.sort(key=lambda x : x[HEURISTIC_INDEX])
    


    # test prints
    print(starting_srcs)                        # temp
    print(free_cells(board, target, "r"))       # temp

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


    # # temp : print out board state changes
    for i in temp:
        board = make_place(board, i, PlayerColor.RED)
        print(render_board(board, target, ansi=False))

    # print (valid_place(board,temp[0]))                        # temp
    # print (make_place(board, temp[0], PlayerColor.RED))       # temp

    return temp


def distance_from_axes(source: Coord, target: Coord) -> int:
    """Heuristic: Finds the minimum distance from a source coord to either of a 
    target coord's axes. Returns this integer.
    """
    # todo - should subtract(?) summed additional measure that considers how 
    # many filled cells the more important row or column already has
    return min(
        abs(target.c - source.c), 
        abs(target.r - source.r)
    )


# todo - temp naming and idea 
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
    xy = ceildiv(abs(target.c-source.c) + free_cells(board,target,"c"), P_SIZE)
    yx = ceildiv(abs(target.r-source.r) + free_cells(board,target,"r"), P_SIZE)
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

    # Subtract occupied cells to find free count
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

    # todo - Verify this is the only invalid way a piece can be placed
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
