# Points intersection
def lines_intersection(first: tuple, second: tuple) -> bool:
    """ Check if two lines (tuples of points) intersect

    Args:
        first (tuple(Point, Point)): First line.
        second (tuple(Point, Point)): Second line.

    Returns:
        bool: True of the lines intersect

    Complexity:
        O(1)
    """
    def get_side(one: Point, two: Point, three: Point) -> int:
        """ Check the side of third point (left/right/collinear)"""
        side = (two - one).y * (three - two).x - (three - two).y * (two - one).x
        if not side: return 0
        return -1 if side < 0 else 1

    def is_between(one: Point, two: Point, three: Point) -> bool:
        """ Checks if second point is in square formed by min/max coordinates of other points."""
        if two.x > max(one.x, three.x): return False
        if two.x < min(one.x, three.x): return False
        if two.y > max(one.y, three.y): return False
        if two.y < min(one.y, three.y): return False
        return True

    A, B = first
    C, D = second
    a, b, c, d = get_side(A, B, C), get_side(A, B, D), get_side(C, D, A), get_side(C, D, B)
    if a != b and c != d: return True
    if not a and is_between(A, C, B): return True
    if not b and is_between(A, D, B): return True
    if not c and is_between(C, A ,D): return True
    if not d and is_between(C, B, D): return True
    return False
