# Sieve of Erathosenes to check primarity
class Sieve:
    """ Sieve of Eratosthenes.
        You can ask for prime or get all primes list (primes).
    """
    primes = [2]
    primarity = None
    def __init__(self, N: int):
        """ Processes upgraded sieve of Eratosthenes.

        Args:
            N (int): The size of sieve (0 to N inclusive)

        Complexity:
            O(Nlog(N))
        """
        # Import of sqrt!
        from math import sqrt
        N+=1
        Q = 1 + int(sqrt(N))
        self.primarity = [True]*N
        self.primarity[0] = self.primarity[1] = False
        for i in range(4, N, 2): self.primarity[i] = False
        for k in range(3, Q+1, 2):
            if self.primarity[k]:
                for j in range(k*k, N, k*2):
                    self.primarity[j] = False
        [self.primes.append(p) for p in range(3, N, 2) if self.primarity[p]]

    def is_prime(self, N: int) -> bool:
        """ Returns True if N is prime. It mus be in range of initiated number (inclusive).

        Args:
            N (int): Number to be tested

        Complexity:
            O(1)

        Returns:
            bool: True if argument is prime.
        """
        return self.primarity[N]
