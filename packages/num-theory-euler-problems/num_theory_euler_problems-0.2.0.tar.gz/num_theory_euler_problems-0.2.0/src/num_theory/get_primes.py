def get_primes(num: int) -> list:
    '''
    Returns the list of all prime numbers less than or equal to n.

    Parameters
    -----------
    n: int. 

    Returns
    -----------
    list (containing integers) 
               
    Examples
    -----------
    >>> get_primes(14)
    [2, 5, 7, 11, 13]

    >>> get_primes(5)
    [2, 5]

    >>> get_primes(-2)
    []
    '''
    if not isinstance(num, (int, float)):
        raise TypeError("Input must be a numeric value (int or float).")
    
    num = int(num)
    
    prime = [True for i in range(num+1)]
    # boolean array
    p = 2
    while (p * p <= num):
 
        # If prime[p] is not changed, then it is a prime
        if (prime[p] == True):
 
            # Updating all multiples of p
            for i in range(p * p, num+1, p):
                prime[i] = False
        p += 1

    # For range of numbers, if a number is prime, add it to prime_nums
    # There is potential for further optimization here
    prime_nums = []
    for p in range(2, num+1):
        if prime[p]:
            prime_nums.append(p)
    
    return prime_nums