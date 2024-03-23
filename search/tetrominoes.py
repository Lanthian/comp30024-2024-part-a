# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from core import Coord, Direction
# todo - change to .core for use in program.py perhaps?

def tetrominoes(
        c: Coord, 
        avoid_coords: list[Coord]=[]
) -> list[list[Coord]]:
    """Takes a Coord c and generates a list of Place actions of all unique 4 
    tiled "tetrominoes" that include this coordinate, relating to the board size
    defined in core.py. List should be of length 76 be default.
    Returns None
    (z*2 + s*2 + i*2 + t*4 + o*1 + j*4 + l*4) * 4 = 19 * 4 = 76

    Parameters:
        `c`: a Coord on which place actions should be centred around (including)
        `avoid_coords`: list of Coords which should not be included in any place 
            actions and will limit the size of the output - empty by default
    
    Returns:
        A list of lists of Coords (list of place actions) or in the case that 
            starting coordinate is present in `avoid_coord` list, and empty list
    """
    # todo- insert into sorted lists rather than inserting and sorting each time
    t = []

    # Check if no possible tetrominos to generate from starting coord
    if c in avoid_coords: return t

    in_progress = [[c]]
    seen = []               # todo - cannot use set as lists are unhashable...
    # Work through a queue of semi-assembled tetrominoes to build whole set
    while len(in_progress) > 0:
        curr = in_progress.pop(0)
        curr.sort()
        # Skip node if already seen
        if curr in seen:
            continue

        # otherwise, add to seen set and check if valid
        else:
            seen.append(curr)
            if len(curr) == 4:
                # valid tetromino
                t.append(curr)
                continue
        
        # Loop through each direction for each piece, attaching a new block
        for coord in curr:
            for dir in [d.value for d in Direction]:
                new = Coord.__add__(coord, dir)
                # Avoid duplicating existing and including disallowed coords
                if (new in curr) or (new in avoid_coords): continue
                in_progress.append(curr + [new])

    return t


# possible = tetrominoes(Coord(0,0), [Coord(1,0)])
possible = tetrominoes(Coord(0,0), [Coord(0,0)])
possible.sort()
for p in possible:
    print(p.__str__())
print(len(possible))
