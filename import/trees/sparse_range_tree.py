from dataclasses import dataclass
from typing import Optional

@dataclass
class TreeNode:
    start: int
    end: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None
    min_val: Optional[int] = None
    max_val: Optional[int] = None

    def update(self):
        """Update min and max based on children"""
        min_vals = []
        max_vals = []

        if self.left:
            if self.left.min_val is not None:
                min_vals.append(self.left.min_val)
            if self.left.max_val is not None:
                max_vals.append(self.left.max_val)

        if self.right:
            if self.right.min_val is not None:
                min_vals.append(self.right.min_val)
            if self.right.max_val is not None:
                max_vals.append(self.right.max_val)

        self.min_val = min(min_vals) if min_vals else None
        self.max_val = max(max_vals) if max_vals else None

    def get_min(self) -> Optional[int]:
        return self.min_val

    def get_max(self) -> Optional[int]:
        return self.max_val


class SparseRangeTree:
    def __init__(self, k: int):
        """ K is the maximum number of bits in the range [0, 2^k - 1] """
        self.k = k
        self.N = 1 << k
        self.root = TreeNode(0, self.N - 1)

    def _insert(self, node: TreeNode, value: int):
        if node.start == node.end:
            node.min_val = node.max_val = value
            return

        mid = (node.start + node.end) // 2
        if value <= mid:
            if not node.left:
                node.left = TreeNode(node.start, mid)
            self._insert(node.left, value)
        else:
            if not node.right:
                node.right = TreeNode(mid + 1, node.end)
            self._insert(node.right, value)

        node.update()

    def insert(self, value: int):
        if 0 <= value < self.N:
            self._insert(self.root, value)

    def _delete(self, node: TreeNode, value: int):
        if not node or node.min_val is None:
            return

        if node.start == node.end:
            if node.min_val == value:
                node.min_val = node.max_val = None
            return

        mid = (node.start + node.end) // 2
        if value <= mid and node.left:
            self._delete(node.left, value)
        elif node.right:
            self._delete(node.right, value)

        node.update()

    def delete(self, value: int):
        if 0 <= value < self.N:
            self._delete(self.root, value)

    def _get_next(self, node: TreeNode, value: int) -> Optional[int]:
        if not node or node.min_val is None:
            return None

        if node.start > value:
            return node.get_min()

        if node.end <= value:
            return None

        left_result = self._get_next(node.left, value) if node.left else None
        right_result = self._get_next(node.right, value) if node.right else None

        if left_result is not None and left_result > value:
            return left_result
        if right_result is not None and right_result > value:
            return right_result
        return None

    def _get_prev(self, node: TreeNode, value: int) -> Optional[int]:
        if not node or node.max_val is None:
            return None

        if node.end < value:
            return node.get_max()

        if node.start >= value:
            return None

        right_result = self._get_prev(node.right, value) if node.right else None
        left_result = self._get_prev(node.left, value) if node.left else None

        if right_result is not None and right_result < value:
            return right_result
        if left_result is not None and left_result < value:
            return left_result
        return None

    def get_next(self, value: int) -> Optional[int]:
        return self._get_next(self.root, value)

    def get_prev(self, value: int) -> Optional[int]:
        return self._get_prev(self.root, value)

    def get_min(self) -> Optional[int]:
        return self.root.get_min()

    def get_max(self) -> Optional[int]:
        return self.root.get_max()
