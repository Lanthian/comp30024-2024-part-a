# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from .core import PlayerColor, Coord, PlaceAction
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
            starting_srcs.append((coord, distance_from_axes(coord,target)))
            starting_srcs.sort(key=lambda x : x[HEURISTIC_INDEX])
    
    # test print
    print(starting_srcs)        # temp

    # maybe find open air neighbours of these points instead...

    # next, need to try placing all possible tetrominos down, centred from this 
    # point, and measure which move is best via similar heuristic
    # then, repeat - finding open air spots next to these

    # from this note here, I'm discovering that the process of queuing and 
    # selecting next moves is really quite complex, or elusive to me right now 
    # at the very least


    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return [
        PlaceAction(Coord(2, 5), Coord(2, 6), Coord(3, 6), Coord(3, 7)),
        PlaceAction(Coord(1, 8), Coord(2, 8), Coord(3, 8), Coord(4, 8)),
        PlaceAction(Coord(5, 8), Coord(6, 8), Coord(7, 8), Coord(8, 8)),
    ]

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
