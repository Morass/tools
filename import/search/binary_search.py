# Binary search
def binary_search(beg: int, end: int, foo: int) -> int:
    """
    Args:
        beg (int): Lowest possible value
        end (int): Highest possible value
        foo (function): Function which returns true or false (first true then false)

    Returns:
        int: The last value for which "foo" yields true.

    Complexity:
        O(log(end-beg))
    """
    mn = beg
    while beg < end:
        if foo(M := (beg + end)//2): end = M
        else: beg = M+1
    return max(mn, beg-1)
