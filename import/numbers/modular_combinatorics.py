# Class for fast combinatorics computation(s) in modulo
class modularCombinatorics:
    """ Class for basic combinatorics problems in modulo - mostly including factorial.

    Variables:
        modulo (int): The integral base of the system
        factorial (list[int]): Factorial up to "N" (in modulo)
        inversion (list[int]): 1/factorial up to "N" (in modulo)
    """
    modulo = None
    factorial = None
    inversion = None

    def __init__(self, maximum: int = int(1e6), mod: int = int(1e9+7)):
        """ Initialisation of class -- mostly includes computation of factorial and its inversion up to "maximum" (inclusive)

        Args:
            maximum (int): The value (inclusive) for which the factorial and its inversion will be calculated. Defaults to 1e6.
            mod (int): The base in which all the calculations will be done. Defaults to 1e9+7

        Complexity:
            O(maximum + log(mod))
        """
        maximum+=1
        tmp = [1]*maximum
        self.inversion = [1]*maximum
        self.factorial = [1]*maximum
        self.modulo = mod
        for i in range(2, maximum):
            self.factorial[i]=self.factorial[i-1]*i%mod
            tmp[i]=-(mod//i*tmp[mod%i])%mod+mod
            self.inversion[i]=self.inversion[i-1]*tmp[i]%mod

    def fac(self, N: int) -> int:
        """ Calculates N!%mod

        Args:
            N (int): The N-th factorial we want to calculate

        Complexity:
            O(1)

        Returns:
            int: N!%mod

        Note:
            If factorial is negative then inversion is returned (i.e. for N==-6, 1/6! is returned)
        """
        if N < 0: return self.inversion[-N]
        return self.factorial[N]

    def permutations(self, items: list) -> int:
        """ Returns the number of permutations of "items" (each item can be there multiple times)

        Args:
            items (list[int]): Items to be permuted

        Complexity:
            O(len(items))

        Returns:
            int: Number of possible permutations of items

        Note:
            Formula: sum(items)!/(item[i]!*..*item[last]!)
        """
        ret = self.fac(sum(items))
        for i in items:
            ret = ret * self.fac(-i) % self.modulo
        return ret

    def choose(self, N: int, K: int = 2) -> int:
        """ Calculates N over K in modulo.

        Args:
            N (int): The number of items we are choosing from
            K (int): The number of items we are choosing

        Complexity:
            O(1)

        Returns:
            int: N over K
        """
        return self.permutations([N-K, K])

