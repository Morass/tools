# Normalize
def normalize(A: list) -> tuple:
    """ Returns list in which values have same relative order but are from 0 to len(A)-1

    Args:
        A (list[int]): List of integer which is to be normalized.

    Complexity:
        O(Nlog(N))

    Returns:
        tuple: List of integers with same relative order.
               List of backward mapping
    """
    B = list(A)
    B.sort()
    d=dict()
    I=0
    for i in range(len(B)):
        if not i or B[i]!=B[i-1]:
            d[B[i]]=I
            I+=1
    Z = [d[i] for i in A]
    R = [-1]*len(d.values())
    for i, v in enumerate(A):
        R[Z[i]]=v
    return Z, R
