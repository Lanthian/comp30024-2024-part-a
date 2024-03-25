# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from core import Coord, Direction
from program import PlaceAction
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
    seen = []               
    # todo - cannot use set as lists are unhashable...
    # Work through a queue of semi-assembled tetrominoes to build whole set
    while len(in_progress) > 0:
        curr = in_progress.pop(0)
        curr.sort()     # ensures each piece+place is always defined the same
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


def tetrominoes_plus(c: Coord) -> list[Coord]:
    """Takes a Coord c and generates a list of Place actions of all unique 4 
    tiled "tetrominoes" that build off of this coordinate, that is, are adjacent
    to the coordinate but do NOT include it.
    List should always be of TODO un-calculated length - apparently 188?
    """
    t = []

    for dir in [d.value for d in Direction]:
        new = Coord.__add__(c, dir)
        # Add surrounding tetrominoes, omitting centre tile, and dropping dups
        t += [t1 for t1 in tetrominoes(new, [c]) if t1 not in t]
        # (1*s, 1*z, 1*l, 1*j, 2*t) * 4 = 24 dropped as dup

    return t


# possible = tetrominoes(Coord(0,0), [Coord(1,0)])
possible = tetrominoes_plus(Coord(0,0))
# possible = tetrominoes(Coord(0,0), [Coord(0,0)])
# possible.sort()
# for p in possible:
#     print(p.__str__())
print(len(possible))


# NO PLACEACTIONS HAVE BEEN CODED YET, NEED TO HARD CODE ALL OF THESE

def generate_I_touching(target: Coord) -> list[PlaceAction]:
    return [
        # for vertical
        PlaceAction(target.right(1), target.right(1).up(1), target.right(1).up(2), target.right(1).up(3)),  
        PlaceAction(target.right(1), target.right(1).up(1), target.right(1).up(2), target.right(1).down(1)),  
        PlaceAction(target.right(1), target.right(1).up(1), target.right(1).down(2), target.right(1).down(1)),  
        PlaceAction(target.right(1), target.right(1).down(3), target.right(1).down(2), target.right(1).down(1)),  
        PlaceAction(target.down(1), target.down(2), target.down(3), target.down(4)),  
        PlaceAction(target.up(1), target.up(2), target.up(3), target.up(4)),  
        PlaceAction(target.left(1), target.left(1).up(1), target.left(1).up(2), target.left(1).up(3)),  
        PlaceAction(target.left(1), target.left(1).up(1), target.left(1).up(2), target.left(1).down(1)),  
        PlaceAction(target.left(1), target.left(1).up(1), target.left(1).down(2), target.left(1).down(1)),  
        PlaceAction(target.left(1), target.left(1).down(3), target.left(1).down(2), target.left(1).down(1)),    
        
        # for horizontal
        PlaceAction(target.right(1), target.right(2), target.right(3), target.right(4)),  
        PlaceAction(target.left(1), target.left(2), target.left(3), target.left(4)),  
        PlaceAction(target.down(1), target.down(1).right(1), target.down(1).right(2), target.down(1).right(3)),  
        PlaceAction(target.down(1), target.down(1).left(1), target.down(1).right(1), target.down(1).right(2)),  
        PlaceAction(target.down(1), target.down(1).left(2), target.down(1).right(1), target.down(1).left(2)),  
        PlaceAction(target.down(1), target.down(1).left(4), target.down(1).left(2), target.down(1).left(1)),  
        PlaceAction(target.up(1), target.up(1).right(1), target.up(1).right(2), target.up(1).right(3)),  
        PlaceAction(target.up(1), target.up(1).left(1), target.up(1).right(1), target.up(1).right(2)),  
        PlaceAction(target.up(1), target.up(1).left(2), target.up(1).right(1), target.up(1).left(2)),  
        PlaceAction(target.up(1), target.up(1).left(4), target.up(1).left(2), target.up(1).left(1)),   
    ]

def generate_O_touching(target: Coord) -> list[PlaceAction]:
    return [
        PlaceAction(target.down(1), target.down(2), target.down(1).right(1), target.down(2).right(1)),  
        PlaceAction(target.down(1), target.down(2), target.down(1).left(1), target.down(2).left(1)),  
        PlaceAction(target.up(1), target.up(2), target.up(1).right(1), target.up(2).right(1)),  
        PlaceAction(target.up(1), target.up(2), target.up(1).left(1), target.up(2).left(1)),  
        PlaceAction(target.right(1), target.right(2), target.right(1).down(1), target.right(2).down(1)),  
        PlaceAction(target.right(1), target.right(2), target.right(1).up(1), target.right(2).up(1)),  
        PlaceAction(target.left(1), target.left(2), target.left(1).down(1), target.left(2).down(1)),  
        PlaceAction(target.left(1), target.left(2), target.left(1).up(1), target.left(2).up(1)),  
    ]

def generate_T_touching(target: Coord) -> list[PlaceAction]:
    return [
        # down, this is in order of shapes in specs
        PlaceAction(target.down(1), target.down(1).right(2), target.down(2).right(1), target.down(1).right(1)),  
        PlaceAction(target.down(1), target.down(1).left(1), target.down(1).right(1), target.down(2)),  
        PlaceAction(target.down(1), target.down(1).left(2), target.down(2).left(1), target.down(1).left(1)),  
        PlaceAction(target.left(1), target.left(2), target.left(3), target.left(2).down(1)),  
        PlaceAction(target.right(1), target.right(2), target.right(3), target.right(2).down(1)),  
        PlaceAction(target.up(1), target.left(1), target.up(1).left(1), target.up(1).left(2)),  
        PlaceAction(target.up(1), target.right(1), target.up(1).right(1), target.up(1).right(2)),  
        PlaceAction(target.up(1), target.up(2), target.up(2).left(1), target.up(2).right(1)),

        #up
        PlaceAction(target.right(1), target.down(1), target.down(1).right(1), target.down(2).right(1)),  
        PlaceAction(target.down(1), target.down(2), target.down(3), target.down(2).left(1)),  
        PlaceAction(target.left(1), target.down(1).left(1), target.down(1).left(2), target.down(2).left(1)),  
        PlaceAction(target.left(2), target.left(1), target.left(1).up(1), target.left(1).down(1)),  
        PlaceAction(target.left(1), target.left(1).up(1), target.left(1).up(2), target.left(2).up(1)),  
        PlaceAction(target.up(1), target.up(2), target.up(3), target.left(1).up(2)),  
        PlaceAction(target.right(1), target.right(1).up(1), target.up(1), target.right(1).up(2)),  
        PlaceAction(target.right(1), target.right(2), target.right(2).up(1), target.right(2).down(1)),

        #left
        PlaceAction(target.right(1), target.down(1), target.down(1).right(1), target.down(1).right(2)),  
        PlaceAction(target.down(2), target.down(1), target.down(2).left(1), target.down(2).right(1)),  
        PlaceAction(target.left(1), target.down(1), target.down(1).left(1), target.down(1).left(2)),  
        PlaceAction(target.left(1), target.left(2), target.left(3), target.left(2).up(1)),  
        PlaceAction(target.right(1), target.right(2), target.right(3), target.right(2).up(1)),  
        PlaceAction(target.up(1), target.up(2).left(1), target.up(1).left(1), target.up(1).left(2)),  
        PlaceAction(target.up(1), target.up(2), target.up(1).left(1), target.up(1).right(1)),  
        PlaceAction(target.up(1), target.up(2).right(1), target.up(1).right(1), target.up(1).right(2)),

        #right
        PlaceAction(target.down(1), target.down(2), target.down(2).right(1), target.down(3)),  
        PlaceAction(target.up(1), target.up(2), target.up(2).right(1), target.up(3)),  
        PlaceAction(target.left(1), target.down(1), target.down(1).left(1), target.down(2).left(1)),  
        PlaceAction(target.left(1), target.left(2), target.left(2).up(1), target.left(2).down(1)),  
        PlaceAction(target.left(1), target.up(1), target.up(1).left(1), target.up(2).left(1)),  
        PlaceAction(target.right(1), target.up(2).right(1), target.up(1).right(1), target.up(2).right(2)),  
        PlaceAction(target.right(1), target.right(2), target.up(1).right(1), target.down(1).right(1)),  
        PlaceAction(target.right(1), target.down(2).right(1), target.down(1).right(1), target.down(1).right(2)),
    ]

def generate_J_touching(target: Coord) -> list[PlaceAction]:
    return [
        #up this is in order of shapes in specs
        PlaceAction(target.right(1), target.down(1), target.down(1).right(1), target.right(1).up(1)),  
        PlaceAction(target.right(1), target.right(1).down(1), target.right(1).down(2), target.down(2)),  
        PlaceAction(target.down(1), target.down(2), target.down(3), target.down(3).left(1)),  
        PlaceAction(target.left(1), target.left(1).down(1), target.left(1).down(2), target.left(2).down(2)),  
        PlaceAction(target.left(1), target.left(1).up(1), target.left(1).down(1), target.left(2).down(1)),  
        PlaceAction(target.left(1), target.left(2), target.left(1).up(1), target.left(1).up(2)),  
        PlaceAction(target.left(1).up(1), target.up(1), target.up(2), target.up(3)),  
        PlaceAction(target.up(1), target.up(1).right(1), target.up(2).right(1), target.up(3).right(1)),  
        PlaceAction(target.right(1), target.right(2), target.right(2).up(1), target.right(2).up(2)),  

        #right
        PlaceAction(target.down(1), target.down(2), target.down(2).right(1), target.down(2).right(2)),  
        PlaceAction(target.left(1), target.left(1).down(1), target.down(1), target.down(1).right(1)),  
        PlaceAction(target.left(2), target.left(2).down(1), target.left(1).down(1), target.down(1)),  
        PlaceAction(target.left(1), target.left(2), target.left(3), target.left(3).up(1)),  
        PlaceAction(target.up(1), target.up(1).left(1), target.up(1).left(2), target.up(2).left(2)),  
        PlaceAction(target.up(1), target.up(1).right(1), target.up(1).left(1), target.up(2).left(1)),  
        PlaceAction(target.up(2), target.up(1), target.up(1).right(1), target.up(1).right(2)),  
        PlaceAction(target.right(1), target.up(1).right(1), target.right(2), target.right(3)),  
        PlaceAction(target.right(1), target.right(1).down(1), target.right(2).down(1), target.right(3).down(1)),  

        #down
        PlaceAction(target.down(1), target.down(2), target.down(3), target.down(1).right(1)),  
        PlaceAction(target.down(1), target.left(1).down(1), target.left(1).down(2), target.left(1).down(3)),  
        PlaceAction(target.left(1), target.left(2), target.left(2).down(1), target.left(2).down(2)),  
        PlaceAction(target.up(1), target.left(1), target.left(1).up(1), target.left(1).down(1)),  
        PlaceAction(target.up(2), target.left(1), target.left(1).up(1), target.left(1).up(2)),  
        PlaceAction(target.up(1), target.up(2), target.up(3), target.up(3).right(1)),  
        PlaceAction(target.right(1), target.right(1).up(1), target.right(1).up(2), target.right(2).up(2)),  
        PlaceAction(target.right(1), target.right(1).down(1), target.right(1).up(1), target.right(2).up(1)),  
        PlaceAction(target.right(2), target.right(1), target.right(1).down(1), target.right(1).down(2)),  

        #left
        PlaceAction(target.down(1), target.down(1).right(1), target.down(1).right(2), target.down(2).right(2)),  
        PlaceAction(target.down(1), target.down(1).left(1), target.down(1).right(1), target.down(2).right(1)),  
        PlaceAction(target.down(2), target.down(1), target.down(1).left(1), target.down(1).left(2)),  
        PlaceAction(target.left(1), target.left(2), target.left(3), target.left(1).down(1)),  
        PlaceAction(target.left(1), target.left(1).up(1), target.left(2).up(1), target.left(3).up(1)),  
        PlaceAction(target.up(1), target.up(2), target.up(2).left(1), target.up(2).left(2)),  
        PlaceAction(target.right(1), target.right(1).up(1), target.up(1), target.up(1).left(1)),  
        PlaceAction(target.up(1), target.up(1).right(1), target.up(1).right(2), target.right(2)),  
        PlaceAction(target.right(1), target.right(2), target.right(3), target.right(3).down(1)),  
    ]

def generate_L_touching(target: Coord) -> list[PlaceAction]:
    return [
        #up
        PlaceAction(target.right(2), target.right(1), target.right(1).up(1), target.right(1).up(2)),  
        PlaceAction(target.right(1), target.right(1).up(1), target.right(1).down(1), target.right(2).down(1)),  
        PlaceAction(target.right(1), target.right(1).down(1), target.right(1).down(2), target.right(2).down(2)),  
        PlaceAction(target.down(1), target.down(2), target.down(3), target.down(3).right(1)),  
        PlaceAction(target.left(1), target.left(1).down(1), target.left(1).down(2), target.down(2)),  
        PlaceAction(target.left(1), target.left(1).up(1), target.left(1).down(1), target.down(1)),  
        PlaceAction(target.left(1), target.left(2), target.left(2).up(1), target.left(2).up(2)),  
        PlaceAction(target.up(1), target.up(1).left(1), target.up(2).left(1), target.up(3).left(1)),  
        PlaceAction(target.up(1), target.up(2), target.up(3), target.up(1).right(1)),  

        #right
        PlaceAction(target.down(1), target.down(2), target.down(1).right(1), target.down(1).right(2)),  
        PlaceAction(target.down(1), target.down(1).left(1), target.down(1).right(1), target.down(2).left(1)),  
        PlaceAction(target.down(1), target.down(1).left(1), target.down(1).left(2), target.down(2).left(2)),  
        PlaceAction(target.left(1), target.left(2), target.left(3), target.left(3).down(1)),  
        PlaceAction(target.up(1), target.up(1).left(1), target.up(1).left(2), target.left(2)),  
        PlaceAction(target.up(1), target.up(1).right(1), target.up(1).left(1), target.left(1)),  
        PlaceAction(target.up(2), target.up(1), target.up(2).right(1), target.up(2).right(2)),  
        PlaceAction(target.right(1), target.right(1).up(1), target.right(2).up(1), target.right(3).up(1)),  
        PlaceAction(target.right(2), target.right(1), target.right(3), target.right(1).down(1)),  

        #down
        PlaceAction(target.down(1), target.down(1).right(1), target.down(2).right(1), target.down(3).right(1)),  
        PlaceAction(target.down(1), target.down(2), target.down(3), target.down(1).left(1)),  
        PlaceAction(target.left(1), target.left(2), target.left(1).down(1), target.left(1).down(2)),  
        PlaceAction(target.left(1), target.left(1).up(1), target.left(1).down(1), target.left(2).up(1)),  
        PlaceAction(target.left(1), target.left(1).up(1), target.left(1).up(2), target.left(2).up(2)),  
        PlaceAction(target.up(1), target.up(2), target.up(3), target.up(3).left(1)),  
        PlaceAction(target.right(1), target.right(1).up(1), target.right(1).up(2), target.up(2)),  
        PlaceAction(target.right(1), target.right(1).down(1), target.right(1).up(1), target.up()),  
        PlaceAction(target.right(1), target.right(2), target.right(2).down(1), target.right(2).down(2)),  

        #left
        PlaceAction(target.down(1), target.down(1).right(1), target.down(1).right(2), target.right(2)),  
        PlaceAction(target.down(1), target.down(1).left(1), target.down(1).right(1), target.right(1)),  
        PlaceAction(target.down(1), target.down(2), target.down(2).left(1), target.down(2).left(2)),  
        PlaceAction(target.left(1), target.left(1).down(1), target.down(1).left(2), target.down(1).left(3)),  
        PlaceAction(target.left(1), target.left(2), target.left(3), target.left(1).up(1)),  
        PlaceAction(target.up(1), target.up(2), target.up(1).left(1), target.up(1).left(2)),  
        PlaceAction(target.up(1), target.up(1).left(1), target.up(1).right(1), target.up(2).right(1)),  
        PlaceAction(target.up(1), target.up(1).right(1), target.up(1).right(2), target.up(2).right(2)),  
        PlaceAction(target.right(1), target.right(2), target.right(3), target.right(3).up(1)), 
    ]

def generate_Z_touching(target: Coord) -> list[PlaceAction]:
    return [
        # horizontal
        PlaceAction(target.down(1), target.down(1).right(1), target.down(2).right(1), target.down(2).right(2)),  
        PlaceAction(target.down(2), target.down(1), target.down(1).left(1), target.down(2).right(1)),  
        PlaceAction(target.left(1), target.left(2), target.left(1).down(1), target.down(1)),  
        PlaceAction(target.left(2), target.left(1), target.left(2).up(1), target.left(3).up(1)),  
        PlaceAction(target.up(1), target.up(1).left(1), target.up(2).left(1), target.up(2).left(2)),  
        PlaceAction(target.up(2), target.up(1), target.up(1).right(1), target.up(2).left(1)),  
        PlaceAction(target.right(1), target.right(2), target.right(1).up(1), target.up(1)),  
        PlaceAction(target.right(2), target.right(1), target.right(2).down(1), target.right(3).down(1)), 

        #vertical
        PlaceAction(target.right(1), target.down(1), target.down(1).right(1), target.down(2)),  
        PlaceAction(target.down(2), target.down(1), target.down(2).left(1), target.down(3).left(1)),  
        PlaceAction(target.left(1), target.left(1).down(1), target.left(2).down(1), target.left(2).down(2)),  
        PlaceAction(target.left(2), target.left(1), target.left(1).up(1), target.left(2).down(1)),  
        PlaceAction(target.up(1), target.up(2), target.left(1), target.up(1).left(1)),  
        PlaceAction(target.up(2), target.up(1), target.up(2).right(1), target.up(3).right(1)),  
        PlaceAction(target.right(1), target.right(1).up(1), target.right(2).up(1), target.right(2).up(2)),  
        PlaceAction(target.right(2), target.right(1), target.right(1).down(1), target.right(2).up(1)), 
    ]

def generate_S_touching(target: Coord) -> list[PlaceAction]:
    return [
        # horizontal
        PlaceAction(target.down(1), target.down(1).right(1), target.down(2), target.down(2).left(1)),  
        PlaceAction(target.down(1), target.down(1).left(1), target.down(2).left(1), target.down(2).left(2)),  
        PlaceAction(target.left(1), target.left(2), target.down(1).left(2), target.down(1).left(3)),  
        PlaceAction(target.left(2), target.left(1), target.up(1), target.up(1).left(1)),  
        PlaceAction(target.up(1), target.up(2), target.up(1).left(1), target.up(2).right(1)),  
        PlaceAction(target.up(1), target.up(1).right(1), target.up(2).right(1), target.up(2).right(2)),  
        PlaceAction(target.right(1), target.right(2), target.right(2).up(1), target.right(3).up(1)),  
        PlaceAction(target.down(1), target.right(1), target.down(1).right(1), target.right(2)), 

        #vertical
        PlaceAction(target.down(2).right(1), target.down(3).right(1), target.down(1), target.down(2)),  
        PlaceAction(target.left(1), target.down(1), target.down(2), target.down(1).left(1)),  
        PlaceAction(target.left(1), target.left(2), target.left(2).up(1), target.left(1).down(1)),  
        PlaceAction(target.left(1), target.left(1).up(1), target.left(2).up(1), target.left(2).up(2)),  
        PlaceAction(target.up(1), target.up(2), target.up(2).left(1), target.up(3).left(1)),  
        PlaceAction(target.right(1), target.up(1), target.up(1).right(1), target.up(2)),  
        PlaceAction(target.right(1), target.right(2), target.right(1).up(1), target.right(2).down(1)),  
        PlaceAction(target.right(1), target.right(1).down(1), target.right(2).down(1), target.right(2).down(2)), 
    ]

def generate_all_touching_shapes(target: Coord) -> list[PlaceAction]:
    touching_shapes = []
    touching_shapes.extend(generate_I_touching(target))
    touching_shapes.extend(generate_O_touching(target))
    touching_shapes.extend(generate_T_touching(target))
    touching_shapes.extend(generate_J_touching(target))
    touching_shapes.extend(generate_L_touching(target))
    touching_shapes.extend(generate_Z_touching(target))
    touching_shapes.extend(generate_S_touching(target))
    return touching_shapes