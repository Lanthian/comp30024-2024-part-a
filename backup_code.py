# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

# == Taken from program.py, 2023.04.03 ==
# todo: REDR - currently unused, opting for floats instead
def ceildiv(a, b):
    """Helper math function to perform ceiling division.
    Inspired by user @dlitz https://stackoverflow.com/users/253367/dlitz
        in post https://stackoverflow.com/a/17511341
    """
    return -(a // -b)

# todo: REDR - currently unused
def distance_from_axes(source: Coord, target: Coord) -> int:
    """Heuristic: Finds the minimum distance from a source coord to either of a 
    target coord's axes. Returns this integer.
    """
    row_distance = abs_distance(target.c,source.c)
    col_distance = abs_distance(target.r,source.r)
    
    return min(row_distance, col_distance)
