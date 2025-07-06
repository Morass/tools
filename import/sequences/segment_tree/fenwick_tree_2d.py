from collections import defaultdict
from functools import cache

class Fenwick2D:
    def __init__(self, n: int, m: int):
        self.n: int = n
        self.m: int = m
        self.tree: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))

    def add(self, x: int, y: int, delta: int) -> None:
        """ Adds delta to the value at (x, y) in the Fenwick Tree.

            Args:
                x (int): The x-coordinate (1-indexed).
                y (int): The y-coordinate (1-indexed).
                delta (int): The value to add.
        """
        xi = x
        while xi <= self.n:
            yi = y
            while yi <= self.m:
                self.tree[xi][yi] += delta
                yi += yi & -yi
            xi += xi & -xi

    @cache(maxsize=None)
    def prefix_sum(self, x, y) -> int:
        res = 0
        xi = x
        while xi > 0:
            yi = y
            while yi > 0:
                res += self.tree[xi][yi]
                yi -= yi & -yi
            xi -= xi & -xi
        return res

    def query_rect(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """ Calculates the sum of values in the rectangle defined by
            the corners (x1, y1) and (x2, y2).

            Args:
                x1 (int): The x-coordinate of the bottom-left corner (1-indexed).
                y1 (int): The y-coordinate of the bottom-left corner (1-indexed).
                x2 (int): The x-coordinate of the top-right corner (1-indexed).
                y2 (int): The y-coordinate of the top-right corner (1-indexed).

            Returns:
                int: The sum of values in the specified rectangle.
        """
        return (self.prefix_sum(x2, y2)
                - self.prefix_sum(x1 - 1, y2)
                - self.prefix_sum(x2, y1 - 1)
                + self.prefix_sum(x1 - 1, y1 - 1))
