# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from core import Coord, Direction
# todo - change to .core for use in program.py perhaps?

def tetrominoes(c: Coord) -> list[Coord]:
    t = []

    in_progress = [[c]]
    seen = []               # todo - cannot use set as lists are unhashable...
    # Work through a queue of semi-assembled tetrominoes to build whole set
    while len(in_progress) > 0:
        curr = in_progress.pop(0)
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
                in_progress.append(curr + [Coord.__add__(coord, dir)])

    return t


possible = tetrominoes(Coord(0,0))
print(len(possible))
#312 possible tetrominoes placeable around (0,0)? Seems unlikely 
# - investigate this number
