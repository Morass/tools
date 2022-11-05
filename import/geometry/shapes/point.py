# 3 Dimensional point with basic operations
import math
class Point:
    """ Class which represents point in 3 dimensions (or 2 if last parameter is not set)

    Variables:
        x (float): X coordinate
        y (float): Y coordinate
        z (float): Z coordinate
    """
    x = None
    y = None
    z = None
    def __init__(self, x: float, y: float, z: float = 0):

        """ Initialisation of point by 2 or 3 of its coordinates

        Args:
            x (float): X coordinate of point.
            y (float): Y coordinate of point.
            z (float): Z coordinate of point (defaults to 0).

        Complexity:
            O(1)
        """
        self.x, self.y, self.z = x, y, z

    def __sub__(self, point: Point) -> Point:
        """ Subtraction operator for two point.

        Args:
            point (Point) Another point which is to be subtracted.

        Note:
            This function does not mangle with class - it creates new one.

        Complexity:
            O(1)

        Returns:
            Point: Result of operation "this point" - "arg point".

        Note:
            This is a scalar operation.
        """
        return Point(self.x-point.x, self.y-point.y, self.z-point.z)

    def __lt__(self, point: Point) -> bool:
        """ Operator "<" between two points. The lower coordinates the lower - priority X -> y -> z.

        Args:
            point (Point): The point with which we want to compare.

        Returns:
            bool: True, if this point is lesser than argument.

        Complexity:
            O(1)
        """
        if self.x != point.x: return self.x < point.x
        if self.y != point.y: return self.y < point.y
        return self.z < point.z

    def __repr__(self) -> str:
        """ Returns better representation of object for debugging.

        Returns:
            str: Representation if form of (x, y, z)

        Complexity:
            O(1)
        """
        return f"({self.x}, {self.y}, {self.z})"

    def dot(self, point: Point) -> float:
        """ Dot product of two points

        Args:
            point (Point): The point to get dot product with

        Complexity:
            O(1)

        Returns:
            float: The dot product of two points.

        Note:
            This is a scalar operation.
        """
        return self.x*point.x + self.y*point.y + self.z*point.z

    def cross(self, point: Point) -> Point:
        """ Cross product of two points

        Args:
            point (Point): The point to get cross product with

        Complexity:
            O(1)

        Returns:
            Point: The cross product of "this point" and "argument point".

        Note:
            This is a vector operation
        """
        return Point(self.y*point.z - self.z*point.y,
                     self.z*point.x - self.x*point.z,
                     self.x*point.y - self.y*point.x)

    def bend(self, second: Point, third: Point) -> int:
        """ Checks whether the angles of two points bend clockwise, anticlockwise or are straight.

        Note:
            The order of points is: This, second and then third.

        Args:
            second (Point): The second point in the angle.
            third (Point): The last point in the angle.

        Returns:
            1: If the angle is anti-clockwise.
            -1: If the angle is clockwise.
            0: If the angle is straight.
        """
        one = second - self
        two = third - self
        cross = one.x * two.y - one.y * two.x
        if cross > 0: return 1
        if cross < 0: return -1
        return 0


    def absolute(self) -> float:
        """ Returns the absolute of Point (|point|).

        Returns:
            float: |point|

        Complexity:
            O(1)
        """
        return pow((self.x ** 2 + self.y ** 2 + self.z ** 2), 0.5)

    def distance(self, point: Point) -> float:
        """ Find distance between two points.

        Args:
            point (Point): The second point to which we are seeking the distance.

        Returns:
            float: Distance between points.

        Complexity:
            O(1)
        """
        return math.sqrt(pow(self.x-point.x, 2)+
                         pow(self.y-point.y, 2)+
                         pow(self.z-point.z, 2))
