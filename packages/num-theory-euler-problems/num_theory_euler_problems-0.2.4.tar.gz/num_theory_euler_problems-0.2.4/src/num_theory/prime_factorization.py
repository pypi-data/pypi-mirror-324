def prime_factorization(n):
    """
    Compute the prime factorization of a given integer.

    Parameters
    ----------
    n : int
        The integer to factorize. Must be a positive integer greater than 1.

    Returns
    -------
    list of tuple
        A list of tuples where each tuple represents a prime factor and its corresponding power.
        Example: For n=28, the output will be [(2, 2), (7, 1)], indicating 28 = 2^2 * 7^1.

    Raises
    ------
    ValueError
        If the input `n` is not a positive integer greater than 1.

    Examples
    --------
    >>> prime_factorization(28)
    [(2, 2), (7, 1)]

    >>> prime_factorization(100)
    [(2, 2), (5, 2)]

    Notes
    -----
    - This function uses trial division to determine the prime factors.
    - For large values of `n`, consider optimized algorithms such as Pollard's Rho or
      the Quadratic Sieve for better performance.
    """
    
    # Defensive input validation
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    if n <= 1:
        raise ValueError("Input must be a positive integer greater than 1.")

    # Prime factorization using trial division
    factors = []
    divisor = 2

    while n > 1:
        power = 0
        while n % divisor == 0:
            n //= divisor
            power += 1
        if power > 0:
            factors.append((divisor, power))
        divisor += 1
        # Optimization: Stop if divisor squared is greater than n
        if divisor * divisor > n:
            break

    # If n is still greater than 1, it must be a prime number
    if n > 1:
        factors.append((n, 1))

    return factors