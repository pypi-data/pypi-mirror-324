def is_prime(n):
    """
    Check if a number is prime.

    Parameters
    ----------
    n : int
        The number to check for primality. Must be a positive integer greater than 1.

    Returns
    -------
    bool
        Returns True if the number is prime, otherwise False.

    Raises
    ------
    ValueError
        If the input is not a positive integer greater than 1.

    Examples
    --------
    >>> is_prime(2)
    True
    >>> is_prime(4)
    False
    >>> is_prime(13)
    True
    """
    # Input validation
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    if n <= 1:
        raise ValueError("Input must be a positive integer greater than 1.")

    # Check primality
    if n == 2:
        return True  # 2 is the smallest prime number
    if n % 2 == 0:
        return False  # Exclude all even numbers greater than 2

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False

    return True
