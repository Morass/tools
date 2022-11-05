# Roling hash class
class rollingHash:
    """ This class accepts list, length, modulo and base and stores hashes of continuous subsequences of length "length".

        hashed_list (list[int]): List of rolling hashes
        powers (list[int]): Power of _base^i
        inversions (list[int]): Inversion of _base^-i
        _mod (int): Modulo used for rolling hash
        _base (int): Alphabet of integers in input list.
    """
    hashed_list = None
    powers = None
    inversions = None
    _mod = None
    _base = None
    def __init__(self, lst: list, base: int = 131,mod: int = 101210328665281103):
        """ Creates list of hashed subsequences (length len(lst))
        Args:
            lst (list[int]): List of arbitrary integers. Most expected use-case are characters of string.
            base (int): Prime number larger then largest of integers i nlst.
            mod (int): Modulo of rolling hash. The higher, the slower but the lower are chances on collision.

        Complexity:
            O(len(lst))

        Note:
            Even through linear complexity, the mathematical operations are pretty heavy.

        Note:
            There is an issue with "zeroes" so all integers will be added 1 (i.e. non-negative sequence is possible)
        """
        N = len(lst)
        self._base = base
        self._mod = mod
        self.powers = [1]*N
        self.inversions = [1]*N
        self.hashed_list = [0]*N
        self.hashed_list[0] = (lst[0]+1)%mod
        inv = self.inversions[1] = pow(base, mod-2, mod)
        for i in range(1, N):
            if i!=1: self.inversions[i]=self.inversions[i-1]*inv%mod
            self.powers[i] = self.powers[i-1]*base%mod
            self.hashed_list[i]=(self.powers[i]*(1+lst[i])+self.hashed_list[i-1])%mod

    def get(self, begin: int, end: int) -> int:
        """ Returns the value of rolling hash on indices begin -> end

        Args:
            begin (int): Start of sequence for which we want to calculate rolling hash.
            end (int): End of sequence for which we want to calculate rolling hash.

        Complexity:
            O(1)

        Returns:
            int: The rolling hash of subsequence between begin and end.
        """
        return (self.hashed_list[end]-(0 if not begin else self.hashed_list[begin-1])+self._mod)*self.inversions[begin]%self._mod

    @classmethod
    def from_string(cls, string: str, mod: int = int(1e9+7)) -> rollingHash:
        """ Creates rolling hash from "string" input

        Args:
            string (str): Input string (converted to list)
            mode (int): Modulus to be used

        Complexity:
            O(len(string))

        Returns:
            rollingHash: Roling hash class initialised with string
        """
        return cls([ord(c) for c in string], 131, mod)

