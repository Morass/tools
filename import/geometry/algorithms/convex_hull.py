# Class for creation of convex hull
class convexHull:
    """ Data structure which accepts points (2D) and creates convex hull from them.

    Requires:
        import Point

    Variables:
        hull (list[point]): List with result convex hull.
        points (list[points]): list with points added to the data structure.

    Note:
        Structure uses Andrew's algorithm.
    """
    hull = None
    points = None
    def __init__(self):
        """ Creates points list.

        Complexity:
            O(1)
        """
        self.points = []

    def add_point(self, point: Point):
        """ Adds point to list with inserted points.

        Complexity:
            O(1)

        Args:
            points (Point): 2D point to be added.
        """
        self.points.append(point)

    def convex_hull(self):
        """ Creates convex hull.

        Complexity:
            O(NlogN))

        Note:
            First point will be duplicated as last point
        """
        self.hull = []
        if len(self.points) < 2:
            self.hull = list(self.points)
            return
        self.points.sort()
        for point in self.points:
            while len(self.hull) > 1 and self.hull[-2].bend(self.hull[-1], point) == -1:
                self.hull.pop()
            self.hull.append(point)
        self.points.reverse()
        total = len(self.hull)
        for point in self.points[1:]:
            while len(self.hull) > total and self.hull[-2].bend(self.hull[-1], point) == -1:
                self.hull.pop()
            self.hull.append(point)

    def get_perimeter(self) -> float:
        """ Gets perimeter of found convex hull.

        Complexity:
            O(hull-size)

        Returns:
            float: Perimeter of convex hull.
        """
        return sum([self.hull[i].distance(self.hull[i+1]) for i in range(len(self.hull)-1)])

    def get_hull(self) -> list(Point):
        """ Returns the convex hull.

        Note:
            Every point is returned once even though one of them is twice in the original representation.

        Complexity:
            O(1)

        Returns:
            list(Point): Convex hull starting from leftmost point.
        """
        return self.hull[:-1]

